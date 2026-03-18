# file: Kochi-Metro-main/inventory_management.py
#!/usr/bin/env python3
"""
KMRL Inventory Management – Spare Parts Reorder & Summary
Adds an inventory module aligned with other project scripts.

Usage:
  python inventory_management.py
  python inventory_management.py --csv metro_spare_parts_inventory.csv --out .

Outputs:
  - inventory_reorder_report.csv  : Rows needing reorder (priority-sorted)
  - inventory_summary.json        : KPIs & distribution stats
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

import pandas as pd


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    warnings: List[str]


REQUIRED_COLS = {"Quantity_Available", "Reorder_Level"}
NUMERIC_COLS = ["Quantity_Available", "Reorder_Level", "Unit_Cost", "Lead_Time_Days", "Usage_Count"]
DATE_PREFS = ["Last_Used_Date", "Last_Inspection_Date"]


def read_inventory(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    df = pd.read_csv(path)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df


def validate_and_coerce(df: pd.DataFrame) -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")

    # Coerce numbers
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            neg = df[col] < 0
            if neg.any():
                # Negative stock/lead-time is nonsense operationally
                warnings.append(f"Negative values in {col} set to 0")
                df.loc[neg, col] = 0
            df[col] = df[col].fillna(0)

    # Dates (prefer last used; fallback to last inspection)
    date_col = next((c for c in DATE_PREFS if c in df.columns), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df["days_since_last_used"] = (pd.Timestamp(datetime.utcnow().date()) - df[date_col].dt.normalize()).dt.days
    else:
        df["days_since_last_used"] = pd.NA

    # Tidy strings to avoid grouping issues
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    return ValidationResult(ok=not errors, errors=errors, warnings=warnings)


def derive(df: pd.DataFrame) -> pd.DataFrame:
    if REQUIRED_COLS.issubset(df.columns):
        df["needs_reorder"] = (df["Quantity_Available"] <= df["Reorder_Level"]).fillna(False)
    else:
        df["needs_reorder"] = False

    crit_col = "Criticality_Level" if "Criticality_Level" in df.columns else ("Criticality" if "Criticality" in df.columns else None)
    crit_map = {"high": 3, "medium": 2, "low": 1}
    crit_score = (
        df[crit_col].astype(str).str.lower().map(crit_map).fillna(0) if crit_col else pd.Series(0, index=df.index)
    )
    lead = df["Lead_Time_Days"] if "Lead_Time_Days" in df.columns else pd.Series(0, index=df.index)
    usage = df["Usage_Count"] if "Usage_Count" in df.columns else pd.Series(0, index=df.index)

    # Priority favors critical parts, long lead time, and high usage
    base = crit_score + (lead.fillna(0) / 10.0) + (usage.fillna(0) / 10.0)
    df["priority"] = base.where(df["needs_reorder"], -1.0)
    return df


def summarize(df: pd.DataFrame) -> Dict[str, Any]:
    total = len(df)
    needs = int(df["needs_reorder"].sum()) if "needs_reorder" in df.columns else 0
    by_crit: Dict[str, int] = {}
    for col in ["Criticality_Level", "Criticality"]:
        if col in df.columns:
            by_crit = df.loc[df["needs_reorder"] == True, col].astype(str).str.title().value_counts().to_dict()  # noqa: E712
            break

    by_cat = df.loc[df["needs_reorder"] == True, "Category"].value_counts().to_dict() if "Category" in df.columns else {}
    avg_lead = float(df.loc[df["needs_reorder"] == True, "Lead_Time_Days"].mean()) if "Lead_Time_Days" in df.columns else None

    return {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "total_parts": total,
        "needs_reorder": needs,
        "reorder_rate_pct": round((needs / total * 100.0), 2) if total else 0.0,
        "avg_lead_time_days_reorder": round(avg_lead, 2) if avg_lead is not None and not pd.isna(avg_lead) else None,
        "by_criticality_reorder": by_crit,
        "by_category_reorder": by_cat,
    }


def build_report(df: pd.DataFrame, limit: Optional[int]) -> pd.DataFrame:
    cols = [c for c in [
        "Part_ID", "Part_Name", "Category", "Supplier_Name", "Storage_Location",
        "Quantity_Available", "Reorder_Level", "Unit_Cost",
        "Lead_Time_Days", "Usage_Count",
        "Criticality_Level", "Criticality", "days_since_last_used",
        "needs_reorder", "priority"
    ] if c in df.columns]
    rep = df[df["needs_reorder"] == True].copy()  # noqa: E712
    rep = rep.sort_values(["priority"], ascending=False)
    if limit:
        rep = rep.head(limit)
    return rep[cols] if cols else rep


def save_outputs(summary: Dict[str, Any], report: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "inventory_summary.json").write_text(pd.io.json.dumps(summary, indent=2))
    report.to_csv(out_dir / "inventory_reorder_report.csv", index=False)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="KMRL Inventory Management – Reorder analysis")
    parser.add_argument("--csv", default="metro_spare_parts_inventory.csv", help="Inventory CSV path")
    parser.add_argument("--out", default=".", help="Output directory")
    parser.add_argument("--limit", type=int, default=None, help="Limit report rows")
    args = parser.parse_args(argv)

    csv_path = Path(args.csv)
    out_path = Path(args.out)

    print("🧰 KMRL Inventory Management")
    print("=" * 30)
    print(f"CSV: {csv_path.resolve()}")
    print(f"Out: {out_path.resolve()}")

    df = read_inventory(csv_path)
    vr = validate_and_coerce(df)
    df = derive(df)

    if vr.warnings:
        print("\nWarnings:")
        for w in vr.warnings:
            print(f" - {w}")
    if not vr.ok:
        print("\nValidation errors:")
        for e in vr.errors:
            print(f" - {e}")
        print("Proceeding with best-effort outputs...\n")

    summary = summarize(df)
    report = build_report(df, args.limit)
    save_outputs(summary, report, out_path)

    print("\n📦 Outputs:")
    print(f" - {out_path / 'inventory_summary.json'}")
    print(f" - {out_path / 'inventory_reorder_report.csv'}")
    print(f"\n✅ Done. Reorder items: {summary['needs_reorder']} / {summary['total_parts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

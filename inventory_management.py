#!/usr/bin/env python3
"""
KMRL Inventory Management System
===============================
Integrated inventory management module for Kochi Metro Rail Limited.
Provides spare parts management, reorder analysis, and reporting functionality.

Usage:
  python inventory_management.py
  python inventory_management.py --csv metro_spare_parts_inventory.csv --out reports/

Features:
  - Automatic reorder level calculation
  - Critical parts identification
  - Supplier performance analysis
  - Real-time inventory reporting
  - Integration with existing KMRL systems

Author: KMRL Development Team
Date: 2025-09-28
"""

import argparse
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class InventoryValidation:
    """Results of inventory data validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    total_parts: int

class InventoryManager:
    """Main inventory management class for KMRL spare parts."""
    
    REQUIRED_COLUMNS = {
        'Part_ID', 'Part_Name', 'Quantity_Available', 'Reorder_Level'
    }
    
    NUMERIC_COLUMNS = [
        'Quantity_Available', 'Reorder_Level', 'Unit_Cost', 
        'Lead_Time_Days', 'Usage_Count'
    ]
    
    CRITICALITY_PRIORITY = {
        'high': 3,
        'medium': 2, 
        'low': 1
    }
    
    def __init__(self, csv_path: Path):
        """Initialize inventory manager with CSV data."""
        self.csv_path = csv_path
        self.data: Optional[pd.DataFrame] = None
        self.processed_data: Optional[pd.DataFrame] = None
        
    def load_data(self) -> pd.DataFrame:
        """Load and clean inventory data from CSV."""
        logger.info(f"Loading inventory data from {self.csv_path}")
        
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Inventory CSV not found: {self.csv_path}")
            
        # Read and clean column names
        self.data = pd.read_csv(self.csv_path)
        self.data.columns = [col.strip().replace(' ', '_') for col in self.data.columns]
        
        logger.info(f"Loaded {len(self.data)} parts from inventory")
        return self.data
    
    def validate_data(self) -> InventoryValidation:
        """Validate inventory data quality and completeness."""
        errors = []
        warnings = []
        
        if self.data is None:
            errors.append("No data loaded")
            return InventoryValidation(False, errors, warnings, 0)
        
        # Check required columns
        missing_cols = self.REQUIRED_COLUMNS - set(self.data.columns)
        if missing_cols:
            errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        
        # Validate numeric columns
        for col in self.NUMERIC_COLUMNS:
            if col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
                
                # Check for negative values
                negative_mask = self.data[col] < 0
                if negative_mask.any():
                    warnings.append(f"Found negative values in {col}, setting to 0")
                    self.data.loc[negative_mask, col] = 0
                
                # Fill NaN values
                self.data[col] = self.data[col].fillna(0)
        
        # Clean string columns
        for col in self.data.select_dtypes(include=['object']).columns:
            self.data[col] = self.data[col].astype(str).str.strip()
        
        is_valid = len(errors) == 0
        total_parts = len(self.data)
        
        return InventoryValidation(is_valid, errors, warnings, total_parts)
    
    def analyze_reorder_needs(self) -> pd.DataFrame:
        """Analyze parts that need reordering and calculate priorities."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Create processed copy
        self.processed_data = self.data.copy()
        
        # Determine reorder needs
        self.processed_data['needs_reorder'] = (
            self.processed_data['Quantity_Available'] <= 
            self.processed_data['Reorder_Level']
        )
        
        # Calculate criticality score
        criticality_col = self._find_criticality_column()
        if criticality_col:
            criticality_score = (
                self.processed_data[criticality_col]
                .astype(str)
                .str.lower()
                .map(self.CRITICALITY_PRIORITY)
                .fillna(1)
            )
        else:
            criticality_score = pd.Series(1, index=self.processed_data.index)
        
        # Calculate priority score
        lead_time = self.processed_data.get('Lead_Time_Days', pd.Series(0, index=self.processed_data.index))
        usage_count = self.processed_data.get('Usage_Count', pd.Series(0, index=self.processed_data.index))
        
        # Priority calculation: criticality + lead_time factor + usage factor
        priority_score = (
            criticality_score * 10 +  # Base criticality
            (lead_time.fillna(0) / 10) +  # Lead time impact
            (usage_count.fillna(0) / 100)  # Usage frequency impact
        )
        
        # Only assign priority to parts that need reordering
        self.processed_data['priority_score'] = priority_score.where(
            self.processed_data['needs_reorder'], 0
        )
        
        return self.processed_data
    
    def _find_criticality_column(self) -> Optional[str]:
        """Find the criticality column in data."""
        possible_names = ['Criticality_Level', 'Criticality', 'Priority']
        for name in possible_names:
            if name in self.processed_data.columns:
                return name
        return None
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate inventory summary statistics."""
        if self.processed_data is None:
            raise ValueError("Data not analyzed. Call analyze_reorder_needs() first.")
        
        total_parts = len(self.processed_data)
        needs_reorder = self.processed_data['needs_reorder'].sum()
        
        # Critical parts (high criticality AND needs reorder)
        criticality_col = self._find_criticality_column()
        if criticality_col:
            critical_reorder = len(
                self.processed_data[
                    (self.processed_data['needs_reorder']) & 
                    (self.processed_data[criticality_col].str.lower() == 'high')
                ]
            )
        else:
            critical_reorder = 0
        
        # Average lead time for parts needing reorder
        reorder_parts = self.processed_data[self.processed_data['needs_reorder']]
        avg_lead_time = None
        if len(reorder_parts) > 0 and 'Lead_Time_Days' in reorder_parts.columns:
            avg_lead_time = reorder_parts['Lead_Time_Days'].mean()
        
        # Category breakdown
        category_breakdown = {}
        if 'Category' in self.processed_data.columns:
            category_breakdown = (
                self.processed_data[self.processed_data['needs_reorder']]
                ['Category']
                .value_counts()
                .to_dict()
            )
        
        # Supplier breakdown  
        supplier_breakdown = {}
        if 'Supplier_Name' in self.processed_data.columns:
            supplier_breakdown = (
                self.processed_data[self.processed_data['needs_reorder']]
                ['Supplier_Name']
                .value_counts()
                .to_dict()
            )
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'total_parts': int(total_parts),
            'needs_reorder': int(needs_reorder),
            'reorder_percentage': round((needs_reorder / total_parts) * 100, 2) if total_parts > 0 else 0,
            'critical_priority': int(critical_reorder),
            'avg_lead_time_days': round(avg_lead_time, 2) if avg_lead_time is not None else None,
            'category_breakdown': category_breakdown,
            'supplier_breakdown': supplier_breakdown,
            'system': 'KMRL Inventory Management',
            'version': '1.0.0'
        }
    
    def get_reorder_report(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Get prioritized reorder report."""
        if self.processed_data is None:
            raise ValueError("Data not analyzed. Call analyze_reorder_needs() first.")
        
        # Filter parts that need reordering
        reorder_parts = self.processed_data[self.processed_data['needs_reorder']].copy()
        
        # Sort by priority score (descending)
        reorder_parts = reorder_parts.sort_values('priority_score', ascending=False)
        
        # Limit results if specified
        if limit:
            reorder_parts = reorder_parts.head(limit)
        
        # Select relevant columns for report
        report_columns = [
            col for col in [
                'Part_ID', 'Part_Name', 'Category', 'Supplier_Name', 
                'Storage_Location', 'Quantity_Available', 'Reorder_Level',
                'Unit_Cost', 'Lead_Time_Days', 'Usage_Count',
                'Criticality_Level', 'needs_reorder', 'priority_score'
            ] if col in reorder_parts.columns
        ]
        
        return reorder_parts[report_columns]
    
    def save_reports(self, output_dir: Path):
        """Save inventory reports to files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate reports
        summary = self.generate_summary()
        reorder_report = self.get_reorder_report()
        
        # Save summary JSON
        summary_file = output_dir / 'inventory_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        # Save reorder report CSV
        report_file = output_dir / 'inventory_reorder_report.csv'
        reorder_report.to_csv(report_file, index=False)
        
        logger.info(f"Reports saved to {output_dir}")
        logger.info(f"  - Summary: {summary_file}")
        logger.info(f"  - Reorder Report: {report_file}")
        
        return summary_file, report_file

def main():
    """Main entry point for inventory management."""
    parser = argparse.ArgumentParser(
        description="KMRL Inventory Management - Spare Parts Analysis"
    )
    parser.add_argument(
        '--csv', 
        default='metro_spare_parts_inventory.csv',
        help='Path to inventory CSV file'
    )
    parser.add_argument(
        '--out', 
        default='.',
        help='Output directory for reports'
    )
    parser.add_argument(
        '--limit', 
        type=int, 
        help='Limit number of parts in reorder report'
    )
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize paths
    csv_path = Path(args.csv)
    output_dir = Path(args.out)
    
    try:
        print("🧰 KMRL Inventory Management System")
        print("=" * 50)
        print(f"📁 Input CSV: {csv_path.resolve()}")
        print(f"📊 Output Directory: {output_dir.resolve()}")
        
        # Initialize inventory manager
        manager = InventoryManager(csv_path)
        
        # Load and validate data
        manager.load_data()
        validation = manager.validate_data()
        
        # Print validation results
        print(f"\n✅ Validation Results:")
        print(f"   Total Parts: {validation.total_parts}")
        print(f"   Status: {'✅ Valid' if validation.is_valid else '❌ Invalid'}")
        
        if validation.warnings:
            print("\n⚠️  Warnings:")
            for warning in validation.warnings:
                print(f"   - {warning}")
        
        if validation.errors:
            print("\n❌ Errors:")
            for error in validation.errors:
                print(f"   - {error}")
            
            if not validation.is_valid:
                print("\n🚫 Cannot proceed due to validation errors.")
                return 1
        
        # Analyze reorder needs
        print("\n🔍 Analyzing reorder requirements...")
        manager.analyze_reorder_needs()
        
        # Generate summary
        summary = manager.generate_summary()
        
        print(f"\n📋 Inventory Summary:")
        print(f"   Total Parts: {summary['total_parts']}")
        print(f"   Need Reorder: {summary['needs_reorder']} ({summary['reorder_percentage']}%)")
        print(f"   Critical Priority: {summary['critical_priority']}")
        if summary['avg_lead_time_days']:
            print(f"   Avg Lead Time: {summary['avg_lead_time_days']} days")
        
        # Save reports
        print("\n💾 Saving reports...")
        summary_file, report_file = manager.save_reports(output_dir)
        
        print(f"\n🎉 Inventory analysis complete!")
        print(f"📄 Summary: {summary_file}")
        print(f"📊 Reorder Report: {report_file}")
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit(main())
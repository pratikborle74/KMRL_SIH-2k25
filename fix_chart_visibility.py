#!/usr/bin/env python
"""
Quick fix script to ensure all Plotly charts have visible text
"""

import re

def fix_chart_visibility():
    # Read the dashboard file
    with open('kmrl_interactive_dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count current fixes
    current_font_fixes = content.count("font=dict(color='#212121')")
    print(f"Current font fixes found: {current_font_fixes}")
    
    # Find all st.plotly_chart calls
    chart_calls = re.findall(r'st\.plotly_chart\(fig, width=\'stretch\'\)', content)
    print(f"Total chart calls found: {len(chart_calls)}")
    
    # Simple approach: Add a universal chart styling function call before each chart
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # If this line creates a plotly chart, ensure the next few lines have proper styling
        if 'st.plotly_chart(fig, width=\'stretch\')' in line:
            # Check if previous lines have update_layout with font
            has_font_styling = False
            for j in range(max(0, i-10), i):
                if 'font=dict(color=' in lines[j] or 'font={' in lines[j]:
                    has_font_styling = True
                    break
            
            if not has_font_styling:
                # Insert styling before the chart call
                indent = len(line) - len(line.lstrip())
                styling_line = ' ' * indent + 'ensure_chart_visibility(fig)'
                fixed_lines.insert(-1, styling_line)  # Insert before the chart call
    
    # Write the fixed version
    with open('kmrl_interactive_dashboard.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("Chart visibility fix applied!")

if __name__ == '__main__':
    fix_chart_visibility()
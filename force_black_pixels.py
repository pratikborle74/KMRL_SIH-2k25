#!/usr/bin/env python
"""
FORCE BLACK PIXELS - Direct pixel manipulation approach
This bypasses matplotlib's text rendering and forces pixels to be black
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

def force_black_text_pixels():
    """Create matplotlib chart then force text pixels to black"""
    
    print("🔧 Creating chart with FORCED BLACK PIXELS...")
    
    # Step 1: Create matplotlib chart normally
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
    
    # KMRL data
    models = ['Failure\nPrediction', 'Optimization\nDecision', 'Demand\nForecasting']
    accuracies = [98.6, 100.0, 50.0]
    colors = ['red', 'blue', 'green']
    
    # Create bars
    bars = ax.bar(models, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add text (matplotlib will render this however it wants)
    ax.set_title('KMRL ML Model Performance', fontsize=16, fontweight='bold')
    ax.set_xlabel('Models', fontsize=12, fontweight='bold')  
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.tick_params(labelsize=10)
    
    # Add percentage labels
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc:.1f}%', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # Step 2: Save to memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, facecolor='white', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    # Step 3: Open with PIL and force text pixels to black
    image = Image.open(buf)
    pixels = image.load()
    width, height = image.size
    
    print(f"📊 Processing {width}x{height} image...")
    
    # Step 4: Find light gray pixels and make them black
    black_pixel_count = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]  # Get RGB values
            
            # If pixel is light gray (likely text), make it pure black
            gray_level = (r + g + b) / 3
            if 50 < gray_level < 200:  # Light gray range
                pixels[x, y] = (0, 0, 0)  # Force to black
                black_pixel_count += 1
    
    print(f"✅ Forced {black_pixel_count} pixels to black")
    
    # Step 5: Save the modified image
    image.save('FORCED_BLACK_PIXELS.png')
    print("✅ Saved: FORCED_BLACK_PIXELS.png")
    
    return image

def create_pure_pil_chart():
    """Create chart entirely with PIL (no matplotlib)"""
    
    print("🎨 Creating chart with PURE PIL (no matplotlib)...")
    
    # Create image
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to load a font
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        label_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw title
    draw.text((400, 50), 'KMRL ML Model Performance', fill=(0, 0, 0), 
              font=title_font, anchor='mt')
    
    # Draw bars manually
    bar_width = 120
    bar_spacing = 200
    bar_colors = ['red', 'blue', 'green']
    models = ['Failure\nPrediction', 'Optimization\nDecision', 'Demand\nForecasting']
    accuracies = [98.6, 100.0, 50.0]
    
    base_y = 500
    max_height = 300
    
    for i, (model, acc, color) in enumerate(zip(models, accuracies, bar_colors)):
        x = 100 + i * bar_spacing
        bar_height = int(max_height * acc / 100)
        
        # Draw bar
        draw.rectangle([x, base_y - bar_height, x + bar_width, base_y], 
                      fill=color, outline=(0, 0, 0), width=2)
        
        # Draw model label (pure black text) - handle multiline manually
        model_lines = model.split('\n')
        for j, line in enumerate(model_lines):
            draw.text((x + bar_width//2, base_y + 20 + j * 20), line, fill=(0, 0, 0), 
                     font=small_font, anchor='mt')
        
        # Draw percentage (pure black text)  
        draw.text((x + bar_width//2, base_y - bar_height - 30), f'{acc:.1f}%', 
                 fill=(0, 0, 0), font=label_font, anchor='mb')
    
    # Draw axes labels (pure black text)
    draw.text((50, 350), 'Accuracy (%)', fill=(0, 0, 0), font=label_font, anchor='mm')
    draw.text((400, 580), 'Models', fill=(0, 0, 0), font=label_font, anchor='mm')
    
    # Draw axis lines
    draw.line([(80, 200), (80, 500)], fill=(0, 0, 0), width=3)  # Y-axis
    draw.line([(80, 500), (720, 500)], fill=(0, 0, 0), width=3)  # X-axis
    
    image.save('PURE_PIL_CHART.png')
    print("✅ Saved: PURE_PIL_CHART.png")
    
    return image

def create_text_only_black():
    """Create image with only text to verify black pixels"""
    
    print("📝 Creating TEXT-ONLY with pure black pixels...")
    
    image = Image.new('RGB', (600, 400), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Draw multiple lines of pure black text
    texts = [
        "THIS IS BLACK TEXT",
        "RGB (0, 0, 0)",
        "PURE BLACK PIXELS"
    ]
    
    y_pos = 80
    for text in texts:
        draw.text((300, y_pos), text, fill=(0, 0, 0), font=font, anchor='mt')
        y_pos += 80
    
    # Add a black rectangle for comparison
    draw.rectangle([50, 300, 550, 350], fill=(0, 0, 0))
    
    image.save('TEXT_ONLY_BLACK.png')
    print("✅ Saved: TEXT_ONLY_BLACK.png")
    
    # Verify pixels
    test_pixel = image.getpixel((300, 100))
    print(f"📊 Text pixel RGB: {test_pixel}")
    if test_pixel == (0, 0, 0):
        print("✅ TEXT PIXELS ARE PURE BLACK!")
    else:
        print(f"❌ Text pixels are: {test_pixel}")
    
    return image

def main():
    """Run all pixel forcing methods"""
    
    print("🔧 FORCING BLACK PIXELS - DIRECT APPROACH")
    print("=" * 50)
    
    # Method 1: Force matplotlib pixels to black
    force_black_text_pixels()
    print()
    
    # Method 2: Pure PIL chart
    create_pure_pil_chart()
    print()
    
    # Method 3: Text-only verification
    create_text_only_black()
    
    print("\n" + "=" * 50)
    print("🔧 PIXEL FORCING COMPLETE!")
    print("\nFiles created:")
    print("• FORCED_BLACK_PIXELS.png - Matplotlib with forced black pixels")
    print("• PURE_PIL_CHART.png - Chart made entirely with PIL")
    print("• TEXT_ONLY_BLACK.png - Pure black text test")
    
    print("\n🧪 TEST THESE FILES:")
    print("1. TEXT_ONLY_BLACK.png should have PURE BLACK text")
    print("2. If TEXT_ONLY_BLACK.png text is still light,")
    print("   the issue is your display/viewer settings")
    print("=" * 50)

if __name__ == "__main__":
    main()
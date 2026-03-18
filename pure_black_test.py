#!/usr/bin/env python
"""
PURE BLACK PIXEL TEST - No text rendering, just raw black pixels
This creates images with guaranteed black pixels
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_raw_black_pixels():
    """Create image with raw black pixels using numpy"""
    
    print("🖤 Creating RAW BLACK PIXELS (no text rendering)...")
    
    # Create a 600x400 white image
    width, height = 600, 400
    image_array = np.full((height, width, 3), 255, dtype=np.uint8)  # Start with white
    
    # Draw black rectangles and shapes manually
    # Big black rectangle
    image_array[50:150, 50:550] = [0, 0, 0]  # Pure black
    
    # Black stripes
    for y in range(200, 350, 20):
        image_array[y:y+10, 50:550] = [0, 0, 0]  # Black stripes
    
    # Convert to PIL Image
    image = Image.fromarray(image_array, 'RGB')
    image.save('RAW_BLACK_PIXELS.png')
    
    # Verify pixels
    test_pixel = image.getpixel((100, 100))  # Should be black
    white_pixel = image.getpixel((100, 30))   # Should be white
    
    print(f"📊 Black area pixel: {test_pixel}")
    print(f"📊 White area pixel: {white_pixel}")
    
    if test_pixel == (0, 0, 0):
        print("✅ RAW BLACK PIXELS ARE CORRECT!")
    else:
        print(f"❌ Even raw pixels are wrong: {test_pixel}")
    
    return image

def create_matplotlib_black_shapes():
    """Create black shapes with matplotlib"""
    
    print("📐 Creating BLACK SHAPES with matplotlib...")
    
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
    
    # Add black rectangles
    rect1 = patches.Rectangle((0.1, 0.7), 0.8, 0.2, linewidth=0, facecolor='black')
    rect2 = patches.Rectangle((0.1, 0.1), 0.8, 0.2, linewidth=0, facecolor='#000000')
    
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    # Add black circles
    circle = patches.Circle((0.5, 0.5), 0.15, linewidth=0, facecolor='k')
    ax.add_patch(circle)
    
    # Remove axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('MATPLOTLIB_BLACK_SHAPES.png', dpi=150, facecolor='white', 
                bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print("✅ Saved: MATPLOTLIB_BLACK_SHAPES.png")

def create_text_bitmap():
    """Create text using PIL with absolute black verification"""
    
    print("🔤 Creating TEXT BITMAP with absolute verification...")
    
    # Create white image
    image = Image.new('RGB', (500, 200), (255, 255, 255))
    
    # Manually draw letters using black pixels
    pixels = image.load()
    
    # Draw letter "A" manually with black pixels
    # Simple bitmap font approach
    letter_A = [
        "  ###  ",
        " ## ## ",
        "##   ##",
        "#######",
        "##   ##",
        "##   ##",
        "##   ##"
    ]
    
    start_x, start_y = 50, 50
    scale = 3  # Make it bigger
    
    for row, line in enumerate(letter_A):
        for col, char in enumerate(line):
            if char == '#':
                # Draw a scale x scale black square
                for dy in range(scale):
                    for dx in range(scale):
                        x = start_x + col * scale + dx
                        y = start_y + row * scale + dy
                        if x < 500 and y < 200:
                            pixels[x, y] = (0, 0, 0)  # Force black
    
    # Draw letter "B" next to it
    letter_B = [
        "######",
        "##   ##",
        "##   ##", 
        "######",
        "##   ##",
        "##   ##",
        "######"
    ]
    
    start_x = 150
    for row, line in enumerate(letter_B):
        for col, char in enumerate(line):
            if char == '#':
                for dy in range(scale):
                    for dx in range(scale):
                        x = start_x + col * scale + dx
                        y = start_y + row * scale + dy
                        if x < 500 and y < 200:
                            pixels[x, y] = (0, 0, 0)  # Force black
    
    image.save('TEXT_BITMAP.png')
    
    # Verify the pixels we just set
    test_pixel_A = image.getpixel((60, 60))  # Should be black from letter A
    test_pixel_B = image.getpixel((160, 60))  # Should be black from letter B
    test_pixel_white = image.getpixel((10, 10))  # Should be white background
    
    print(f"📊 Letter A pixel: {test_pixel_A}")
    print(f"📊 Letter B pixel: {test_pixel_B}")
    print(f"📊 Background pixel: {test_pixel_white}")
    
    if test_pixel_A == (0, 0, 0) and test_pixel_B == (0, 0, 0):
        print("✅ MANUALLY DRAWN TEXT IS BLACK!")
    else:
        print(f"❌ Even manually drawn pixels are wrong!")
        print("🚨 This indicates a SYSTEM-LEVEL issue!")
    
    return image

def main():
    """Run all black pixel tests"""
    
    print("🖤 PURE BLACK PIXEL VERIFICATION TEST")
    print("=" * 50)
    
    create_raw_black_pixels()
    print()
    create_matplotlib_black_shapes()
    print()
    create_text_bitmap()
    
    print("\n" + "=" * 50)
    print("🖤 BLACK PIXEL TESTS COMPLETE!")
    print("\nFiles created:")
    print("• RAW_BLACK_PIXELS.png - Raw numpy black pixels")
    print("• MATPLOTLIB_BLACK_SHAPES.png - Black shapes")
    print("• TEXT_BITMAP.png - Manually drawn black letters")
    
    print("\n🔍 ANALYSIS:")
    print("If even RAW_BLACK_PIXELS.png appears light,")
    print("there is a FUNDAMENTAL system/display issue.")
    print("The problem is NOT in Python/PIL/matplotlib.")
    
    print("\n💡 SOLUTION:")
    print("1. Try viewing files in different applications")
    print("2. Check Windows color management settings")
    print("3. Try on a different computer/monitor")
    print("4. Check graphics driver color settings")
    print("=" * 50)

if __name__ == "__main__":
    main()
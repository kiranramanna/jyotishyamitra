#!/usr/bin/env python3
"""
Enhanced South Indian Chart SVG Generator
==========================================

Creates a proper South Indian (4x4) horoscope chart SVG with:
- FIXED zodiac sign positions in 4x4 grid (as per traditional South Indian format)
- 360-degree nakshatra pada ruler around the perimeter  
- Color-coded nakshatra blocks (4 padas per block)
- Planetary tick marks at exact nirayana longitudes
- Proper planet placement by zodiac sign (not house)
- All nuanced details matching the reference samples

Key Mapping (FIXED - never changes):
- (0,0) Pisces   (0,1) Aries*   (0,2) Taurus   (0,3) Gemini
- (1,0) Aquarius [   CENTER      BLOCK    ]    (1,3) Cancer
- (2,0) Capricorn[    CHART      INFO     ]    (2,3) Leo  
- (3,0) Sagitt.  (3,1) Scorpio  (3,2) Libra   (3,3) Virgo

*0° starts at top-left corner of Aries cell (0,1)

Usage:
    python enhanced_south_indian_chart.py <json_file>
"""

import json
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Configuration constants
CANVAS_SIZE = 800
MARGIN = 50
GRID_SIZE = CANVAS_SIZE - 2 * MARGIN
CELL_SIZE = GRID_SIZE // 4
CENTER_X = CANVAS_SIZE // 2
CENTER_Y = CANVAS_SIZE // 2

# Label options: 'western', 'vedic', 'symbol'
LABEL_OPTIONS = "vedic"  # Change this to switch between modes

# Divisional chart selection: 'D1', 'D2', 'D3', etc.
DIVISIONAL_CHART = "D1"  # Default to D1 (Rashi chart)

# Font sizes
HOUSE_FONT_SIZE = 14
PLANET_FONT_SIZE = 14
DEGREE_FONT_SIZE = 11
TICK_FONT_SIZE = 10
TITLE_FONT_SIZE = 18

# Ruler dimensions
RULER_WIDTH = 15
RULER_INNER_RADIUS = GRID_SIZE // 2 + 5
RULER_OUTER_RADIUS = RULER_INNER_RADIUS + RULER_WIDTH

# FIXED zodiac sign positions in the 4x4 grid (this never changes)
SIGN_POSITIONS = {
    1: (0, 1),   # Aries - cell (0,1) 
    2: (0, 2),   # Taurus - cell (0,2)
    3: (0, 3),   # Gemini - cell (0,3)
    4: (1, 3),   # Cancer - cell (1,3)
    5: (2, 3),   # Leo - cell (2,3)
    6: (3, 3),   # Virgo - cell (3,3)
    7: (3, 2),   # Libra - cell (3,2)
    8: (3, 1),   # Scorpio - cell (3,1)
    9: (3, 0),   # Sagittarius - cell (3,0)
    10: (2, 0),  # Capricorn - cell (2,0)
    11: (1, 0),  # Aquarius - cell (1,0)
    12: (0, 0)   # Pisces - cell (0,0)
}

# Sign names - Western
SIGN_NAMES_WESTERN = {
    1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
    5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio", 
    9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces"
}

# Sign names - Vedic
SIGN_NAMES_VEDIC = {
    1: "Mesha", 2: "Vrishabha", 3: "Mithuna", 4: "Karka",
    5: "Simha", 6: "Kanya", 7: "Thula", 8: "Vrischika",
    9: "Dhanus", 10: "Makara", 11: "Kumbha", 12: "Meena"
}

# Zodiac symbols
ZODIAC_SYMBOLS = {
    1: "♈", 2: "♉", 3: "♊", 4: "♋",
    5: "♌", 6: "♍", 7: "♎", 8: "♏",
    9: "♐", 10: "♑", 11: "♒", 12: "♓"
}

# Colors for zodiac signs - Modern balanced tones for better readability
ZODIAC_COLORS = {
    1: "#FFB3BA",   # Aries - Light coral (blood red inspired)
    2: "#E6E6FA",   # Taurus - Light lavender (white with more presence)
    3: "#C1FFC1",   # Gemini - Pale green (more visible green)
    4: "#FFB6C1",   # Cancer - Light pink (more vibrant)
    5: "#DDA0DD",   # Leo - Plum (violet inspired, more depth)
    6: "#F5F5F5",   # Virgo - White smoke (clear but with substance)
    7: "#B0E0E6",   # Libra - Powder blue (more defined blue)
    8: "#FFDAB9",   # Scorpio - Peach puff (orange inspired, warmer)
    9: "#F0E68C",   # Sagittarius - Khaki (yellow with more body)
    10: "#D2B48C",  # Capricorn - Tan (variegated, earthier)
    11: "#DEB887",  # Aquarius - Burlywood (brown inspired, richer)
    12: "#D3D3D3"   # Pisces - Light gray (black inspired, more present)
}

# Planet colors (matching the sample charts)
PLANET_COLORS = {
    "Sun": "#FF0000",       # Red
    "Moon": "#00FFFF",      # Cyan
    "Mars": "#FF00FF",      # Magenta
    "Mercury": "#00FF00",   # Green
    "Jupiter": "#FFA500",   # Orange
    "Venus": "#808080",     # Gray
    "Saturn": "#000080",    # Deep blue
    "Rahu": "#800000",      # Maroon
    "Ketu": "#000000"       # Black
}

# Planet symbols - Western
PLANET_SYMBOLS_WESTERN = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", 
    "Rahu": "Ra", "Ketu": "Ke"
}

# Planet symbols - Vedic
PLANET_SYMBOLS_VEDIC = {
    "Sun": "Su", "Moon": "Ch", "Mars": "Ma", "Mercury": "Bu",
    "Jupiter": "Gu", "Venus": "Sk", "Saturn": "Sa", 
    "Rahu": "Ra", "Ketu": "Ke"
}

# Planet symbols - Pure symbols
PLANET_SYMBOLS_PURE = {
    "Sun": "☉", "Moon": "☽", "Mars": "♂", "Mercury": "☿",
    "Jupiter": "♃", "Venus": "♀", "Saturn": "♄", 
    "Rahu": "☊", "Ketu": "☋"
}

# Nakshatra colors - Modern balanced tones for better readability
NAKSHATRA_COLORS = [
    "#FFB3BA",  # 1. Ashwini - light coral (blood red inspired)
    "#FF6B6B",  # 2. Bharani - soft red (deep red inspired)
    "#F5F5F5",  # 3. Krittika - white smoke (white)
    "#F0F0F0",  # 4. Rohini - light gray (white)
    "#C0C0C0",  # 5. Mrigashira - silver (unchanged - already balanced)
    "#90EE90",  # 6. Ardra - light green (green inspired)
    "#9090AA",  # 7. Punarvasu - blue gray (lead inspired)
    "#CD5C5C",  # 8. Pushya - indian red (black red inspired)
    "#CD5C5C",  # 9. Ashlesha - indian red (black red inspired)
    "#FFFACD",  # 10. Magha - lemon chiffon (ivory/cream)
    "#D2B48C",  # 11. Purva Phalguni - tan (light brown - unchanged)
    "#87CEEB",  # 12. Uttara Phalguni - sky blue (bright blue balanced)
    "#66CDAA",  # 13. Hasta - medium aquamarine (deep green balanced)
    "#808080",  # 14. Chitra - gray (black balanced)
    "#696969",  # 15. Swati - dim gray (black balanced)
    "#FFD700",  # 16. Vishakha - gold (unchanged - already balanced)
    "#CD853F",  # 17. Anuradha - peru (red brown balanced)
    "#F5F5DC",  # 18. Jyeshta - beige (cream - unchanged)
    "#FFFFE0",  # 19. Mula - light yellow (bright yellow balanced)
    "#696969",  # 20. Purva Ashadha - dim gray (black balanced)
    "#B87333",  # 21. Uttara Ashadha - copper (unchanged - already balanced)
    "#ADD8E6",  # 22. Sravana - light blue (unchanged - already balanced)
    "#A9A9A9",  # 23. Dhanishtha - dark gray (silver grey - unchanged)
    "#20B2AA",  # 24. Shatabhisha - light sea green (blue green - unchanged)
    "#A9A9A9",  # 25. Purva Bhadra - dark gray (silver grey - unchanged)
    "#DA70D6",  # 26. Uttara Bhadra - orchid (purple balanced)
    "#DEB887"   # 27. Revati - burlywood (brown balanced)
]

# Use nakshatra colors for pada blocks (each nakshatra has 4 padas)
PADA_COLORS = NAKSHATRA_COLORS


def get_sign_label(sign_num):
    """Get the appropriate sign label based on the current label mode."""
    if LABEL_OPTIONS == "western":
        sign_name = SIGN_NAMES_WESTERN[sign_num][:3]  # Abbreviated
        symbol = ZODIAC_SYMBOLS[sign_num]
        return f"{symbol}{sign_name}"
    elif LABEL_OPTIONS == "vedic":
        sign_name = SIGN_NAMES_VEDIC[sign_num][:3]  # Abbreviated
        symbol = ZODIAC_SYMBOLS[sign_num]
        return f"{symbol}{sign_name}"
    elif LABEL_OPTIONS == "symbol":
        return ZODIAC_SYMBOLS[sign_num]
    else:
        # Default to vedic
        sign_name = SIGN_NAMES_VEDIC[sign_num][:3]
        symbol = ZODIAC_SYMBOLS[sign_num]
        return f"{symbol}{sign_name}"

def get_planet_symbol(planet_name):
    """Get the appropriate planet symbol based on the current label mode."""
    if LABEL_OPTIONS == "western":
        return PLANET_SYMBOLS_WESTERN.get(planet_name, planet_name[:2])
    elif LABEL_OPTIONS == "vedic":
        return PLANET_SYMBOLS_VEDIC.get(planet_name, planet_name[:2])
    elif LABEL_OPTIONS == "symbol":
        return PLANET_SYMBOLS_PURE.get(planet_name, planet_name[:1])
    else:
        # Default to vedic
        return PLANET_SYMBOLS_VEDIC.get(planet_name, planet_name[:2])

def longitude_to_sign_number(longitude):
    """Convert nirayana longitude to zodiac sign number (1-12)."""
    # Each sign spans 30 degrees
    # 0-30 = Aries (1), 30-60 = Taurus (2), etc.
    sign_num = int(longitude // 30) + 1
    if sign_num > 12:
        sign_num = sign_num % 12
    if sign_num == 0:
        sign_num = 12
    return sign_num

def get_degree_in_sign(longitude):
    """Get the degree within the sign (0-30)."""
    return longitude % 30

def calculate_ascendant_sign(chart_data):
    """Calculate which zodiac sign the ascendant is in."""
    asc_longitude = chart_data[DIVISIONAL_CHART]['ascendant']['nirayana_long']
    return longitude_to_sign_number(asc_longitude)

def calculate_house_to_sign_mapping(ascendant_sign):
    """Calculate which zodiac sign each house falls in."""
    house_to_sign = {}
    for house in range(1, 13):
        sign = ((ascendant_sign - 1 + house - 1) % 12) + 1
        house_to_sign[house] = sign
    return house_to_sign

def create_svg_root():
    """Create the root SVG element with proper dimensions."""
    root = Element('svg', {
        'width': str(CANVAS_SIZE),
        'height': str(CANVAS_SIZE),
        'xmlns': 'http://www.w3.org/2000/svg',
        'viewBox': f'0 0 {CANVAS_SIZE} {CANVAS_SIZE}'
    })
    return root

def add_styles(root):
    """Add CSS styles to the SVG."""
    defs = SubElement(root, 'defs')
    style = SubElement(defs, 'style')
    style.text = """
        .house-number { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; fill: #333; }
        .planet-symbol { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; text-anchor: middle; }
        .degree-label { font-family: Arial, sans-serif; font-size: 11px; text-anchor: middle; fill: black; }
        .tick-label { font-family: Arial, sans-serif; font-size: 10px; font-weight: bold; text-anchor: middle; fill: black; }
        .title { font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; fill: black; }
        .chart-info { font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; fill: red; }
        .sign-label { font-family: Arial, sans-serif; font-size: 10px; text-anchor: start; fill: #666; font-weight: bold; }
    """

def add_background(root):
    """Add white background to the SVG."""
    SubElement(root, 'rect', {
        'x': '0', 'y': '0', 
        'width': str(CANVAS_SIZE), 'height': str(CANVAS_SIZE),
        'fill': 'white'
    })

def add_pada_ruler_around_perimeter(root):
    """Add the 360-degree nakshatra pada ruler starting from 0° Aries."""
    # Each pada = 3°20' = 3.333 degrees, 108 padas total
    pada_degrees = 360 / 108
    
    # Grid bounds
    grid_left = MARGIN
    grid_top = MARGIN  
    grid_right = MARGIN + GRID_SIZE
    grid_bottom = MARGIN + GRID_SIZE
    
    # Calculate the perimeter length for each edge
    grid_width = GRID_SIZE
    grid_height = GRID_SIZE
    
    # The 0° point starts at top-left corner of Aries cell (0,1)
    # This is at x = grid_left + CELL_SIZE, y = grid_top
    aries_start_x = grid_left + CELL_SIZE
    
    # Create pada blocks starting from 0° Aries
    for pada_idx in range(108):
        pada_start_deg = pada_idx * pada_degrees
        pada_end_deg = (pada_idx + 1) * pada_degrees
        
        # Use a rotating color scheme (Ashwini starts at pada_idx = 0)
        nakshatra_idx = pada_idx // 4
        
        # Use the traditional nakshatra color (no variations)
        color = PADA_COLORS[nakshatra_idx % len(PADA_COLORS)]
        
        # Draw pada block on the appropriate edge starting from 0° Aries
        draw_pada_block_from_aries(root, pada_start_deg, pada_end_deg, color, 
                                 grid_left, grid_top, grid_right, grid_bottom, aries_start_x)
        
        # Add nakshatra boundary line at the end of each nakshatra (every 4th pada)
        if (pada_idx + 1) % 4 == 0:
            draw_nakshatra_boundary_line(root, pada_end_deg, grid_left, grid_top, grid_right, grid_bottom, aries_start_x)

def draw_pada_block_from_aries(root, start_deg, end_deg, color, grid_left, grid_top, grid_right, grid_bottom, aries_start_x):
    """Draw a single pada block starting from 0° Aries position with exact corner boundaries."""
    grid_width = grid_right - grid_left
    grid_height = grid_bottom - grid_top
    
    # Use consistent thin stroke for all pada blocks
    stroke_width = "0.5"
    
    # Define exact corner positions
    # 0° = Aries top-left corner (aries_start_x, grid_top)
    # 90° = Cancer top-right corner (grid_right, grid_top + CELL_SIZE)  
    # 180° = Libra bottom-right corner (grid_right - CELL_SIZE, grid_bottom)
    # 270° = Capricorn bottom-left corner (grid_left, grid_bottom - CELL_SIZE)
    
    cancer_corner_x = grid_right
    cancer_corner_y = grid_top + CELL_SIZE
    
    libra_corner_x = grid_right - CELL_SIZE  
    libra_corner_y = grid_bottom
    
    capricorn_corner_x = grid_left
    capricorn_corner_y = grid_bottom - CELL_SIZE
    
    if start_deg <= 90 and end_deg <= 90:
        # Top edge: from Aries corner (0°) to Cancer corner (90°) only
        # 0° at aries_start_x, 90° at grid_right  
        available_width = grid_right - aries_start_x
        block_start_x = aries_start_x + (start_deg / 90) * available_width
        block_end_x = aries_start_x + (end_deg / 90) * available_width
        SubElement(root, 'rect', {
            'x': str(block_start_x), 'y': str(grid_top - RULER_WIDTH),
            'width': str(block_end_x - block_start_x), 'height': str(RULER_WIDTH),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
    elif start_deg <= 180 and end_deg <= 180 and start_deg >= 90:
        # Right edge: from Cancer corner (90°) to Libra corner (180°) only
        # Map degrees 90-180 to the segment from Cancer corner to Libra corner
        available_height = libra_corner_y - cancer_corner_y
        block_start_y = cancer_corner_y + ((start_deg - 90) / 90) * available_height
        block_end_y = cancer_corner_y + ((end_deg - 90) / 90) * available_height
        SubElement(root, 'rect', {
            'x': str(grid_right), 'y': str(block_start_y),
            'width': str(RULER_WIDTH), 'height': str(block_end_y - block_start_y),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
    elif start_deg <= 270 and end_deg <= 270 and start_deg >= 180:
        # Bottom edge: from Libra corner (180°) to Capricorn corner (270°) only
        # Map degrees 180-270 to the segment from Libra corner to Capricorn corner
        available_width = libra_corner_x - capricorn_corner_x
        block_start_x = libra_corner_x - ((start_deg - 180) / 90) * available_width
        block_end_x = libra_corner_x - ((end_deg - 180) / 90) * available_width
        SubElement(root, 'rect', {
            'x': str(block_end_x), 'y': str(grid_bottom),
            'width': str(block_start_x - block_end_x), 'height': str(RULER_WIDTH),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
    elif start_deg >= 270:
        # Left edge: from Capricorn corner (270°) back toward Aries corner (360°/0°) only
        # Map degrees 270-360 to the segment from Capricorn corner to Aries corner
        available_height = capricorn_corner_y - grid_top
        block_start_y = capricorn_corner_y - ((start_deg - 270) / 90) * available_height
        block_end_y = capricorn_corner_y - ((end_deg - 270) / 90) * available_height
        SubElement(root, 'rect', {
            'x': str(grid_left - RULER_WIDTH), 'y': str(block_end_y),
            'width': str(RULER_WIDTH), 'height': str(block_start_y - block_end_y),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
    # Handle edge cases where pada spans across corners
    elif start_deg < 90 < end_deg:
        # Spans from top edge to right edge at Cancer corner
        # Top part: from start to Cancer corner (90°)
        available_width = grid_right - aries_start_x
        block_start_x = aries_start_x + (start_deg / 90) * available_width
        SubElement(root, 'rect', {
            'x': str(block_start_x), 'y': str(grid_top - RULER_WIDTH),
            'width': str(grid_right - block_start_x), 'height': str(RULER_WIDTH),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
        # Right part: from Cancer corner to end
        available_height = libra_corner_y - cancer_corner_y
        block_end_y = cancer_corner_y + ((end_deg - 90) / 90) * available_height
        SubElement(root, 'rect', {
            'x': str(grid_right), 'y': str(cancer_corner_y),
            'width': str(RULER_WIDTH), 'height': str(block_end_y - cancer_corner_y),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
    elif start_deg < 180 < end_deg:
        # Spans from right edge to bottom edge at Libra corner
        # Right part: from start to Libra corner (180°)
        available_height = libra_corner_y - cancer_corner_y
        block_start_y = cancer_corner_y + ((start_deg - 90) / 90) * available_height
        SubElement(root, 'rect', {
            'x': str(grid_right), 'y': str(block_start_y),
            'width': str(RULER_WIDTH), 'height': str(libra_corner_y - block_start_y),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
        # Bottom part: from Libra corner to end
        available_width = libra_corner_x - capricorn_corner_x
        block_end_x = libra_corner_x - ((end_deg - 180) / 90) * available_width
        SubElement(root, 'rect', {
            'x': str(block_end_x), 'y': str(grid_bottom),
            'width': str(libra_corner_x - block_end_x), 'height': str(RULER_WIDTH),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
    elif start_deg < 270 < end_deg:
        # Spans from bottom edge to left edge at Capricorn corner
        # Bottom part: from start to Capricorn corner (270°)
        available_width = libra_corner_x - capricorn_corner_x
        block_start_x = libra_corner_x - ((start_deg - 180) / 90) * available_width
        SubElement(root, 'rect', {
            'x': str(capricorn_corner_x), 'y': str(grid_bottom),
            'width': str(block_start_x - capricorn_corner_x), 'height': str(RULER_WIDTH),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })
        # Left part: from Capricorn corner to end
        available_height = capricorn_corner_y - grid_top
        block_end_y = capricorn_corner_y - ((end_deg - 270) / 90) * available_height
        SubElement(root, 'rect', {
            'x': str(grid_left - RULER_WIDTH), 'y': str(block_end_y),
            'width': str(RULER_WIDTH), 'height': str(capricorn_corner_y - block_end_y),
            'fill': color, 'stroke': '#333333', 'stroke-width': stroke_width
        })

def draw_nakshatra_boundary_line(root, degree, grid_left, grid_top, grid_right, grid_bottom, aries_start_x):
    """Draw a strong boundary line at nakshatra boundaries."""
    # Define exact corner positions matching the pada ruler
    cancer_corner_x = grid_right
    cancer_corner_y = grid_top + CELL_SIZE
    libra_corner_x = grid_right - CELL_SIZE
    libra_corner_y = grid_bottom
    capricorn_corner_x = grid_left
    capricorn_corner_y = grid_bottom - CELL_SIZE
    
    # Calculate position on perimeter based on degree
    if degree <= 90:
        # Top edge: from Aries corner to Cancer corner
        available_width = cancer_corner_x - aries_start_x
        x = aries_start_x + (degree / 90) * available_width
        SubElement(root, 'line', {
            'x1': str(x), 'y1': str(grid_top - RULER_WIDTH),
            'x2': str(x), 'y2': str(grid_top),
            'stroke': '#000000', 'stroke-width': '2'
        })
    elif degree <= 180:
        # Right edge: from Cancer corner to Libra corner
        available_height = libra_corner_y - cancer_corner_y
        y = cancer_corner_y + ((degree - 90) / 90) * available_height
        SubElement(root, 'line', {
            'x1': str(grid_right), 'y1': str(y),
            'x2': str(grid_right + RULER_WIDTH), 'y2': str(y),
            'stroke': '#000000', 'stroke-width': '2'
        })
    elif degree <= 270:
        # Bottom edge: from Libra corner to Capricorn corner
        available_width = libra_corner_x - capricorn_corner_x
        x = libra_corner_x - ((degree - 180) / 90) * available_width
        SubElement(root, 'line', {
            'x1': str(x), 'y1': str(grid_bottom),
            'x2': str(x), 'y2': str(grid_bottom + RULER_WIDTH),
            'stroke': '#000000', 'stroke-width': '2'
        })
    else:
        # Left edge: from Capricorn corner back toward Aries corner
        available_height = capricorn_corner_y - grid_top
        y = capricorn_corner_y - ((degree - 270) / 90) * available_height
        SubElement(root, 'line', {
            'x1': str(grid_left - RULER_WIDTH), 'y1': str(y),
            'x2': str(grid_left), 'y2': str(y),
            'stroke': '#000000', 'stroke-width': '2'
        })

def add_major_degree_markers(root):
    """Add major degree markers (0°, 90°, 180°, 270°) at exact corner positions."""
    grid_left = MARGIN
    grid_top = MARGIN
    grid_right = MARGIN + GRID_SIZE
    grid_bottom = MARGIN + GRID_SIZE
    
    # Use exact corner positions matching the pada ruler
    # 0° = Aries top-left corner (grid_left + CELL_SIZE, grid_top)
    aries_x = grid_left + CELL_SIZE
    aries_y = grid_top
    
    # 90° = Cancer top-right corner (grid_right, grid_top + CELL_SIZE)
    cancer_x = grid_right
    cancer_y = grid_top + CELL_SIZE
    
    # 180° = Libra bottom-right corner (grid_right - CELL_SIZE, grid_bottom)
    libra_x = grid_right - CELL_SIZE
    libra_y = grid_bottom
    
    # 270° = Capricorn bottom-left corner (grid_left, grid_bottom - CELL_SIZE)
    capricorn_x = grid_left
    capricorn_y = grid_bottom - CELL_SIZE
    
    # 360° = top-left corner of Pisces cell (0,0) - where the circle completes
    pisces_x = grid_left
    pisces_y = grid_top
    
    markers = [
        (0, aries_x, aries_y - RULER_WIDTH - 5),
        (90, cancer_x + RULER_WIDTH + 5, cancer_y),  
        (180, libra_x, libra_y + RULER_WIDTH + 15),
        (270, capricorn_x - RULER_WIDTH - 5, capricorn_y),
        (360, pisces_x - RULER_WIDTH - 5, pisces_y - RULER_WIDTH - 5)
    ]
    
    for degree, x, y in markers:
        SubElement(root, 'text', {
            'x': str(x), 'y': str(y), 'class': 'tick-label'
        }).text = f"{degree}°"

def add_zodiac_squares(root, chart_data):
    """Add zodiac sign squares with colors, house numbers, and sign labels."""
    # Calculate house-to-sign mapping based on ascendant
    ascendant_sign = calculate_ascendant_sign(chart_data)
    house_to_sign = calculate_house_to_sign_mapping(ascendant_sign)
    
    # Reverse mapping: sign to house  
    sign_to_house = {v: k for k, v in house_to_sign.items()}
    
    # Draw each zodiac sign square
    for sign_num in range(1, 13):
        row, col = SIGN_POSITIONS[sign_num]
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        
        # Skip center cells
        if (row, col) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
            continue
            
        # Add colored square
        SubElement(root, 'rect', {
            'x': str(x), 'y': str(y),
            'width': str(CELL_SIZE), 'height': str(CELL_SIZE),
            'fill': ZODIAC_COLORS.get(sign_num, '#FFFFFF'),
            'stroke': 'black', 'stroke-width': '2'
        })
        
        # Add house number
        house_num = sign_to_house.get(sign_num, "")
        SubElement(root, 'text', {
            'x': str(x + 10), 'y': str(y + 20), 'class': 'house-number'
        }).text = str(house_num)
        
        # Add sign name with symbol - positioned to stay within cell
        sign_label = get_sign_label(sign_num)
        SubElement(root, 'text', {
            'x': str(x + CELL_SIZE - 40), 'y': str(y + 20), 'class': 'sign-label'
        }).text = sign_label

def add_planetary_tick_marks(root, chart_data):
    """Add planetary tick marks on the pada ruler at exact longitudes using exact corner boundaries."""
    planets = chart_data[DIVISIONAL_CHART]['planets']
    
    grid_left = MARGIN
    grid_top = MARGIN
    grid_right = MARGIN + GRID_SIZE
    grid_bottom = MARGIN + GRID_SIZE
    
    # Define exact corner positions matching the pada ruler
    aries_start_x = grid_left + CELL_SIZE
    cancer_corner_x = grid_right
    cancer_corner_y = grid_top + CELL_SIZE
    libra_corner_x = grid_right - CELL_SIZE
    libra_corner_y = grid_bottom
    capricorn_corner_x = grid_left
    capricorn_corner_y = grid_bottom - CELL_SIZE
    
    for planet_name, planet_data in planets.items():
        longitude = planet_data['nirayana_long']
        color = PLANET_COLORS.get(planet_name, '#000000')
        
        # Calculate position on perimeter based on longitude starting from Aries
        degree = longitude % 360
        
        # Calculate tick position using exact corner boundaries
        tick_x1 = tick_y1 = tick_x2 = tick_y2 = 0
        label_x = label_y = 0
        
        if degree <= 90:
            # Top edge: from Aries corner to Cancer corner
            available_width = cancer_corner_x - aries_start_x
            x = aries_start_x + (degree / 90) * available_width
            tick_x1 = tick_x2 = x
            tick_y1 = grid_top - RULER_WIDTH - 2
            tick_y2 = grid_top - RULER_WIDTH - 8
            label_x = x
            label_y = grid_top - RULER_WIDTH - 12
        elif degree <= 180:
            # Right edge: from Cancer corner to Libra corner
            available_height = libra_corner_y - cancer_corner_y
            y = cancer_corner_y + ((degree - 90) / 90) * available_height
            tick_x1 = grid_right + RULER_WIDTH + 2
            tick_x2 = grid_right + RULER_WIDTH + 8
            tick_y1 = tick_y2 = y
            label_x = grid_right + RULER_WIDTH + 15
            label_y = y + 3
        elif degree <= 270:
            # Bottom edge: from Libra corner to Capricorn corner
            available_width = libra_corner_x - capricorn_corner_x
            x = libra_corner_x - ((degree - 180) / 90) * available_width
            tick_x1 = tick_x2 = x
            tick_y1 = grid_bottom + RULER_WIDTH + 2
            tick_y2 = grid_bottom + RULER_WIDTH + 8
            label_x = x
            label_y = grid_bottom + RULER_WIDTH + 18
        else:
            # Left edge: from Capricorn corner back toward Aries corner
            available_height = capricorn_corner_y - grid_top
            y = capricorn_corner_y - ((degree - 270) / 90) * available_height
            tick_x1 = grid_left - RULER_WIDTH - 2
            tick_x2 = grid_left - RULER_WIDTH - 8
            tick_y1 = tick_y2 = y
            label_x = grid_left - RULER_WIDTH - 15
            label_y = y + 3
        
        # Draw planetary tick mark
        SubElement(root, 'line', {
            'x1': str(tick_x1), 'y1': str(tick_y1),
            'x2': str(tick_x2), 'y2': str(tick_y2),
            'stroke': color, 'stroke-width': '2'
        })
        
        # Add planet label
        symbol = get_planet_symbol(planet_name)
        SubElement(root, 'text', {
            'x': str(label_x), 'y': str(label_y),
            'font-family': 'Arial, sans-serif', 'font-size': '9',
            'font-weight': 'bold', 'text-anchor': 'middle', 'fill': color
        }).text = symbol

def add_planets_to_signs(root, chart_data):
    """Add planets to their zodiac sign positions based on nirayana longitude."""
    planets = chart_data[DIVISIONAL_CHART]['planets']
    
    # Group planets by zodiac sign
    sign_planets = {}
    for planet_name, planet_data in planets.items():
        longitude = planet_data['nirayana_long']
        sign_num = longitude_to_sign_number(longitude)
        
        if sign_num not in sign_planets:
            sign_planets[sign_num] = []
        sign_planets[sign_num].append({
            'name': planet_name,
            'data': planet_data
        })
    
    # Place planets in their sign cells
    for sign_num, planet_list in sign_planets.items():
        row, col = SIGN_POSITIONS[sign_num]
        
        # Skip center cells
        if (row, col) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
            continue
            
        base_x = MARGIN + col * CELL_SIZE
        base_y = MARGIN + row * CELL_SIZE
        
        # Position multiple planets in the same sign
        planet_count = len(planet_list)
        for i, planet_info in enumerate(planet_list):
            planet_name = planet_info['name']
            planet_data = planet_info['data']
            
            # Calculate position within cell
            if planet_count == 1:
                x = base_x + CELL_SIZE // 2
                y = base_y + CELL_SIZE // 2 + 5
            else:
                # Space multiple planets
                if planet_count <= 3:
                    x = base_x + 30 + (i * 40)
                    y = base_y + CELL_SIZE // 2 + 5
                else:
                    # More than 3 planets - use rows
                    x = base_x + 30 + ((i % 3) * 40)
                    y = base_y + 40 + ((i // 3) * 25)
            
            # Get planet color
            color = PLANET_COLORS.get(planet_name, '#000000')
            
            # Add planet symbol
            symbol = get_planet_symbol(planet_name)
            SubElement(root, 'text', {
                'x': str(x), 'y': str(y),
                'class': 'planet-symbol', 'fill': color
            }).text = symbol
            
            # Add degree label
            degree_in_sign = get_degree_in_sign(planet_data['nirayana_long'])
            SubElement(root, 'text', {
                'x': str(x), 'y': str(y + 12),
                'class': 'degree-label'
            }).text = f"{degree_in_sign:.0f}°{int((degree_in_sign % 1) * 60):02d}'"

def add_chart_title_and_info(root, chart_data):
    """Add chart title and birth information in center."""
    user_details = chart_data.get('user_details', {})
    name = user_details.get('name', 'Birth Chart')
    
    # Center info block (no title at top anymore)
    center_y = CENTER_Y - 60
    
    # Add name and divisional chart to center info area
    chart_name = chart_data.get(DIVISIONAL_CHART, {}).get('name', DIVISIONAL_CHART)
    title_text = f"{name} ({DIVISIONAL_CHART}-{chart_name})"
    SubElement(root, 'text', {
        'x': str(CENTER_X), 'y': str(center_y),
        'class': 'title'
    }).text = title_text
    
    # Birth details
    birth_details = user_details.get('birthdetails', {})
    if birth_details:
        dob = birth_details.get('DOB', {})
        tob = birth_details.get('TOB', {})
        pob = birth_details.get('POB', {})
        gender = birth_details.get('Gender', '')
        
        date_str = f"{dob.get('day', '')}-{dob.get('month', '')}-{dob.get('year', '')}"
        time_str = f"{tob.get('hour', '')}:{tob.get('min', '')}:{tob.get('sec', '')}"
        place_str = pob.get('name', '')
        timezone = pob.get('timezone', '')
        
        # Add timezone to date/time if available
        datetime_str = f"{date_str} {time_str}"
        if timezone:
            datetime_str += f" (UTC+{timezone})"
        
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(center_y + 25),
            'class': 'chart-info'
        }).text = datetime_str
        
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(center_y + 40),
            'class': 'chart-info'
        }).text = place_str
        
        # Add gender if available and not empty
        if gender and gender.strip():
            SubElement(root, 'text', {
                'x': str(CENTER_X), 'y': str(center_y + 55),
                'class': 'chart-info'
            }).text = f"Gender: {gender.title()}"
    
    # Calculate panchanga starting position based on whether gender was displayed
    panchanga_y = center_y + 75
    if birth_details and birth_details.get('Gender', '').strip():
        panchanga_y = center_y + 75
    else:
        panchanga_y = center_y + 60  # Move up if no gender displayed
    
    # Maasa and Vaara
    maasa = user_details.get('maasa', '')
    vaara = user_details.get('vaara', '')
    if maasa and vaara:
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(panchanga_y),
            'font-family': 'Arial, sans-serif', 'font-size': '10',
            'text-anchor': 'middle', 'fill': 'green'
        }).text = f"{maasa} | {vaara}"
    
    # Tithi and Karana
    tithi = user_details.get('tithi', '')
    karana = user_details.get('karana', '')
    if tithi and karana:
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(panchanga_y + 12),
            'font-family': 'Arial, sans-serif', 'font-size': '10',
            'text-anchor': 'middle', 'fill': 'green'
        }).text = f"{tithi.title()} | {karana}"
    
    # Nakshatra and Yoga
    nakshatra = user_details.get('nakshatra', '')
    yoga = user_details.get('yoga', '')
    if nakshatra and yoga:
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(panchanga_y + 24),
            'font-family': 'Arial, sans-serif', 'font-size': '10',
            'text-anchor': 'middle', 'fill': 'green'
        }).text = f"{nakshatra} | {yoga}"
    
    # Moon Rashi
    rashi = user_details.get('rashi', '')
    if rashi:
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(panchanga_y + 36),
            'font-family': 'Arial, sans-serif', 'font-size': '10',
            'text-anchor': 'middle', 'fill': 'green'
        }).text = f"Moon: {rashi}"
        
    # Ascendant info
    if 'ascendant' in chart_data[DIVISIONAL_CHART]:
        asc_data = chart_data[DIVISIONAL_CHART]['ascendant']
        asc_degree = get_degree_in_sign(asc_data['nirayana_long'])
        asc_sign = asc_data['sign']
        
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(panchanga_y + 50),
            'font-family': 'Arial, sans-serif', 'font-size': '11',
            'text-anchor': 'middle', 'fill': 'blue'
        }).text = f"Ayanamsa: Lahiri"
        
        SubElement(root, 'text', {
            'x': str(CENTER_X), 'y': str(panchanga_y + 65),
            'font-family': 'Arial, sans-serif', 'font-size': '11',
            'text-anchor': 'middle', 'fill': 'blue'
        }).text = f"ASC {asc_degree:.0f}°{int((asc_degree % 1) * 60):02d}' {asc_sign}"

def generate_enhanced_south_indian_chart(chart_data):
    """Generate the complete enhanced South Indian chart."""
    root = create_svg_root()
    
    # Add styles
    add_styles(root)
    
    # Add background
    add_background(root)
    
    # Add chart title and info
    add_chart_title_and_info(root, chart_data)
    
    # Add zodiac squares with house numbers
    add_zodiac_squares(root, chart_data)
    
    # Add the enhanced pada ruler
    add_pada_ruler_around_perimeter(root)
    
    # Add major degree markers
    add_major_degree_markers(root)
    
    # Add planetary tick marks on ruler
    add_planetary_tick_marks(root, chart_data)
    
    # Add planets to their zodiac sign positions
    add_planets_to_signs(root, chart_data)
    
    return root

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, 'unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')

def main():
    """Main function to handle command line arguments and generate SVG."""
    global DIVISIONAL_CHART
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python enhanced_south_indian_chart.py <json_file> [divisional_chart]")
        print("Example: python enhanced_south_indian_chart.py ../chart_creator/swami_vivekananda_chart-d1.json")
        print("Example: python enhanced_south_indian_chart.py ../chart_creator/swami_vivekananda_chart-d1.json D2")
        print("Available divisional charts: D1 (default), D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60")
        sys.exit(1)
    
    json_file = Path(sys.argv[1])
    
    # Optional divisional chart argument
    if len(sys.argv) == 3:
        DIVISIONAL_CHART = sys.argv[2].upper()
        if not DIVISIONAL_CHART.startswith('D'):
            DIVISIONAL_CHART = f"D{DIVISIONAL_CHART}"
    if not json_file.exists():
        print(f"Error: JSON file '{json_file}' not found.")
        sys.exit(1)
    
    try:
        # Load chart data
        with open(json_file, 'r') as f:
            chart_data = json.load(f)
        
        # Validate divisional chart exists
        if DIVISIONAL_CHART not in chart_data:
            available_charts = [key for key in chart_data.keys() if key.startswith('D') and key[1:].isdigit()]
            print(f"Error: Divisional chart '{DIVISIONAL_CHART}' not found in the JSON file.")
            print(f"Available divisional charts in this file: {', '.join(available_charts)}")
            sys.exit(1)
        
        # Check if the divisional chart has required data
        if 'planets' not in chart_data[DIVISIONAL_CHART] or 'ascendant' not in chart_data[DIVISIONAL_CHART]:
            print(f"Error: Divisional chart '{DIVISIONAL_CHART}' is missing required 'planets' or 'ascendant' data.")
            sys.exit(1)
        
        # Generate enhanced SVG
        svg_root = generate_enhanced_south_indian_chart(chart_data)
        
        # Create output filename in the enhanced_chart folder
        divisional_suffix = f"_{DIVISIONAL_CHART.lower()}" if DIVISIONAL_CHART != "D1" else ""
        output_file = Path(__file__).parent / f"{json_file.stem}_enhanced_correct{divisional_suffix}.svg"
        
        # Save SVG
        svg_content = prettify_xml(svg_root)
        with open(output_file, 'w') as f:
            f.write(svg_content)
        
        print(f"Enhanced South Indian chart generated successfully: {output_file}")
        
        # Debug info
        print(f"Divisional Chart: {DIVISIONAL_CHART} ({chart_data[DIVISIONAL_CHART].get('name', DIVISIONAL_CHART)})")
        ascendant_sign = calculate_ascendant_sign(chart_data)
        sign_names = SIGN_NAMES_VEDIC if LABEL_OPTIONS == "vedic" else SIGN_NAMES_WESTERN
        print(f"Ascendant in: {sign_names[ascendant_sign]}")
        
        planets = chart_data[DIVISIONAL_CHART]['planets']
        for name, data in planets.items():
            longitude = data['nirayana_long']
            sign = longitude_to_sign_number(longitude)
            degree = get_degree_in_sign(longitude)
            print(f"{name}: {longitude:.1f}° → {sign_names[sign]} {degree:.1f}°")
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error generating chart: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
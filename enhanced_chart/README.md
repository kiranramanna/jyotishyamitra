# Enhanced South Indian Chart Generator

This folder contains the **correct implementation** of an enhanced South Indian (4×4) horoscope chart generator that follows the traditional Vedic astrology principles and the detailed specifications from the reference instructions.

## Key Features

### ✅ Correct Implementation Highlights

1. **Fixed Zodiac Sign Grid**: Uses the traditional South Indian format where zodiac signs have FIXED positions in the 4×4 grid:
   ```
   (0,0) Pisces   (0,1) Aries*   (0,2) Taurus   (0,3) Gemini
   (1,0) Aquarius [   CENTER      BLOCK    ]    (1,3) Cancer
   (2,0) Capricorn[    CHART      INFO     ]    (2,3) Leo  
   (3,0) Sagitt.  (3,1) Scorpio  (3,2) Libra   (3,3) Virgo
   ```
   *0° starts at top-left corner of Aries cell (0,1)

2. **360-Degree Nakshatra Pada Ruler**: 
   - Traditional color-coded blocks around the perimeter (27 nakshatra colors)
   - Each nakshatra contains 4 padas (108 total pada divisions)
   - Each pada = 3°20' (360° ÷ 108 = 3.333...)
   - **Visual Hierarchy**: Thin borders (0.5px) between padas, thick borders (1.5px) between nakshatras

3. **Traditional Nakshatra Colors**:
   - Authentic colors based on traditional Vedic descriptions
   - 27 distinct nakshatra colors (Ashwini=blood red, Bharani=deep red, Krittika=white, etc.)
   - No color variations within nakshatras - uses consistent traditional colors

4. **Correct Planet Placement**:
   - Planets placed by **zodiac sign** (based on nirayana longitude)
   - NOT by house number (common mistake in other implementations)
   - Example: Sun at 269.4° → Sagittarius (correct), not by house number

5. **Planetary Tick Marks**:
   - Exact longitude positions marked on the perimeter ruler
   - Color-coded by planet (Red=Sun, Cyan=Moon, Magenta=Mars, etc.)
   - Labels with planet symbols (Su, Mo, Ma, Me, Ju, Ve, Sa, Ra, Ke)

6. **House Numbers**:
   - Calculated correctly from ascendant position
   - Shows which house each zodiac sign represents
   - Example: If ascendant in Sagittarius → Sagittarius=1st house, Capricorn=2nd house, etc.

## Files

- `enhanced_south_indian_chart.py` - Main generator script
- `README.md` - This documentation

## Usage

```bash
python enhanced_south_indian_chart.py <json_file>
```

### Examples:
```bash
# Using JSON file from chart_creator folder
python enhanced_south_indian_chart.py ../chart_creator/swami_vivekananda_chart-d1.json

# Using JSON file from current folder
python enhanced_south_indian_chart.py swami_vivekananda_chart-di.json
```

### Configuration Options

#### Label Modes
Change the `LABEL_OPTIONS` variable in the script to switch between different labeling systems:

```python
# In enhanced_south_indian_chart.py line ~41
LABEL_OPTIONS = "vedic"  # Options: "western", "vedic", "symbol"
```

**Western Mode**: Traditional Western astrology names
- Zodiac: ♈Ari, ♉Tau, ♊Gem, ♋Can, ♌Leo, ♍Vir, ♎Lib, ♏Sco, ♐Sag, ♑Cap, ♒Aqu, ♓Pis
- Planets: Su, Mo, Ma, Me, Ju, Ve, Sa, Ra, Ke

**Vedic Mode**: Traditional Sanskrit names (Default)
- Zodiac: ♈Mes, ♉Vri, ♊Mit, ♋Kar, ♌Sim, ♍Kan, ♎Thu, ♏Vri, ♐Dha, ♑Mak, ♒Kum, ♓Mee
- Planets: Su, Ch, Ma, Bu, Gu, Sk, Sa, Ra, Ke

**Symbol Mode**: Pure symbols without text
- Zodiac: ♈, ♉, ♊, ♋, ♌, ♍, ♎, ♏, ♐, ♑, ♒, ♓
- Planets: ☉, ☽, ♂, ☿, ♃, ♀, ♄, ☊, ☋

## Output

Generates an SVG file with suffix `_enhanced_correct.svg` containing:

- **Zodiac squares** with modern balanced colors and zodiac symbols
- **House numbers** in each sign (calculated from ascendant)
- **Planet symbols** with degrees/minutes in appropriate labeling mode
- **360° pada ruler** with modern nakshatra colors and clean boundary lines
- **Planetary tick marks** at exact longitudes with color-coded symbols
- **Major degree markers** (0°, 90°, 180°, 270°, 360°)
- **Comprehensive user information** in center:
  - **Name** and **birth details** (date, time, place, timezone)
  - **Panchanga details** (Maasa, Vaara, Tithi, Karana, Nakshatra, Yoga)
  - **Moon sign** and **gender** (optional)
  - **Ayanamsa** and **ascendant** information

## Validation Example

For Swami Vivekananda's chart:
```
Ascendant in: Sagittarius
Sun: 269.4° → Sagittarius 29.4°  ← Correctly placed in Sagittarius
Moon: 167.5° → Virgo 17.5°
Mars: 6.3° → Aries 6.3°
Mercury: 281.8° → Capricorn 11.8°
Jupiter: 184.0° → Libra 4.0°
Venus: 277.1° → Capricorn 7.1°
Saturn: 163.6° → Virgo 13.6°
Rahu: 232.2° → Scorpio 22.2°
Ketu: 52.2° → Taurus 22.2°
```

## Technical Details

### Coordinate System
- Uses a 4×4 matrix with cells indexed as (row, column) from 0 to 3
- 0° Aries starts at top-left corner of cell (0,1)
- 90° Cancer at top-right corner of cell (1,3)
- 180° Libra at bottom-right corner of cell (3,2)
- 270° Capricorn at bottom-left corner of cell (2,0)
- 360° Pisces at top-left corner of cell (0,0) - circle completion marker

### Planet Colors
- Sun: Red (#FF0000)
- Moon: Cyan (#00FFFF)  
- Mars: Magenta (#FF00FF)
- Mercury: Green (#00FF00)
- Jupiter: Orange (#FFA500)
- Venus: Gray (#808080)
- Saturn: Deep Blue (#000080)
- Rahu: Maroon (#800000)
- Ketu: Black (#000000)

### Zodiac Colors (Modern Balanced)
```python
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
```

### Nakshatra Colors (Modern Balanced)
```python
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
```

### Nakshatra Boundary System
- **Uniform Pada Borders (0.5px)**: All pada blocks have consistent thin gray borders
- **Strong Boundary Lines (2px)**: Bold black lines mark the end of each nakshatra (every 4th pada)
- **Clean Visual Hierarchy**: Focus on major nakshatra divisions rather than individual pada emphasis
- **Professional Appearance**: No special treatment of individual padas, emphasis on astronomical boundaries

### Algorithm
1. Calculate ascendant zodiac sign from nirayana longitude
2. Map houses to zodiac signs (1st house = ascendant sign)
3. Place planets in zodiac sign cells (by nirayana longitude)
4. Draw pada ruler with 108 divisions around perimeter using traditional nakshatra colors
5. Apply border hierarchy (thin for padas, thick for nakshatra boundaries)
6. Add planetary tick marks at exact longitude positions
7. Display house numbers in appropriate sign cells
8. Add degree markers at cardinal points (0°, 90°, 180°, 270°, 360°)

## Recent Updates & Enhancements

### Latest Features (v3.0)
1. **Modern Color Palette**: 
   - **Zodiac Signs**: Updated to modern, balanced tones for better readability while maintaining traditional color themes
   - **Nakshatra Colors**: Refined with softer, professional tones that preserve visual distinction
   - Examples: Aries (Light Coral), Taurus (Light Lavender), Gemini (Pale Green), etc.

2. **Enhanced Nakshatra Boundary System**:
   - **Clean Boundary Lines**: Replaced thick pada borders with strong black boundary lines at nakshatra endings
   - **Professional Appearance**: No special emphasis on individual padas, focus on major nakshatra divisions
   - **2px Bold Lines**: Clear visual markers at every 4th pada (13°20' intervals)

3. **Zodiac Symbol Integration**:
   - **Symbol + Name Format**: Shows zodiac symbols with abbreviated names (e.g., ♈Mes, ♉Vri)
   - **Proper Positioning**: Symbols and names positioned within cell boundaries to prevent overlap
   - **Bold Text**: Enhanced readability with font-weight bold for sign labels

4. **Label Options System**: Three distinct labeling modes via `LABEL_OPTIONS` variable:
   - **Western Mode** (`"western"`): ♈Ari, ♉Tau, Planets: Su, Mo, Ma, Me, Ju, Ve, Sa, Ra, Ke
   - **Vedic Mode** (`"vedic"`): ♈Mes, ♉Vri, Planets: Su, Ch, Ma, Bu, Gu, Sk, Sa, Ra, Ke  
   - **Symbol Mode** (`"symbol"`): ♈, ♉, ♊ only, Planets: ☉, ☽, ♂, ☿, ♃, ♀, ♄, ☊, ☋

5. **Comprehensive User Details Display**:
   - **Complete Birth Information**: Date, time, place with timezone (UTC+5.88)
   - **Panchanga Details**: Maasa, Vaara, Tithi, Karana, Nakshatra, Yoga, Moon sign
   - **Optional Gender**: Robust handling of optional fields without breaking
   - **Color-Coded Information**: Red for birth details, Green for Panchanga, Blue for astrological calculations
   - **Center Layout**: All information consolidated in center area, title moved from top

6. **Enhanced Visual Design**:
   - **Clean Top Area**: Removed title from top for cleaner appearance
   - **Organized Information Hierarchy**: Logical flow from personal to spiritual/astrological details
   - **Improved Spacing**: Better vertical spacing between information groups
   - **Professional Typography**: Consistent font sizing and color coding

### Previous Evolution
- **v1.0**: Basic South Indian chart with correct zodiac sign placement
- **v1.1**: Added nakshatra pada ruler around perimeter  
- **v1.2**: Implemented traditional nakshatra color scheme
- **v1.3**: Added border hierarchy for visual distinction between nakshatras and padas
- **v2.0**: Traditional colors and visual hierarchy borders
- **v2.1**: Modern color refinements for better readability
- **v2.2**: Enhanced nakshatra boundary system with clean lines
- **v2.3**: Zodiac symbol integration and proper positioning
- **v3.0**: Complete labeling system, comprehensive user details, and professional design

## Differences from Previous Implementations

❌ **Previous Wrong Approach:**
- Mixed up house numbers with zodiac signs
- Placed planets by house number instead of zodiac sign
- Incorrect 0° reference point
- Sun wrongly placed in Pisces instead of Sagittarius
- Generic pada colors without traditional significance
- No visual distinction between nakshatras and padas

✅ **This Correct Approach:**
- Fixed zodiac sign positions in grid
- Planets placed by actual zodiac sign (nirayana longitude)
- Correct 0° starting from Aries corner
- Sun correctly placed in Sagittarius
- Traditional nakshatra colors based on authentic Vedic descriptions
- Clear visual hierarchy with different border weights
- Corner-precise pada block positioning

## Code Structure

### Key Functions
- `add_pada_ruler_around_perimeter()`: Creates the 360° nakshatra pada ruler with modern balanced colors
- `draw_pada_block_from_aries()`: Draws individual pada blocks with uniform borders
- `draw_nakshatra_boundary_line()`: Adds strong boundary lines at nakshatra endings (every 4th pada)
- `add_planetary_tick_marks()`: Places planet markers at exact nirayana longitudes with appropriate symbols
- `add_planets_to_signs()`: Places planets in correct zodiac sign cells (not house numbers)
- `calculate_house_to_sign_mapping()`: Correctly maps houses to signs based on ascendant
- `add_chart_title_and_info()`: Displays comprehensive user details in center with proper formatting
- `get_sign_label()`: Returns appropriate zodiac labels based on current label mode
- `get_planet_symbol()`: Returns appropriate planet symbols based on current label mode

### Configuration Constants
- `CANVAS_SIZE = 800`: SVG canvas dimensions
- `RULER_WIDTH = 15`: Width of the perimeter pada ruler
- `LABEL_OPTIONS`: Current labeling mode ("western", "vedic", "symbol")
- `ZODIAC_COLORS`: Modern balanced colors for zodiac signs
- `NAKSHATRA_COLORS`: Modern balanced colors for 27 nakshatras
- `PLANET_COLORS`: Color mapping for planetary symbols and tick marks
- `SIGN_POSITIONS`: Fixed mapping of zodiac signs to 4×4 grid positions
- `SIGN_NAMES_WESTERN/VEDIC`: Name dictionaries for different labeling modes
- `PLANET_SYMBOLS_WESTERN/VEDIC/PURE`: Symbol dictionaries for different labeling modes

## Dependencies

- Python 3.6+
- Standard library only (json, sys, pathlib, xml.etree.ElementTree, xml.dom.minidom)

## References

- Traditional South Indian chart format
- Vedic astrology principles  
- Nakshatra pada system (108 divisions of 3°20' each)
- Traditional nakshatra color descriptions from classical texts
- Sample charts and detailed implementation instructions
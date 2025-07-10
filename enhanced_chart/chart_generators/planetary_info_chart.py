#!/usr/bin/env python3
"""
Planetary Info Chart Generator
===============================

Generates planetary information charts as SVG images showing
planetary positions with symbols, coordinates, and details.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from .base_chart import ChartGenerator


class PlanetaryInfoChart(ChartGenerator):
    """Generates planetary information chart with positions and details."""
    
    def __init__(self, chart_data: Dict[str, Any], output_dir: Path):
        """Initialize planetary info chart generator."""
        super().__init__(chart_data, output_dir)
        
        # Chart specific dimensions
        self.chart_width = 200
        self.line_height = 18
        self.margin = 15
        
        # Planet symbols mapping (Unicode astronomical symbols)
        self.planet_symbols = {
            'Sun': '☉',
            'Moon': '☽',
            'Mars': '♂',
            'Mercury': '☿',
            'Jupiter': '♃',
            'Venus': '♀',
            'Saturn': '♄',
            'Rahu': '☊',
            'Ketu': '☋',
            'Uranus': '♅',
            'Neptune': '♆',
            'Pluto': '♇',
            'Ascendant': 'Asc',
            'Asc': 'Asc'
        }
        
        # Sign symbols mapping
        self.sign_symbols = {
            'Aries': '♈', 'Mesha': '♈',
            'Taurus': '♉', 'Vrishabha': '♉',
            'Gemini': '♊', 'Mithuna': '♊',
            'Cancer': '♋', 'Karka': '♋',
            'Leo': '♌', 'Simha': '♌',
            'Virgo': '♍', 'Kanya': '♍',
            'Libra': '♎', 'Thula': '♎',
            'Scorpio': '♏', 'Vrischika': '♏',
            'Sagittarius': '♐', 'Dhanu': '♐', 'Saggitarius': '♐',
            'Capricorn': '♑', 'Makara': '♑',
            'Aquarius': '♒', 'Kumbha': '♒',
            'Pisces': '♓', 'Meena': '♓'
        }
        
        # Planet colors (matching the sample)
        self.planet_colors = {
            'Sun': (255, 140, 0),      # Dark orange
            'Moon': (0, 100, 200),     # Blue
            'Mars': (255, 0, 0),       # Red
            'Mercury': (0, 150, 0),    # Green
            'Jupiter': (255, 165, 0),  # Orange
            'Venus': (128, 0, 128),    # Purple
            'Saturn': (0, 0, 139),     # Dark blue
            'Rahu': (139, 69, 19),     # Brown
            'Ketu': (105, 105, 105),   # Gray
            'Uranus': (0, 255, 255),   # Cyan
            'Neptune': (0, 0, 255),    # Blue
            'Pluto': (128, 0, 0),      # Maroon
            'Ascendant': (255, 0, 0),  # Red
            'Asc': (255, 0, 0)         # Red
        }
    
    def _get_planetary_data(self) -> List[Dict[str, Any]]:
        """
        Extract planetary data from chart data.
        
        Returns:
            List of planetary information dictionaries
        """
        planetary_info = []
        
        # Get D1 chart data
        d1_data = self._safe_get(self.chart_data, 'D1', default={})
        
        # Add ascendant first
        asc_data = self._safe_get(d1_data, 'ascendant', default={})
        if asc_data:
            planetary_info.append(self._format_planetary_entry('Ascendant', asc_data))
        
        # Add planets
        planets_data = self._safe_get(d1_data, 'planets', default={})
        for planet_name, planet_data in planets_data.items():
            planetary_info.append(self._format_planetary_entry(planet_name, planet_data))
        
        # Add nodes if available
        nodes_data = self._safe_get(self.chart_data, 'nodes', default={})
        if nodes_data:
            for node_name, node_data in nodes_data.items():
                planetary_info.append(self._format_planetary_entry(node_name, node_data))
        
        return planetary_info
    
    def _format_planetary_entry(self, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format planetary data entry.
        
        Args:
            name: Planet name
            data: Planet data dictionary
            
        Returns:
            Formatted planetary entry
        """
        # Get position
        pos = self._safe_get(data, 'pos', default={})
        if not pos:
            # Try nirayana_long for degrees
            nirayana_long = self._safe_get(data, 'nirayana_long', default=0)
            if nirayana_long:
                deg = int(nirayana_long % 30)
                min_val = int((nirayana_long % 30 - deg) * 60)
                sec_val = int(((nirayana_long % 30 - deg) * 60 - min_val) * 60)
                pos = {'deg': deg, 'min': min_val, 'sec': sec_val}
            else:
                pos = {'deg': 0, 'min': 0, 'sec': 0}
        
        # Get sign
        sign = self._safe_get(data, 'sign', default='')
        if not sign:
            sign = self._safe_get(data, 'rashi', default='')
        
        # Get nakshatra
        nakshatra = self._safe_get(data, 'nakshatra', default='')
        
        # Get retrogradation status
        retro = self._safe_get(data, 'retro', default=False)
        
        return {
            'name': name,
            'pos': pos,
            'sign': sign,
            'nakshatra': nakshatra,
            'retro': retro
        }
    
    def _format_position_string(self, pos: Dict[str, Any], sign: str, retro: bool = False) -> str:
        """
        Format position string with degrees, minutes, seconds, and sign.
        
        Args:
            pos: Position dictionary with deg, min, sec
            sign: Sign name
            retro: Whether planet is retrograde
            
        Returns:
            Formatted position string
        """
        deg = pos.get('deg', 0)
        min_val = pos.get('min', 0)
        sec_val = pos.get('sec', 0)
        
        # Get sign symbol
        sign_symbol = self.sign_symbols.get(sign, sign[:2] if sign else '')
        
        # Format retrograde indicator
        retro_indicator = 'R' if retro else ''
        
        return f"{deg}°{min_val:02d}'{sec_val:02d}\" {sign_symbol} {retro_indicator}".strip()
    
    def _create_svg_root(self, width: int, height: int) -> Element:
        """Create SVG root element."""
        root = Element('svg', {
            'width': str(width),
            'height': str(height),
            'xmlns': 'http://www.w3.org/2000/svg',
            'viewBox': f'0 0 {width} {height}'
        })
        
        # Add styles
        defs = SubElement(root, 'defs')
        style = SubElement(defs, 'style')
        style.text = """
            .header { font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; fill: #FF0000; }
            .planet-symbol { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; }
            .planet-name { font-family: Arial, sans-serif; font-size: 12px; fill: #000000; }
            .position-text { font-family: Arial, sans-serif; font-size: 10px; fill: #000000; }
        """
        
        # White background
        SubElement(root, 'rect', {
            'x': '0', 'y': '0',
            'width': str(width), 'height': str(height),
            'fill': 'white'
        })
        
        return root
    
    def _add_svg_text(self, parent: Element, x: int, y: int, text: str, 
                     css_class: str = None, fill: str = None) -> Element:
        """Add text element to SVG."""
        attrs = {'x': str(x), 'y': str(y)}
        if css_class:
            attrs['class'] = css_class
        if fill:
            attrs['fill'] = fill
        
        text_elem = SubElement(parent, 'text', attrs)
        text_elem.text = text
        return text_elem
    
    
    def generate(self) -> str:
        """
        Generate planetary information chart as SVG.
        
        Returns:
            Path to generated SVG file
        """
        # Get planetary data
        planetary_data = self._get_planetary_data()
        
        # Calculate SVG dimensions
        num_entries = len(planetary_data)
        chart_height = num_entries * self.line_height + 20
        svg_width = 300
        svg_height = chart_height + 2 * self.margin + 40  # Extra space for header
        
        # Create SVG root
        root = self._create_svg_root(svg_width, svg_height)
        
        # Add header
        header_y = 25
        self._add_svg_text(root, 10, header_y, "Planetary Info:", css_class="header")
        
        # Add planetary information
        info_start_x = self.margin
        info_start_y = header_y + 25
        
        y_offset = 0
        for planet_info in planetary_data:
            planet_name = planet_info['name']
            pos = planet_info['pos']
            sign = planet_info['sign']
            retro = planet_info['retro']
            
            # Get planet symbol and color
            planet_symbol = self.planet_symbols.get(planet_name, planet_name[:2])
            planet_color = f"rgb({self.planet_colors.get(planet_name, self.text_color)[0]}, {self.planet_colors.get(planet_name, self.text_color)[1]}, {self.planet_colors.get(planet_name, self.text_color)[2]})"
            
            # Format position string
            pos_string = self._format_position_string(pos, sign, retro)
            
            current_y = info_start_y + y_offset
            
            # Add planet symbol
            self._add_svg_text(root, info_start_x, current_y, planet_symbol, 
                             css_class="planet-symbol", fill=planet_color)
            
            # Add planet name
            self._add_svg_text(root, info_start_x + 25, current_y, planet_name, 
                             css_class="planet-name")
            
            # Add position
            self._add_svg_text(root, info_start_x + 100, current_y, pos_string, 
                             css_class="position-text")
            
            y_offset += self.line_height
        
        # Generate filename
        user_name = self._get_user_name()
        filename = f"{user_name}_planetary_info.svg"
        
        # Save SVG
        filepath = self._save_svg(root, filename)
        return filepath
    
    def _save_svg(self, root: Element, filename: str) -> str:
        """Save SVG to file."""
        # Pretty print XML
        rough_string = tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent='  ')
        
        # Save to file
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        return str(filepath)
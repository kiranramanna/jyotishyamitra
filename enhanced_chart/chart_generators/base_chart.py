#!/usr/bin/env python3
"""
Base Chart Generator
====================

Base class for generating astrological charts as SVG images.
Provides common functionality for all chart types.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class ChartGenerator:
    """Base class for all chart generators."""
    
    def __init__(self, chart_data: Dict[str, Any], output_dir: Path):
        """
        Initialize chart generator.
        
        Args:
            chart_data: Dictionary containing chart data from JSON
            output_dir: Directory to save generated charts
        """
        self.chart_data = chart_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Common styling (RGB values)
        self.bg_color = (255, 255, 255)  # White background
        self.text_color = (0, 0, 0)      # Black text
        self.header_color = (255, 0, 0)  # Red headers
        self.border_color = (0, 0, 0)    # Black borders
        self.grid_color = (128, 128, 128)  # Gray grid lines
        
        # Font settings
        self.header_font_size = 16
        self.text_font_size = 12
        self.small_font_size = 10
        
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color string."""
        return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
    
    def _create_svg_root(self, width: int, height: int) -> Element:
        """Create SVG root element with common styles."""
        root = Element('svg', {
            'width': str(width),
            'height': str(height),
            'xmlns': 'http://www.w3.org/2000/svg',
            'viewBox': f'0 0 {width} {height}'
        })
        
        # Add common styles
        defs = SubElement(root, 'defs')
        style = SubElement(defs, 'style')
        style.text = f"""
            .header {{ font-family: Arial, sans-serif; font-size: {self.header_font_size}px; font-weight: bold; fill: {self._rgb_to_hex(self.header_color)}; }}
            .text {{ font-family: Arial, sans-serif; font-size: {self.text_font_size}px; fill: {self._rgb_to_hex(self.text_color)}; }}
            .small-text {{ font-family: Arial, sans-serif; font-size: {self.small_font_size}px; fill: {self._rgb_to_hex(self.text_color)}; }}
        """
        
        # White background
        SubElement(root, 'rect', {
            'x': '0', 'y': '0',
            'width': str(width), 'height': str(height),
            'fill': self._rgb_to_hex(self.bg_color)
        })
        
        return root
    
    def _add_svg_text(self, parent: Element, x: int, y: int, text: str, 
                     css_class: str = "text", fill: str = None, text_anchor: str = "middle") -> Element:
        """Add text element to SVG."""
        attrs = {'x': str(x), 'y': str(y), 'class': css_class, 'text-anchor': text_anchor}
        if fill:
            attrs['fill'] = fill
        
        text_elem = SubElement(parent, 'text', attrs)
        text_elem.text = text
        return text_elem
    
    def _add_svg_rect(self, parent: Element, x: int, y: int, width: int, height: int, 
                     fill: str = None, stroke: str = None, stroke_width: str = "1") -> Element:
        """Add rectangle to SVG."""
        attrs = {
            'x': str(x), 'y': str(y),
            'width': str(width), 'height': str(height),
            'stroke-width': stroke_width
        }
        if fill:
            attrs['fill'] = fill
        else:
            attrs['fill'] = self._rgb_to_hex(self.bg_color)
        if stroke:
            attrs['stroke'] = stroke
        else:
            attrs['stroke'] = self._rgb_to_hex(self.border_color)
        
        return SubElement(parent, 'rect', attrs)
    
    def _get_user_name(self) -> str:
        """Get user name from chart data."""
        return self.chart_data.get('user_details', {}).get('name', 'Chart')
    
    def _safe_get(self, data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
        """
        Safely get nested dictionary values.
        
        Args:
            data: Dictionary to search
            *keys: Keys to traverse
            default: Default value if key not found
            
        Returns:
            Value at nested key or default
        """
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def generate(self) -> str:
        """
        Generate the chart and save as SVG.
        
        Returns:
            Path to generated SVG file
        """
        raise NotImplementedError("Subclasses must implement generate() method")
    
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
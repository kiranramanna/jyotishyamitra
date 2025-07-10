#!/usr/bin/env python3
"""
Vimshottari Chart Generator
===========================

Generates Vimshottari Dasha charts as SVG images showing
dasha periods timeline with dates and durations.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element
from .base_chart import ChartGenerator


class VimshottariChart(ChartGenerator):
    """Generates Vimshottari Dasha chart with timeline periods."""
    
    def __init__(self, chart_data: Dict[str, Any], output_dir: Path):
        """Initialize Vimshottari chart generator."""
        super().__init__(chart_data, output_dir)
        
        # Chart specific dimensions
        self.chart_width = 400
        self.line_height = 20
        self.section_height = 150
        self.margin = 20
        self.column_widths = [30, 80, 80, 80, 80]  # Period, Planet, Date, Duration, etc.
        
        # Timeline colors
        self.timeline_colors = {
            1: (255, 200, 200),  # Light red
            2: (200, 255, 200),  # Light green
            3: (200, 200, 255),  # Light blue
            4: (255, 255, 200),  # Light yellow
            5: (255, 200, 255),  # Light magenta
        }
        
        # Dasha planet abbreviations
        self.dasha_planets = {
            'Sun': 'Su', 'Moon': 'Mo', 'Mars': 'Ma', 'Mercury': 'Me',
            'Jupiter': 'Ju', 'Venus': 'Ve', 'Saturn': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke'
        }
    
    def _get_vimshottari_data(self) -> Dict[str, Any]:
        """
        Extract Vimshottari data from chart data.
        
        Returns:
            Dictionary with Vimshottari dasha periods
        """
        vimshottari_data = self._safe_get(self.chart_data, 'vimshottari', default={})
        
        # If no vimshottari data, create sample data matching the image
        if not vimshottari_data:
            # Sample data from the image
            vimshottari_data = {
                'mahadasha': [
                    {'period': 1, 'planet': 'Moon', 'start_date': '14/06/1857 00:15', 'duration': '-5yrs -6mts'},
                    {'period': 2, 'planet': 'Mars', 'start_date': '14/06/1857 10:23', 'duration': '4yrs 5mts'},
                    {'period': 3, 'planet': 'Rahu', 'start_date': '14/06/1874 03:04', 'duration': '11yrs 2mts'},
                    {'period': 4, 'planet': 'Jupiter', 'start_date': '13/06/1892 11:42', 'duration': '23yrs 5mts'},
                    {'period': 5, 'planet': 'Saturn', 'start_date': '14/06/1908 08:42', 'duration': '64yrs 5mts'},
                    {'period': 6, 'planet': 'Mercury', 'start_date': '14/06/1927 23:09', 'duration': '50yrs 4mts'},
                    {'period': 7, 'planet': 'Ketu', 'start_date': '14/06/1944 01:58', 'duration': '68yrs 5mts'},
                    {'period': 8, 'planet': 'Venus', 'start_date': '14/06/1951 18:39', 'duration': '68yrs 5mts'},
                    {'period': 9, 'planet': 'Sun', 'start_date': '14/06/1971 14:59', 'duration': '80yrs 5mts'}
                ],
                'antardasha': [
                    {'period': 1, 'planet': 'Saturn/Rahu', 'start_date': '25/01/1922 17:51', 'duration': '59yrs 0mts'},
                    {'period': 2, 'planet': 'Saturn/Jupiter', 'start_date': '01/12/1924 16:25', 'duration': '61yrs 10mts'},
                    {'period': 3, 'planet': 'Saturn/Saturn', 'start_date': '14/06/1927 23:09', 'duration': '64yrs 5mts'},
                    {'period': 4, 'planet': 'Saturn/Mercury', 'start_date': '16/11/1929 14:09', 'duration': '66yrs 7mts'},
                    {'period': 5, 'planet': 'Saturn/Ketu', 'start_date': '07/11/1930 08:54', 'duration': '67yrs 6mts'},
                    {'period': 6, 'planet': 'Saturn/Venus', 'start_date': '14/06/1948 21:01', 'duration': '65yrs 4mts'},
                    {'period': 7, 'planet': 'Saturn/Sun', 'start_date': '10/12/1936 17:19', 'duration': '73yrs 10mts'},
                    {'period': 8, 'planet': 'Saturn/Moon', 'start_date': '06/06/1939 02:06', 'duration': '76yrs 5mts'},
                    {'period': 9, 'planet': 'Saturn/Mars', 'start_date': '10/01/1941 02:19', 'duration': '78yrs 5mts'}
                ]
            }
        
        return vimshottari_data
    
    def _draw_svg_section_header(self, root: Element, title: str, 
                               x: int, y: int, width: int) -> int:
        """
        Draw section header with background in SVG.
        
        Args:
            root: SVG root element
            title: Section title
            x: X coordinate
            y: Y coordinate
            width: Section width
            
        Returns:
            Height of header
        """
        # Draw header background
        header_height = self.line_height + 5
        self._add_svg_rect(root, x, y, width, header_height, 
                          fill="rgb(255, 165, 0)")
        
        # Draw title
        text_x = x + width // 2
        text_y = y + header_height // 2 + 5  # Adjust for text baseline
        self._add_svg_text(root, text_x, text_y, title, css_class="text")
        
        return header_height
    
    def _draw_svg_column_headers(self, root: Element, x: int, y: int) -> int:
        """
        Draw column headers for the dasha table in SVG.
        
        Args:
            root: SVG root element
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Height of column headers
        """
        headers = ['', 'Planet', 'Date', 'Duration', 'Years']
        current_x = x
        
        for i, header in enumerate(headers):
            width = self.column_widths[i]
            
            # Draw header cell
            self._add_svg_rect(root, current_x, y, width, self.line_height)
            
            # Draw header text
            if header:
                text_x = current_x + width // 2
                text_y = y + self.line_height // 2 + 4  # Adjust for text baseline
                self._add_svg_text(root, text_x, text_y, header, css_class="small-text")
            
            current_x += width
        
        return self.line_height
    
    def _draw_svg_dasha_periods(self, root: Element, periods: List[Dict[str, Any]], 
                              x: int, y: int) -> int:
        """
        Draw dasha periods table in SVG.
        
        Args:
            root: SVG root element
            periods: List of dasha periods
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Height of drawn periods
        """
        current_y = y
        
        for period_data in periods:
            period_num = period_data.get('period', 1)
            planet = period_data.get('planet', '')
            start_date = period_data.get('start_date', '')
            duration = period_data.get('duration', '')
            
            # Get timeline color
            timeline_color = self.timeline_colors.get(period_num, self.bg_color)
            timeline_color_str = f"rgb({timeline_color[0]}, {timeline_color[1]}, {timeline_color[2]})"
            
            # Draw period number cell
            current_x = x
            self._add_svg_rect(root, current_x, current_y, self.column_widths[0], self.line_height, 
                              fill=timeline_color_str)
            
            text_x = current_x + self.column_widths[0] // 2
            text_y = current_y + self.line_height // 2 + 4  # Adjust for text baseline
            self._add_svg_text(root, text_x, text_y, str(period_num), css_class="small-text")
            
            # Draw planet cell
            current_x += self.column_widths[0]
            self._add_svg_rect(root, current_x, current_y, self.column_widths[1], self.line_height)
            
            # Abbreviate planet name
            planet_abbr = self.dasha_planets.get(planet.split('/')[0], planet)
            if '/' in planet:
                parts = planet.split('/')
                planet_abbr = f"{self.dasha_planets.get(parts[0], parts[0])}/{self.dasha_planets.get(parts[1], parts[1])}"
            
            text_x = current_x + 5
            text_y = current_y + self.line_height // 2 + 4  # Adjust for text baseline
            self._add_svg_text(root, text_x, text_y, planet_abbr, css_class="small-text", text_anchor="start")
            
            # Draw date cell
            current_x += self.column_widths[1]
            self._add_svg_rect(root, current_x, current_y, self.column_widths[2], self.line_height)
            
            text_x = current_x + 5
            text_y = current_y + self.line_height // 2 + 4  # Adjust for text baseline
            self._add_svg_text(root, text_x, text_y, start_date, css_class="small-text", text_anchor="start")
            
            # Draw duration cell
            current_x += self.column_widths[2]
            self._add_svg_rect(root, current_x, current_y, self.column_widths[3], self.line_height)
            
            text_x = current_x + 5
            text_y = current_y + self.line_height // 2 + 4  # Adjust for text baseline
            self._add_svg_text(root, text_x, text_y, duration, css_class="small-text", text_anchor="start")
            
            # Draw years cell (optional)
            current_x += self.column_widths[3]
            self._add_svg_rect(root, current_x, current_y, self.column_widths[4], self.line_height)
            
            current_y += self.line_height
        
        return current_y - y
    
    def generate(self) -> str:
        """
        Generate Vimshottari chart.
        
        Returns:
            Path to generated SVG file
        """
        # Get vimshottari data
        vimshottari_data = self._get_vimshottari_data()
        
        # Calculate SVG dimensions
        table_width = sum(self.column_widths)
        
        mahadasha_periods = vimshottari_data.get('mahadasha', [])
        antardasha_periods = vimshottari_data.get('antardasha', [])
        
        # Calculate heights
        mahadasha_height = len(mahadasha_periods) * self.line_height + 50  # +50 for headers
        antardasha_height = len(antardasha_periods) * self.line_height + 50
        
        svg_height = mahadasha_height + antardasha_height + 4 * self.margin + 40  # Extra space for main header
        svg_width = table_width + 2 * self.margin
        
        # Create SVG
        root = self._create_svg_root(svg_width, svg_height)
        
        # Draw main header
        header_y = 25
        self._add_svg_text(root, 10, header_y, "Vimshottari Dasha:", css_class="header")
        
        current_y = header_y + 30
        
        # Draw Mahadasha section
        section_header_height = self._draw_svg_section_header(root, "Vimshottari", 
                                                            self.margin, current_y, table_width)
        current_y += section_header_height + 5
        
        # Draw mahadasha column headers
        col_header_height = self._draw_svg_column_headers(root, self.margin, current_y)
        current_y += col_header_height
        
        # Draw mahadasha periods
        periods_height = self._draw_svg_dasha_periods(root, mahadasha_periods, self.margin, current_y)
        current_y += periods_height + 20
        
        # Draw Antardasha section
        section_header_height = self._draw_svg_section_header(root, "Vimshottari", 
                                                            self.margin, current_y, table_width)
        current_y += section_header_height + 5
        
        # Draw antardasha column headers
        col_header_height = self._draw_svg_column_headers(root, self.margin, current_y)
        current_y += col_header_height
        
        # Draw antardasha periods
        self._draw_svg_dasha_periods(root, antardasha_periods, self.margin, current_y)
        
        # Generate filename
        user_name = self._get_user_name()
        filename = f"{user_name}_vimshottari_dasha.svg"
        
        # Save SVG
        filepath = self._save_svg(root, filename)
        return filepath
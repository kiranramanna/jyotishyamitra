#!/usr/bin/env python3
"""
Shadbala Chart Generator
========================

Generates Shadbala (planetary strength) charts as SVG images showing
tabular planetary strength analysis with percentages.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from .base_chart import ChartGenerator


class ShadbalaChart(ChartGenerator):
    """Generates Shadbala chart with tabular planetary strength analysis."""
    
    def __init__(self, chart_data: Dict[str, Any], output_dir: Path):
        """Initialize Shadbala chart generator."""
        super().__init__(chart_data, output_dir)
        
        # Chart specific dimensions
        self.cell_width = 45
        self.cell_height = 25
        self.margin = 20
        
        # Traditional Shadbala requirements (Brihat Parashara Hora Sastra)
        # "Thirty-nine, thirty-six, thirty, forty-two, thirty-nine, thirty-three
        # and thirty multiplied by ten for the Sun, etc."
        self.required_strength = {
            'Sun': 390,      # 39 x 10
            'Moon': 360,     # 36 x 10
            'Mars': 300,     # 30 x 10
            'Mercury': 420,  # 42 x 10
            'Jupiter': 390,  # 39 x 10
            'Venus': 330,    # 33 x 10
            'Saturn': 300    # 30 x 10
        }
        
        # Shadbala row labels
        self.shadbala_rows = [
            'SthB',    # Sthana Bala
            'DigB',    # Dig Bala
            'KalB',    # Kala Bala
            'ChB',     # Cheshta Bala
            'NaiB',    # Naisargika Bala
            'DriB',    # Drik Bala
            'YudB'     # Yuddha Bala
        ]
        
        # Planet columns  
        self.planet_columns = ['Su', 'Mo', 'Ma', 'Me', 'Ju', 'Ve', 'Sa']
        
        # Planet name mapping
        self.planet_mapping = {
            'Su': 'Sun', 'Mo': 'Moon', 'Ma': 'Mars', 'Me': 'Mercury',
            'Ju': 'Jupiter', 'Ve': 'Venus', 'Sa': 'Saturn'
        }
        
        # Colors for different strength levels
        self.strength_colors = {
            'high': (144, 238, 144),    # Light green
            'medium': (255, 255, 224),  # Light yellow
            'low': (255, 182, 193),     # Light pink
            'default': (255, 255, 255)  # White
        }
    
    def _get_shadbala_data(self) -> Dict[str, Any]:
        """
        Extract Shadbala data from chart data and convert to display format.
        
        Returns:
            Dictionary with Shadbala strength values
        """
        # Extract from Balas.Shadbala in the JSON
        balas_data = self._safe_get(self.chart_data, 'Balas', default={})
        shadbala_raw = self._safe_get(balas_data, 'Shadbala', default={})
        
        # Convert to display format
        shadbala_data = {}
        
        if shadbala_raw:
            # Map JSON structure to display format
            mapping = {
                'SthB': 'Sthanabala.Total',
                'DigB': 'Digbala',
                'KalB': 'Kaalabala.Total',
                'ChB': 'Cheshtabala',
                'NaiB': 'Naisargikabala',
                'DriB': 'Drikbala',
                'YudB': 'Kaalabala.Yuddhabala'
            }
            
            for display_key, json_path in mapping.items():
                path_parts = json_path.split('.')
                data_source = shadbala_raw
                
                # Navigate through nested structure
                for part in path_parts:
                    data_source = data_source.get(part, {})
                    if not isinstance(data_source, dict):
                        break
                
                if isinstance(data_source, dict):
                    # Convert planet names and round values
                    row_data = {}
                    for planet_abbr in self.planet_columns:
                        planet_name = self.planet_mapping[planet_abbr]
                        value = data_source.get(planet_name, 0)
                        row_data[planet_abbr] = round(float(value)) if value else 0
                    shadbala_data[display_key] = row_data
        
        # If no shadbala data, create sample data
        if not shadbala_data:
            shadbala_data = {
                'SthB': {'Su': 215, 'Mo': 121, 'Ma': 276, 'Me': 194, 'Ju': 200, 'Ve': 197, 'Sa': 223},
                'DigB': {'Su': 52, 'Mo': 91, 'Ma': 208, 'Me': 110, 'Ju': 121, 'Ve': 145, 'Sa': 252},
                'KalB': {'Su': 29, 'Mo': 7, 'Ma': 1, 'Me': 55, 'Ju': 29, 'Ve': 34, 'Sa': 37},
                'ChB': {'Su': 0, 'Mo': 15, 'Ma': 3, 'Me': 137, 'Ju': 0, 'Ve': 57, 'Sa': 123},
                'NaiB': {'Su': 103, 'Mo': 62, 'Ma': 134, 'Me': 144, 'Ju': 126, 'Ve': 66, 'Sa': 69},
                'DriB': {'Su': 52, 'Mo': 62, 'Ma': 170, 'Me': 164, 'Ju': 112, 'Ve': 66, 'Sa': 105},
                'YudB': {'Su': 0, 'Mo': 0, 'Ma': 0, 'Me': 0, 'Ju': 0, 'Ve': 0, 'Sa': 0}
            }
        
        return shadbala_data
    
    def _calculate_totals_ranks_and_percentages(self, shadbala_data: Dict[str, Any]) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, float]]:
        """
        Calculate total strength, ranks, and percentages for each planet.
        
        Args:
            shadbala_data: Shadbala strength data
            
        Returns:
            Tuple of (totals, ranks, percentages) dictionaries
        """
        totals = {}
        percentages = {}
        
        # Calculate totals
        for planet in self.planet_columns:
            total = 0
            for row in self.shadbala_rows:
                if row in shadbala_data and planet in shadbala_data[row]:
                    total += shadbala_data[row][planet]
            totals[planet] = total
            
            # Calculate percentage based on traditional requirements
            planet_name = self.planet_mapping[planet]
            required = self.required_strength.get(planet_name, 300)
            percentage = (total / required) * 100 if required > 0 else 0
            percentages[planet] = round(percentage, 1)
        
        # Calculate ranks (1 = highest strength)
        sorted_planets = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        ranks = {}
        for i, (planet, _) in enumerate(sorted_planets):
            ranks[planet] = i + 1
        
        return totals, ranks, percentages
    
    def _get_cell_color(self, value: int, max_value: int) -> Tuple[int, int, int]:
        """
        Get cell color based on strength value.
        
        Args:
            value: Strength value
            max_value: Maximum value in the dataset
            
        Returns:
            RGB color tuple
        """
        if max_value == 0:
            return self.strength_colors['default']
        
        ratio = value / max_value
        
        if ratio >= 0.7:
            return self.strength_colors['high']
        elif ratio >= 0.4:
            return self.strength_colors['medium']
        elif ratio >= 0.1:
            return self.strength_colors['low']
        else:
            return self.strength_colors['default']
    
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
            .table-header { font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; fill: #000000; text-anchor: middle; }
            .table-cell { font-family: Arial, sans-serif; font-size: 11px; fill: #000000; text-anchor: middle; }
            .table-label { font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #000000; text-anchor: middle; }
        """
        
        # White background
        SubElement(root, 'rect', {
            'x': '0', 'y': '0',
            'width': str(width), 'height': str(height),
            'fill': 'white'
        })
        
        return root
    
    def _add_svg_rect(self, parent: Element, x: int, y: int, width: int, height: int, 
                     fill: str = 'white', stroke: str = 'black', stroke_width: str = '1') -> Element:
        """Add rectangle to SVG."""
        return SubElement(parent, 'rect', {
            'x': str(x), 'y': str(y),
            'width': str(width), 'height': str(height),
            'fill': fill, 'stroke': stroke, 'stroke-width': stroke_width
        })
    
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
    
    def _draw_svg_table(self, root: Element, shadbala_data: Dict[str, Any], totals: Dict[str, int], 
                       ranks: Dict[str, int], percentages: Dict[str, float], start_x: int, start_y: int) -> None:
        """Draw the Shadbala table in SVG format."""
        
        # Draw header row
        header_y = start_y
        
        # Empty cell for row labels
        self._add_svg_rect(root, start_x, header_y, self.cell_width, self.cell_height)
        
        # Planet headers
        for col, planet in enumerate(self.planet_columns):
            x = start_x + (col + 1) * self.cell_width
            self._add_svg_rect(root, x, header_y, self.cell_width, self.cell_height)
            
            # Add planet name
            text_x = x + self.cell_width // 2
            text_y = header_y + self.cell_height // 2 + 4
            self._add_svg_text(root, text_x, text_y, planet, css_class="table-header")
        
        # Draw data rows
        for row_idx, row_label in enumerate(self.shadbala_rows):
            y = start_y + (row_idx + 1) * self.cell_height
            
            # Row label
            self._add_svg_rect(root, start_x, y, self.cell_width, self.cell_height)
            text_x = start_x + self.cell_width // 2
            text_y = y + self.cell_height // 2 + 4
            self._add_svg_text(root, text_x, text_y, row_label, css_class="table-label")
            
            # Data cells
            row_data = shadbala_data.get(row_label, {})
            for col, planet in enumerate(self.planet_columns):
                x = start_x + (col + 1) * self.cell_width
                value = row_data.get(planet, 0)
                
                # Get cell color based on strength
                max_value = 300  # Approximate max for color scaling
                color_rgb = self._get_cell_color(value, max_value)
                color_hex = f"rgb({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})"
                
                # Draw cell
                self._add_svg_rect(root, x, y, self.cell_width, self.cell_height, fill=color_hex)
                
                # Draw value
                text_x = x + self.cell_width // 2
                text_y = y + self.cell_height // 2 + 4
                self._add_svg_text(root, text_x, text_y, str(value), css_class="table-cell")
        
        # Draw totals row
        total_y = start_y + (len(self.shadbala_rows) + 1) * self.cell_height
        
        # Total label
        self._add_svg_rect(root, start_x, total_y, self.cell_width, self.cell_height)
        text_x = start_x + self.cell_width // 2
        text_y = total_y + self.cell_height // 2 + 4
        self._add_svg_text(root, text_x, text_y, "Total", css_class="table-label")
        
        # Total values
        for col, planet in enumerate(self.planet_columns):
            x = start_x + (col + 1) * self.cell_width
            total_value = totals.get(planet, 0)
            
            self._add_svg_rect(root, x, total_y, self.cell_width, self.cell_height)
            text_x = x + self.cell_width // 2
            text_y = total_y + self.cell_height // 2 + 4
            self._add_svg_text(root, text_x, text_y, str(total_value), css_class="table-cell")
        
        # Draw ranks row
        rank_y = start_y + (len(self.shadbala_rows) + 2) * self.cell_height
        
        # Rank label
        self._add_svg_rect(root, start_x, rank_y, self.cell_width, self.cell_height)
        text_x = start_x + self.cell_width // 2
        text_y = rank_y + self.cell_height // 2 + 4
        self._add_svg_text(root, text_x, text_y, "Rank", css_class="table-label")
        
        # Rank values
        for col, planet in enumerate(self.planet_columns):
            x = start_x + (col + 1) * self.cell_width
            rank_value = ranks.get(planet, 0)
            
            self._add_svg_rect(root, x, rank_y, self.cell_width, self.cell_height)
            text_x = x + self.cell_width // 2
            text_y = rank_y + self.cell_height // 2 + 4
            self._add_svg_text(root, text_x, text_y, str(rank_value), css_class="table-cell")
        
        # Draw percentages row
        percentage_y = start_y + (len(self.shadbala_rows) + 3) * self.cell_height
        
        # Percentage label
        self._add_svg_rect(root, start_x, percentage_y, self.cell_width, self.cell_height)
        text_x = start_x + self.cell_width // 2
        text_y = percentage_y + self.cell_height // 2 + 4
        self._add_svg_text(root, text_x, text_y, "%", css_class="table-label")
        
        # Percentage values
        for col, planet in enumerate(self.planet_columns):
            x = start_x + (col + 1) * self.cell_width
            percentage_value = percentages.get(planet, 0)
            
            # Color code based on percentage strength
            if percentage_value >= 100:
                fill_color = "rgb(144, 238, 144)"  # Light green - very strong
            elif percentage_value >= 80:
                fill_color = "rgb(255, 255, 224)"  # Light yellow - strong
            elif percentage_value >= 60:
                fill_color = "rgb(255, 255, 255)"  # White - moderate
            else:
                fill_color = "rgb(255, 182, 193)"  # Light pink - weak
            
            self._add_svg_rect(root, x, percentage_y, self.cell_width, self.cell_height, fill=fill_color)
            text_x = x + self.cell_width // 2
            text_y = percentage_y + self.cell_height // 2 + 4
            self._add_svg_text(root, text_x, text_y, f"{percentage_value}%", css_class="table-cell")
    
    
    def generate(self) -> str:
        """
        Generate Shadbala chart as SVG.
        
        Returns:
            Path to generated SVG file
        """
        # Get shadbala data
        shadbala_data = self._get_shadbala_data()
        totals, ranks, percentages = self._calculate_totals_ranks_and_percentages(shadbala_data)
        
        # Calculate SVG dimensions
        table_width = (len(self.planet_columns) + 1) * self.cell_width
        table_height = (len(self.shadbala_rows) + 4) * self.cell_height  # +4 for header, total, rank, percentage
        
        svg_width = table_width + 2 * self.margin
        svg_height = table_height + 2 * self.margin + 50  # Extra space for header
        
        # Create SVG
        root = self._create_svg_root(svg_width, svg_height)
        
        # Add header
        header_y = 25
        self._add_svg_text(root, 10, header_y, "ShadBala:", css_class="header")
        
        # Draw table
        table_start_x = self.margin
        table_start_y = header_y + 25
        
        self._draw_svg_table(root, shadbala_data, totals, ranks, percentages, table_start_x, table_start_y)
        
        # Generate filename
        user_name = self._get_user_name()
        filename = f"{user_name}_shadbala.svg"
        
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
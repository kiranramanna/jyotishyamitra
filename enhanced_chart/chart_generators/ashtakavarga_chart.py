#!/usr/bin/env python3
"""
Ashtakavarga Chart Generator
============================

Generates Ashtakavarga charts as SVG images showing the 4x4 grid
with numerical values for each house.
"""

from pathlib import Path
from typing import Dict, Any, List
from xml.etree.ElementTree import Element
from .base_chart import ChartGenerator


class AshtakavargaChart(ChartGenerator):
    """Generates Ashtakavarga chart with 4x4 grid layout."""
    
    def __init__(self, chart_data: Dict[str, Any], output_dir: Path):
        """Initialize Ashtakavarga chart generator."""
        super().__init__(chart_data, output_dir)
        
        # Chart specific dimensions
        self.chart_width = 200
        self.chart_height = 200
        self.cell_size = 45
        self.margin = 20
        
        # Total image dimensions
        self.image_width = self.chart_width + 2 * self.margin
        self.image_height = self.chart_height + 2 * self.margin + 30  # Extra space for header
        
    def _convert_houses_to_grid(self, house_values: List[int]) -> List[List[int]]:
        """
        Convert 12-house array to 4x4 grid format.
        
        Args:
            house_values: List of 12 house values
            
        Returns:
            4x4 grid with center merged
        """
        if len(house_values) != 12:
            # Fallback to sample data if invalid
            return [
                [27, 21, 35, 27],
                [30, 0, 0, 32],
                [25, 0, 0, 21],
                [24, 31, 33, 31]
            ]
        
        # Map houses to grid positions (South Indian style)
        # Houses: 1=Aries, 2=Taurus, ..., 12=Pisces
        # Grid positions: (row, col)
        house_to_position = {
            12: (0, 0),  # Pisces
            1: (0, 1),   # Aries
            2: (0, 2),   # Taurus
            3: (0, 3),   # Gemini
            11: (1, 0),  # Aquarius
            10: (2, 0),  # Capricorn
            9: (3, 0),   # Sagittarius
            8: (3, 1),   # Scorpio
            7: (3, 2),   # Libra
            6: (3, 3),   # Virgo
            5: (2, 3),   # Leo
            4: (1, 3)    # Cancer
        }
        
        # Initialize 4x4 grid
        grid = [[0 for _ in range(4)] for _ in range(4)]
        
        # Fill grid with house values
        for house_num, value in enumerate(house_values, 1):
            if house_num in house_to_position:
                row, col = house_to_position[house_num]
                grid[row][col] = value
        
        # Center cells (1,1), (1,2), (2,1), (2,2) will be handled specially for merging
        return grid

    def _get_ashtakavarga_data(self) -> Dict[str, List[List[int]]]:
        """
        Extract ashtakavarga data from chart data.
        
        Returns:
            Dictionary with ashtakavarga grids for each planet
        """
        # Try different possible keys
        ashtakavarga_raw = (self._safe_get(self.chart_data, 'AshtakaVarga', default={}) or 
                           self._safe_get(self.chart_data, 'ashtakavarga', default={}))
        
        ashtakavarga_grids = {}
        
        if ashtakavarga_raw:
            # Convert each planet's house array to grid
            for planet, house_values in ashtakavarga_raw.items():
                if isinstance(house_values, list) and len(house_values) == 12:
                    ashtakavarga_grids[planet] = self._convert_houses_to_grid(house_values)
                else:
                    # Fallback for invalid data
                    ashtakavarga_grids[planet] = self._convert_houses_to_grid([0] * 12)
        
        # If no ashtakavarga data, create sample data
        if not ashtakavarga_grids:
            sample_grid = [
                [27, 21, 35, 27],
                [30, 0, 0, 32],
                [25, 0, 0, 21],
                [24, 31, 33, 31]
            ]
            ashtakavarga_grids = {
                'Sun': sample_grid,
                'Moon': sample_grid,
                'Mars': sample_grid,
                'Mercury': sample_grid,
                'Jupiter': sample_grid,
                'Venus': sample_grid,
                'Saturn': sample_grid,
                'Total': sample_grid
            }
        
        return ashtakavarga_grids
    
    def _draw_svg_grid(self, root: Element, grid_data: List[List[int]], 
                      start_x: int, start_y: int) -> None:
        """
        Draw the 4x4 ashtakavarga grid with merged center in SVG.
        
        Args:
            root: SVG root element
            grid_data: 4x4 grid of numerical values
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
        """
        # Draw outer cells first
        for row in range(4):
            for col in range(4):
                # Skip center cells - they will be drawn as one merged cell
                if (row == 1 and col == 1) or (row == 1 and col == 2) or \
                   (row == 2 and col == 1) or (row == 2 and col == 2):
                    continue
                
                x = start_x + col * self.cell_size
                y = start_y + row * self.cell_size
                
                # Draw cell border
                self._add_svg_rect(root, x, y, self.cell_size, self.cell_size)
                
                # Get cell value
                cell_value = grid_data[row][col] if row < len(grid_data) and col < len(grid_data[row]) else 0
                text = str(cell_value)
                
                # Draw text centered in cell
                if text:
                    text_x = x + self.cell_size // 2
                    text_y = y + self.cell_size // 2 + 5  # Adjust for text baseline
                    
                    self._add_svg_text(root, text_x, text_y, text, css_class="text")
        
        # Draw merged center cell (spans 2x2)
        center_x = start_x + 1 * self.cell_size
        center_y = start_y + 1 * self.cell_size
        center_width = 2 * self.cell_size
        center_height = 2 * self.cell_size
        
        # Draw merged center rectangle
        self._add_svg_rect(root, center_x, center_y, center_width, center_height)
        
        # Draw "SAT" in the center of the merged cell
        text = "SAT"
        text_x = center_x + center_width // 2
        text_y = center_y + center_height // 2 + 5  # Adjust for text baseline
        
        self._add_svg_text(root, text_x, text_y, text, css_class="text")
    
    def generate(self, planet: str = "Sun") -> str:
        """
        Generate Ashtakavarga chart for specified planet.
        
        Args:
            planet: Planet name (Sun, Moon, Mars, etc.)
            
        Returns:
            Path to generated SVG file
        """
        # Get ashtakavarga data
        ashtakavarga_data = self._get_ashtakavarga_data()
        
        # Use first available planet if specified planet not found
        if planet not in ashtakavarga_data:
            planet = list(ashtakavarga_data.keys())[0]
        
        grid_data = ashtakavarga_data[planet]
        
        # Create SVG
        root = self._create_svg_root(self.image_width, self.image_height)
        
        # Draw header
        header_y = 25
        self._add_svg_text(root, 10, header_y, "Ashtakavarga:", css_class="header")
        
        # Draw grid
        grid_start_x = self.margin
        grid_start_y = header_y + 25
        
        self._draw_svg_grid(root, grid_data, grid_start_x, grid_start_y)
        
        # Generate filename
        user_name = self._get_user_name()
        filename = f"{user_name}_ashtakavarga_{planet.lower()}.svg"
        
        # Save SVG
        filepath = self._save_svg(root, filename)
        return filepath
    
    def generate_all(self) -> List[str]:
        """
        Generate Ashtakavarga charts for all planets.
        
        Returns:
            List of paths to generated SVG files
        """
        ashtakavarga_data = self._get_ashtakavarga_data()
        filepaths = []
        
        for planet in ashtakavarga_data.keys():
            filepath = self.generate(planet)
            filepaths.append(filepath)
        
        return filepaths
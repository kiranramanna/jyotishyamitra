# -*- coding: utf-8 -*-
"""
South Indian Vedic Chart SVG Generator for Kerykeion
"""

import logging
from pathlib import Path
from string import Template
from typing import Union, List, Optional
from datetime import datetime

from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
from kerykeion.settings.kerykeion_settings import get_settings
from kerykeion.astrological_subject import AstrologicalSubject
from kerykeion.kr_types import KerykeionException, ChartType, KerykeionPointModel, Sign
from kerykeion.kr_types.kr_models import AstrologicalSubjectModel, CompositeSubjectModel
from kerykeion.kr_types.settings_models import KerykeionSettingsModel
from kerykeion.kr_types.kr_literals import KerykeionChartTheme, KerykeionChartLanguage, AxialCusps, Planet
from kerykeion.charts.charts_utils import (
    convert_latitude_coordinate_to_string,
    convert_longitude_coordinate_to_string,
)
from kerykeion.utilities import get_houses_list
from scour.scour import scourString


class SouthIndianChartSVG(KerykeionChartSVG):
    """
    South Indian Vedic Chart SVG Generator
    
    Creates traditional South Indian (Tamil/Kerala style) square chart layouts
    commonly used in Vedic astrology. Inherits from KerykeionChartSVG and uses
    a different template to show the square format instead of circular.
    """

    def __init__(self, *args, **kwargs):
        """Initialize with custom template for South Indian chart"""
        super().__init__(*args, **kwargs)
        # Override template path to use South Indian layout
        self.template_path = Path(__file__).parent / "templates" / "chart_south_indian.xml"
    
    def _create_template_dictionary(self):
        """
        Override to add South Indian house and planet data
        """
        # Get the standard template dictionary from parent
        td = super()._create_template_dictionary()
        
        # Add South Indian specific house and planet mappings
        self._add_south_indian_data(td)
        
        return td
    
    def _add_south_indian_data(self, td):
        """
        Add house numbers, planet placements, and signs for South Indian chart
        Based on actual Ascendant position - house numbers start from wherever Asc is located
        """
        # Standard South Indian chart positions (clockwise from bottom-left)
        # These are the 12 physical positions in the chart
        chart_positions = [
            {'x': 30, 'y': 210, 'pos': 'bottom-left'},       # Position 0 - bottom left
            {'x': 90, 'y': 210, 'pos': 'bottom-center-left'}, # Position 1 - bottom center left  
            {'x': 150, 'y': 210, 'pos': 'bottom-center-right'}, # Position 2 - bottom center right
            {'x': 210, 'y': 210, 'pos': 'bottom-right'},     # Position 3 - bottom right
            {'x': 210, 'y': 150, 'pos': 'right-middle'},     # Position 4 - right middle
            {'x': 210, 'y': 90, 'pos': 'right-top'},        # Position 5 - right top
            {'x': 210, 'y': 30, 'pos': 'top-right'},        # Position 6 - top right
            {'x': 150, 'y': 30, 'pos': 'top-center-right'}, # Position 7 - top center right
            {'x': 90, 'y': 30, 'pos': 'top-center-left'},   # Position 8 - top center left
            {'x': 30, 'y': 30, 'pos': 'top-left'},          # Position 9 - top left
            {'x': 30, 'y': 90, 'pos': 'left-top'},          # Position 10 - left top
            {'x': 30, 'y': 150, 'pos': 'left-middle'},      # Position 11 - left middle
        ]
        
        # Find Ascendant sign to determine starting position
        # Get the Ascendant (1st house cusp) sign
        houses_list = get_houses_list(self.user)
        ascendant_sign = None
        
        if houses_list and len(houses_list) > 0:
            first_house = houses_list[0]  # 1st house
            if hasattr(first_house, 'sign'):
                ascendant_sign = first_house.sign
            elif hasattr(first_house, 'sign_name'):
                ascendant_sign = first_house.sign_name
        
        # Map signs to South Indian chart positions
        # In South Indian charts, signs are always in fixed positions
        sign_to_position = {
            'Aries': 0, 'Ari': 0,      # Bottom-left (Mesha)
            'Taurus': 1, 'Tau': 1,     # Bottom-center-left (Vrishabha)
            'Gemini': 2, 'Gem': 2,     # Bottom-center-right (Mithuna)
            'Cancer': 3, 'Can': 3,     # Bottom-right (Karka)
            'Leo': 4, 'Leo': 4,        # Right-middle (Simha)
            'Virgo': 5, 'Vir': 5,      # Right-top (Kanya)
            'Libra': 6, 'Lib': 6,      # Top-right (Tula)
            'Scorpio': 7, 'Sco': 7,    # Top-center-right (Vrishchika)
            'Sagittarius': 8, 'Sag': 8, # Top-center-left (Dhanus)
            'Capricorn': 9, 'Cap': 9,  # Top-left (Makara)
            'Aquarius': 10, 'Aqu': 10,  # Left-top (Kumbha)
            'Pisces': 11, 'Pis': 11,    # Left-middle (Meena)
        }
        
        # Determine where the Ascendant (1st house) should be placed
        ascendant_position = 0  # Default to bottom-left if not found
        if ascendant_sign:
            ascendant_position = sign_to_position.get(ascendant_sign, 0)
            
        # Debug logging
        logging.debug(f"Ascendant sign: {ascendant_sign}")
        logging.debug(f"Ascendant position: {ascendant_position}")
        
        # Create mapping from house number to chart position
        # House 1 (Ascendant) goes to ascendant_position, then houses 2-12 follow consecutively
        house_to_position = {}
        for house_num in range(1, 13):
            position_index = (ascendant_position + house_num - 1) % 12
            house_to_position[house_num] = position_index
        
        # Initialize all chart positions with empty data
        for pos in range(12):
            td[f'si_house_{pos}_number'] = ''
            td[f'si_house_{pos}_planets'] = ''
            td[f'si_house_{pos}_sign'] = ''
            td[f'si_house_{pos}_x'] = str(chart_positions[pos]['x'])
            td[f'si_house_{pos}_y'] = str(chart_positions[pos]['y'])
        
        # Place planets in houses
        planets = [
            ('Sun', self.user.sun, 'Su'),
            ('Moon', self.user.moon, 'Mo'), 
            ('Mercury', self.user.mercury, 'Me'),
            ('Venus', self.user.venus, 'Ve'),
            ('Mars', self.user.mars, 'Ma'),
            ('Jupiter', self.user.jupiter, 'Ju'),
            ('Saturn', self.user.saturn, 'Sa'),
        ]
        
        # Track planets by house
        house_planets = {i: [] for i in range(1, 13)}
        house_signs = {}
        
        for planet_name, planet_obj, planet_abbrev in planets:
            if hasattr(planet_obj, 'house') and hasattr(planet_obj, 'sign'):
                house_num = self._convert_house_to_number(planet_obj.house)
                if house_num and 1 <= house_num <= 12:
                    house_planets[house_num].append(planet_abbrev)
                    if house_num not in house_signs:
                        house_signs[house_num] = self._get_sign_abbreviation(planet_obj.sign)
        
        # Update template data with house numbers, planets and signs at correct positions
        for house_num in range(1, 13):
            chart_pos = house_to_position[house_num]  # Get chart position for this house
            planets_text = ', '.join(house_planets[house_num])
            sign_text = house_signs.get(house_num, '')
            
            # Place house number, planets, and signs at the correct chart position
            td[f'si_house_{chart_pos}_number'] = str(house_num)
            td[f'si_house_{chart_pos}_planets'] = planets_text
            td[f'si_house_{chart_pos}_sign'] = sign_text

    def _convert_house_to_number(self, house_value):
        """Convert house name or number to integer"""
        if isinstance(house_value, int):
            return house_value
        elif isinstance(house_value, str):
            if house_value.isdigit():
                return int(house_value)
            
            house_name_map = {
                "First_House": 1, "first_house": 1, "1st_house": 1,
                "Second_House": 2, "second_house": 2, "2nd_house": 2,
                "Third_House": 3, "third_house": 3, "3rd_house": 3,
                "Fourth_House": 4, "fourth_house": 4, "4th_house": 4,
                "Fifth_House": 5, "fifth_house": 5, "5th_house": 5,
                "Sixth_House": 6, "sixth_house": 6, "6th_house": 6,
                "Seventh_House": 7, "seventh_house": 7, "7th_house": 7,
                "Eighth_House": 8, "eighth_house": 8, "8th_house": 8,
                "Ninth_House": 9, "ninth_house": 9, "9th_house": 9,
                "Tenth_House": 10, "tenth_house": 10, "10th_house": 10,
                "Eleventh_House": 11, "eleventh_house": 11, "11th_house": 11,
                "Twelfth_House": 12, "twelfth_house": 12, "12th_house": 12
            }
            return house_name_map.get(house_value)
        return None
        
    def _get_sign_abbreviation(self, sign_name):
        """Get standard abbreviation for zodiac signs"""
        abbrev_map = {
            "Aries": "Ari", "Ari": "Ari",
            "Taurus": "Tau", "Tau": "Tau", 
            "Gemini": "Gem", "Gem": "Gem",
            "Cancer": "Can", "Can": "Can",
            "Leo": "Leo", "Leo": "Leo",
            "Virgo": "Vir", "Vir": "Vir",
            "Libra": "Lib", "Lib": "Lib", 
            "Scorpio": "Sco", "Sco": "Sco",
            "Sagittarius": "Sag", "Sag": "Sag",
            "Capricorn": "Cap", "Cap": "Cap",
            "Aquarius": "Aqu", "Aqu": "Aqu",
            "Pisces": "Pis", "Pis": "Pis"
        }
        return abbrev_map.get(sign_name, sign_name[:3])

    def makeTemplate(self, minify: bool = False, remove_css_variables = False) -> str:
        """
        Override to use South Indian chart template instead of circular chart.
        """
        from string import Template
        from kerykeion.utilities import inline_css_variables_in_svg
        from scour.scour import scourString
        
        # Create template dictionary using parent class method (which now includes our override)
        td = self._create_template_dictionary()

        # Use South Indian template instead of default chart.xml
        DATA_DIR = Path(__file__).parent
        xml_svg = DATA_DIR / "templates" / "chart_south_indian.xml"

        # read template
        with open(xml_svg, "r", encoding="utf-8", errors="ignore") as f:
            template = Template(f.read()).substitute(td)

        logging.debug(f"Template dictionary keys: {td.keys()}")

        if remove_css_variables:
            template = inline_css_variables_in_svg(template)

        if minify:
            template = scourString(template)

        return template

    @classmethod
    def from_jyotishyamitra(cls, **kwargs):
        """
        Create South Indian chart directly from jyotishyamitra birth data
        
        Args:
            **kwargs: Birth data parameters (name, year, month, etc.)
            
        Returns:
            SouthIndianChartSVG instance
        """
        from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter
        
        # Create astrological subject
        subject = JyotishyamitraAdapter.create_astrological_subject(**kwargs)
        
        # Return chart instance
        return cls(subject)
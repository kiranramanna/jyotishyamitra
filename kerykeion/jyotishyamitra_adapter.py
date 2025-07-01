# -*- coding: utf-8 -*-
"""
    Adapter for Jyotishyamitra data to Kerykeion format
"""

from kerykeion.astrological_subject import AstrologicalSubject
import sys
import os

# Import jyotishyamitra modules
import jyotishyamitra as jm

class JyotishyamitraAdapter:
    """
    Adapter class to convert Jyotishyamitra data to Kerykeion format
    """
    
    @staticmethod
    def validate_and_get_birthdata(name="", gender="", place="", longitude="", 
                                  latitude="", timezone="", year="", month="", 
                                  day="", hour="", minute="", second="0"):
        """
        Validates and gets birthdata from jyotishyamitra
        """
        # Input the birth data
        jm.input_birthdata(
            name=name, 
            gender=gender, 
            place=place, 
            longitude=longitude, 
            lattitude=latitude, 
            timezone=timezone, 
            year=year, 
            month=month, 
            day=day, 
            hour=hour, 
            min=minute, 
            sec=second
        )
        
        # Validate the birth data
        validation_result = jm.validate_birthdata()
        if validation_result != "SUCCESS":
            raise ValueError(f"Birth data validation failed: {validation_result}")
        
        # Get the validated birth data
        return jm.get_birthdata()
    
    @staticmethod
    def create_astrological_subject(birthdata=None, **kwargs):
        """
        Creates an AstrologicalSubject from jyotishyamitra birthdata
        
        If birthdata is not provided, it will use kwargs to input and validate birthdata
        """
        if not birthdata:
            birthdata = JyotishyamitraAdapter.validate_and_get_birthdata(**kwargs)
        
        if not birthdata:
            raise ValueError("No valid birth data provided")
        
        # Extract data from birthdata
        name = birthdata["name"]
        year = int(birthdata["DOB"]["year"])
        month = int(birthdata["DOB"]["month"])
        day = int(birthdata["DOB"]["day"])
        hour = int(birthdata["TOB"]["hour"])
        minute = int(birthdata["TOB"]["min"])
        city = birthdata["POB"]["name"]
        lng = float(birthdata["POB"]["lon"])
        lat = float(birthdata["POB"]["lat"])
        
        # Get timezone value and handle float conversion properly
        tz_value = birthdata["POB"]["timezone"]
        
        # Convert to float first to normalize the value
        try:
            tz_float = float(tz_value)
            
            # Convert float timezone to a standardized string format
            # Remove trailing .0 if it's a whole number
            if tz_float == int(tz_float):
                tz_str = str(int(tz_float))  # Convert -5.0 to "-5"
            else:
                tz_str = str(tz_float)  # Keep decimal points for values like 5.5
        except (ValueError, TypeError):
            # If conversion fails, use the original value as a string
            tz_str = str(tz_value)
        
        # Map timezone values to timezone names
        timezone_map = {
            "-5": "America/New_York",
            "-5.0": "America/New_York",
            "0": "Europe/London",
            "0.0": "Europe/London",
            "10": "Australia/Sydney",
            "10.0": "Australia/Sydney",
            "-8": "America/Los_Angeles",
            "-8.0": "America/Los_Angeles",
            "-7": "America/Denver",
            "-7.0": "America/Denver",
            "-6": "America/Chicago",
            "-6.0": "America/Chicago",
            "1": "Europe/Paris",
            "1.0": "Europe/Paris",
            "2": "Europe/Athens",
            "2.0": "Europe/Athens",
            "5.5": "Asia/Kolkata",
            "5.30": "Asia/Kolkata"
        }
        
        # Look up timezone name from the map
        if tz_str in timezone_map:
            tz_str = timezone_map[tz_str]
        else:
            # Default to UTC if timezone not found in map
            print(f"Warning: Unknown timezone '{tz_str}', defaulting to UTC")
            tz_str = "UTC"
        
        # Create and return AstrologicalSubject
        return AstrologicalSubject(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            city=city,
            lng=lng,
            lat=lat,
            tz_str=tz_str,
            online=False  # We already have coordinates and timezone
        )
    
    @staticmethod
    def generate_chart(birthdata=None, chart_type="Natal", second_subject=None, **kwargs):
        """
        Generates a Kerykeion chart using jyotishyamitra data
        """
        from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
        
        # Create astrological subject
        subject = JyotishyamitraAdapter.create_astrological_subject(birthdata, **kwargs)
        
        # Create chart
        chart = KerykeionChartSVG(subject, chart_type, second_subject)
        
        return chart

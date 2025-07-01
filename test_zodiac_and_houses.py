#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for different zodiac types and house systems using jyotishyamitra and Kerykeion
"""

import os
import sys
from pathlib import Path

try:
    # Import required modules
    import jyotishyamitra as jm
    from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter
    from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
    from kerykeion.astrological_subject import AstrologicalSubject
    
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    def setup_birthdata():
        """Set up and validate birth data"""
        print("Setting up birth data...")
        
        # Input birth data for Swami Vivekananda
        jm.input_birthdata(
            name="Vivekananda, Swami",
            gender="Male",
            place="Kolkata, India",
            longitude="88.36",
            lattitude="22.53",
            timezone="5.883",  # +05:53 converted to decimal hours
            year="1863",
            month="1",
            day="12",
            hour="6",
            min="33",
            sec="0",
            online=False
        )
        
        # Validate birth data
        validation_result = jm.validate_birthdata()
        if validation_result != "SUCCESS":
            print(f"Birth data validation failed: {validation_result}")
            return None
        
        # Get validated birth data
        return jm.get_birthdata()
    
    def test_tropical_zodiac(birthdata):
        """Test creating a chart with tropical zodiac (default)"""
        print("\n1. Testing Tropical Zodiac (Default)...")
        
        try:
            # Create subject using adapter
            subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
            
            # Create chart
            chart = KerykeionChartSVG(subject)
            
            # Set output directory
            chart.output_directory = Path(charts_dir)
            
            # Generate SVG
            chart.makeSVG()
            
            chart_path = os.path.join(charts_dir, f"{subject.name} - Natal Chart.svg")
            print(f"Tropical chart created successfully: {chart_path}")
            return True
        except Exception as e:
            import traceback
            print(f"Error in test_tropical_zodiac: {e}")
            traceback.print_exc()
            return False
    
    def test_sidereal_zodiac(birthdata):
        """Test creating charts with different sidereal zodiac ayanamsas"""
        print("\n2. Testing Sidereal Zodiac with different ayanamsas...")
        
        # List of ayanamsas to test
        ayanamsas = ["LAHIRI", "RAMAN"]
        success = []
        
        for ayanamsa in ayanamsas:
            try:
                print(f"  Testing {ayanamsa} ayanamsa...")
                
                # Create subject from birthdata
                base_subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
                
                # Create new subject with sidereal zodiac
                sidereal_subject = AstrologicalSubject(
                    name=f"{base_subject.name} - {ayanamsa}",
                    year=base_subject.year,
                    month=base_subject.month,
                    day=base_subject.day,
                    hour=base_subject.hour,
                    minute=base_subject.minute,
                    city=base_subject.city,
                    lng=base_subject.lng,
                    lat=base_subject.lat,
                    tz_str=base_subject.tz_str,
                    zodiac_type="Sidereal",
                    sidereal_mode=ayanamsa,
                    online=False
                )
                
                # Create chart
                chart = KerykeionChartSVG(sidereal_subject)
                
                # Set output directory
                chart.output_directory = Path(charts_dir)
                
                # Generate SVG
                chart.makeSVG()
                
                chart_path = os.path.join(charts_dir, f"{sidereal_subject.name} - Natal Chart.svg")
                print(f"  Sidereal chart with {ayanamsa} created successfully: {chart_path}")
                success.append(True)
            except Exception as e:
                import traceback
                print(f"  Error in test_sidereal_zodiac with {ayanamsa}: {e}")
                traceback.print_exc()
                success.append(False)
        
        return all(success)
    
    def test_house_systems(birthdata):
        """Test creating charts with different house systems"""
        print("\n3. Testing different house systems...")
        
        # List of house systems to test
        # Using valid house system identifiers from the error message
        # ('A', 'B', 'C', 'D', 'F', 'H', 'I', 'i', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y')
        house_systems = [
            ("P", "Placidus"),  # P is valid
            ("W", "Whole Sign")  # W is valid
        ]
        
        success = []
        
        for system_id, system_name in house_systems:
            try:
                print(f"  Testing {system_name} ({system_id}) house system...")
                
                # Create subject from birthdata
                base_subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
                
                # Create new subject with specific house system
                house_subject = AstrologicalSubject(
                    name=f"{base_subject.name} - {system_name}",
                    year=base_subject.year,
                    month=base_subject.month,
                    day=base_subject.day,
                    hour=base_subject.hour,
                    minute=base_subject.minute,
                    city=base_subject.city,
                    lng=base_subject.lng,
                    lat=base_subject.lat,
                    tz_str=base_subject.tz_str,
                    houses_system_identifier=system_id,
                    online=False
                )
                
                # Create chart
                chart = KerykeionChartSVG(house_subject)
                
                # Set output directory
                chart.output_directory = Path(charts_dir)
                
                # Generate SVG
                chart.makeSVG()
                
                chart_path = os.path.join(charts_dir, f"{house_subject.name} - Natal Chart.svg")
                print(f"  Chart with {system_name} house system created successfully: {chart_path}")
                success.append(True)
            except Exception as e:
                import traceback
                print(f"  Error in test_house_systems with {system_name}: {e}")
                traceback.print_exc()
                success.append(False)
        
        return all(success)
    
    def main():
        """Main function to run all tests"""
        print("Starting zodiac and house systems tests...")
        
        # Setup birth data
        birthdata = setup_birthdata()
        if not birthdata:
            print("Failed to set up birth data. Exiting.")
            return False
        
        # Run tests
        tropical_success = test_tropical_zodiac(birthdata)
        sidereal_success = test_sidereal_zodiac(birthdata)
        houses_success = test_house_systems(birthdata)
        
        # Report results
        print("\nTest Results:")
        print(f"Tropical Zodiac: {'PASSED' if tropical_success else 'FAILED'}")
        print(f"Sidereal Zodiac: {'PASSED' if sidereal_success else 'FAILED'}")
        print(f"House Systems: {'PASSED' if houses_success else 'FAILED'}")
        
        all_passed = tropical_success and sidereal_success and houses_success
        
        if all_passed:
            print("\nAll tests PASSED!")
            print(f"Charts have been saved to: {os.path.abspath(charts_dir)}")
        else:
            print("\nSome tests FAILED!")
        
        return all_passed

    if __name__ == "__main__":
        success = main()
        sys.exit(0 if success else 1)
        
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)

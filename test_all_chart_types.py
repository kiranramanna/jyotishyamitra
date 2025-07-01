#!/usr/bin/env python3
"""
Comprehensive test script for all chart types available in Kerykeion using jyotishyamitra data.
This script demonstrates the integration between jyotishyamitra and Kerykeion
by generating various types of astrological charts.
"""

import os
import sys
from pathlib import Path
import jyotishyamitra as jm
from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter
from kerykeion.astrological_subject import AstrologicalSubject
from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
from kerykeion.kr_types.kr_literals import ChartType
from kerykeion.kr_types.kr_literals import ZodiacType, SiderealMode

# Create charts directory if it doesn't exist
charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
os.makedirs(charts_dir, exist_ok=True)

def setup_birthdata():
    """Set up and validate birth data for Swami Vivekananda"""
    print("Setting up birth data for Swami Vivekananda...")
    
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

def test_natal_chart(birthdata):
    """Test creating a basic natal chart"""
    print("\n1. Testing Natal Chart (Default)...")
    
    try:
        # Create subject from birthdata
        subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
        
        # Create chart
        chart = KerykeionChartSVG(subject)
        
        # Set output directory
        chart.output_directory = Path(charts_dir)
        
        # Generate SVG
        chart.makeSVG()
        
        chart_path = os.path.join(charts_dir, f"{subject.name} - Natal Chart.svg")
        print(f"Natal chart created successfully: {chart_path}")
        return True
    except Exception as e:
        import traceback
        print(f"Error in test_natal_chart: {e}")
        traceback.print_exc()
        return False

def test_zodiac_types(birthdata):
    """Test creating charts with different zodiac types"""
    print("\n2. Testing Different Zodiac Types...")
    
    zodiac_configs = [
        {"type": "Tropic", "mode": None, "custom": None},
        {"type": "Sidereal", "mode": "LAHIRI", "custom": None},
        {"type": "Sidereal", "mode": "RAMAN", "custom": None},
        {"type": "Sidereal", "mode": "FAGAN_BRADLEY", "custom": None}
        # Custom ayanamsa not supported in this version
    ]
    
    success = []
    
    for config in zodiac_configs:
        zodiac_type = config["type"]
        mode = config["mode"]
        custom_val = config["custom"]
        
        mode_str = mode if mode else ""
        custom_str = f" ({custom_val}°)" if custom_val else ""
        test_name = f"{zodiac_type} {mode_str}{custom_str}"
        
        try:
            print(f"  Testing {test_name}...")
            
            # Create subject from birthdata
            base_subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
            
            # Create new subject with specific zodiac settings
            kwargs = {
                "name": f"{base_subject.name} - {test_name}",
                "year": base_subject.year,
                "month": base_subject.month,
                "day": base_subject.day,
                "hour": base_subject.hour,
                "minute": base_subject.minute,
                "city": base_subject.city,
                "lng": base_subject.lng,
                "lat": base_subject.lat,
                "tz_str": base_subject.tz_str,
                "zodiac_type": zodiac_type,
                "online": False
            }
            
            if mode:
                kwargs["sidereal_mode"] = mode
            
            # Custom ayanamsa not supported in this version
            # if custom_val:
            #     kwargs["custom_ayanamsa"] = custom_val
            
            zodiac_subject = AstrologicalSubject(**kwargs)
            
            # Create chart
            chart = KerykeionChartSVG(zodiac_subject)
            
            # Set output directory
            chart.output_directory = Path(charts_dir)
            
            # Generate SVG
            chart.makeSVG()
            
            chart_path = os.path.join(charts_dir, f"{zodiac_subject.name} - Natal Chart.svg")
            print(f"  {test_name} chart created successfully: {chart_path}")
            success.append(True)
        except Exception as e:
            import traceback
            print(f"  Error in test_zodiac_types with {test_name}: {e}")
            traceback.print_exc()
            success.append(False)
    
    return all(success)

def test_house_systems(birthdata):
    """Test creating charts with different house systems"""
    print("\n3. Testing Different House Systems...")
    
    # List of house systems to test - using valid house system identifiers
    # ('A', 'B', 'C', 'D', 'F', 'H', 'I', 'i', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y')
    house_systems = [
        ("P", "Placidus"),
        ("K", "Koch"),
        ("W", "Whole Sign"),
        ("B", "Alcabitus"),
        ("R", "Regiomontanus"),
        ("C", "Campanus"),
        ("M", "Morinus"),
        ("O", "Porphyrius")
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

def test_chart_types(birthdata):
    """Test creating different types of charts"""
    print("\n4. Testing Different Chart Types...")
    
    # List of chart types to test - using string literals instead of enum values
    chart_types = [
        ("Natal", "Natal"),
        ("Transit", "Transit"),
        ("Synastry", "Synastry")
        # Other chart types may not be supported in this version
    ]
    
    success = []
    
    for chart_type, chart_name in chart_types:
        try:
            print(f"  Testing {chart_name} chart type...")
            
            # Create subject from birthdata
            subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
            
            # For synastry, we need two subjects
            if chart_type == ChartType.SYNASTRY:
                # Create a second subject for synastry
                # Using a different date for the second person
                second_subject = AstrologicalSubject(
                    name="Second Person",
                    year=1980,
                    month=1,
                    day=1,
                    hour=12,
                    minute=0,
                    city="New York",
                    lng=-74.0060,
                    lat=40.7128,
                    tz_str="America/New_York",
                    online=False
                )
                
                # Create chart with both subjects
                chart = KerykeionChartSVG(subject, chart_type=chart_type, second_obj=second_subject)
                output_filename = f"{subject.name} & {second_subject.name} - Synastry Chart"
            else:
                # Create chart with single subject and specified chart type
                chart = KerykeionChartSVG(subject, chart_type=chart_type)
                output_filename = f"{subject.name} - {chart_name} Chart"
            
            # Set output directory
            chart.output_directory = Path(charts_dir)
            
            # Generate SVG
            chart.makeSVG()
            
            chart_path = os.path.join(charts_dir, f"{output_filename}.svg")
            print(f"  {chart_name} chart created successfully: {chart_path}")
            success.append(True)
        except Exception as e:
            import traceback
            print(f"  Error in test_chart_types with {chart_name}: {e}")
            traceback.print_exc()
            success.append(False)
    
    return all(success)

def test_custom_orientation(birthdata):
    """Test creating a chart with alternative orientation"""
    print("\n5. Testing Alternative Chart Orientation...")
    
    try:
        # Create subject from birthdata
        base_subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
        
        # Create new subject with sidereal zodiac
        # This provides an alternative orientation to the tropical zodiac
        custom_subject = AstrologicalSubject(
            name=f"{base_subject.name} - Alternative-Orientation",
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
            sidereal_mode="LAHIRI",  # Using LAHIRI ayanamsa for alternative orientation
            online=False
        )
        
        # Create chart
        chart = KerykeionChartSVG(custom_subject)
        
        # Set output directory
        chart.output_directory = Path(charts_dir)
        
        # Generate SVG
        chart.makeSVG()
        
        chart_path = os.path.join(charts_dir, f"{custom_subject.name} - Natal Chart.svg")
        print(f"Alternative orientation chart created successfully: {chart_path}")
        return True
    except Exception as e:
        import traceback
        print(f"Error in test_custom_orientation: {e}")
        traceback.print_exc()
        return False

def main():
    """Main function to run all tests"""
    print("Starting comprehensive chart tests...")
    
    # Set up birth data
    birthdata = setup_birthdata()
    if not birthdata:
        print("Failed to set up birth data. Exiting.")
        sys.exit(1)
    
    # Run all tests
    test_results = {
        "Natal Chart": test_natal_chart(birthdata),
        "Zodiac Types": test_zodiac_types(birthdata),
        "House Systems": test_house_systems(birthdata),
        "Chart Types": test_chart_types(birthdata),
        "Custom Orientation": test_custom_orientation(birthdata)
    }
    
    # Print test results
    print("\nTest Results:")
    for test_name, result in test_results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
    
    # Check if all tests passed
    all_passed = all(test_results.values())
    if all_passed:
        print("\nAll tests PASSED!")
    else:
        print("\nSome tests FAILED!")
    
    print(f"Charts have been saved to: {charts_dir}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

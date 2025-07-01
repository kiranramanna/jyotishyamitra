#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for jyotishyamitra and kerykeion integration
"""

import os
import sys
import traceback
from pathlib import Path

# Set up proper paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Import jyotishyamitra
    import jyotishyamitra as jm
    print("Successfully imported jyotishyamitra")
    
    # Import the adapter
    from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter
    print("Successfully imported JyotishyamitraAdapter")
    
    from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
    print("Successfully imported KerykeionChartSVG")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)

def test_direct_parameters():
    """Test creating a chart using direct parameters"""
    print("Testing chart creation with direct parameters...")
    
    try:
        chart = JyotishyamitraAdapter.generate_chart(
            name="John Doe",
            gender="Male",
            place="New York",
            longitude="-74.0060",
            latitude="40.7128",
            timezone="-5",
            year="1980",
            month="6",
            day="15",
            hour="10",
            minute="30"
        )
        
        chart.makeSVG()
        print(f"Chart created for John Doe")
        return True
    except Exception as e:
        print(f"Error in test_direct_parameters: {e}")
        traceback.print_exc()
        return False

def test_jyotishyamitra_data():
    """Test creating a chart using existing jyotishyamitra data"""
    print("Testing chart creation with jyotishyamitra data...")
    
    try:
        # Input birth data
        print("Inputting birth data...")
        jm.input_birthdata(
            name="Jane Doe", 
            gender="Female", 
            place="London", 
            longitude="0", 
            lattitude="51.5074", 
            timezone="0", 
            year="1985", 
            month="3", 
            day="22", 
            hour="14", 
            min="45"
        )
        
        # Validate birth data
        print("Validating birth data...")
        validation_result = jm.validate_birthdata()
        print(f"Validation result: {validation_result}")
        if validation_result != "SUCCESS":
            print(f"Birth data validation failed: {validation_result}")
            return False
        
        # Get validated birth data
        print("Getting validated birth data...")
        birthdata = jm.get_birthdata()
        print(f"Birth data: {birthdata}")
        
        # Create chart
        print("Creating chart...")
        chart = JyotishyamitraAdapter.generate_chart(birthdata)
        chart.makeSVG()
        print(f"Chart created for Jane Doe")
        return True
    except Exception as e:
        print(f"Error in test_jyotishyamitra_data: {e}")
        traceback.print_exc()
        return False

def test_convenience_method():
    """Test creating a chart using the convenience method"""
    print("Testing chart creation with convenience method...")
    
    try:
        chart = KerykeionChartSVG.from_jyotishyamitra(
            name="Alex Smith",
            gender="Male",
            place="Sydney",
            longitude="151.2093",
            latitude="-33.8688",
            timezone="10",
            year="1990",
            month="9",
            day="28",
            hour="8",
            minute="15"
        )
        
        chart.makeSVG()
        print(f"Chart created for Alex Smith")
        return True
    except Exception as e:
        print(f"Error in test_convenience_method: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting chart integration tests...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"sys.path: {sys.path}")
    
    success = []
    
    # Run tests
    print("\n1. Testing direct parameters")
    success.append(test_direct_parameters())
    
    print("\n2. Testing jyotishyamitra data")
    success.append(test_jyotishyamitra_data())
    
    print("\n3. Testing convenience method")
    success.append(test_convenience_method())
    
    # Report results
    print("\nTest Results:")
    print(f"Direct parameters test: {'PASSED' if success[0] else 'FAILED'}")
    print(f"Jyotishyamitra data test: {'PASSED' if success[1] else 'FAILED'}")
    print(f"Convenience method test: {'PASSED' if success[2] else 'FAILED'}")
    
    if all(success):
        print("\nAll tests PASSED! Check your home directory for the generated SVG files.")
    else:
        print(f"\nSome tests FAILED! {success.count(True)}/{len(success)} tests passed.")
        sys.exit(1)

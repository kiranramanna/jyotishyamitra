#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test for Kerykeion chart generation
"""

import os
import sys
from pathlib import Path

try:
    # Import Kerykeion modules directly
    from kerykeion.astrological_subject import AstrologicalSubject
    from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
    
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    # Create a simple test subject
    subject = AstrologicalSubject(
        name="Test Subject",
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        city="New York",
        nation="US",
        lng=-74.0060,
        lat=40.7128,
        tz_str="America/New_York",
        online=False
    )
    
    # Create chart
    chart = KerykeionChartSVG(subject)
    
    # Set output directory to the charts directory in the project
    chart.output_directory = Path(charts_dir)
    
    # Generate SVG
    chart.makeSVG()
    
    chart_path = os.path.join(charts_dir, f"{subject.name} - Natal Chart.svg")
    print(f"Chart generated successfully in: {chart_path}") 
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()

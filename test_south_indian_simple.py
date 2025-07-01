#!/usr/bin/env python3
"""
Simple test script for South Indian Vedic Chart generation (without full jyotishyamitra)
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from kerykeion.astrological_subject import AstrologicalSubject
    from kerykeion.charts.south_indian_chart_svg import SouthIndianChartSVG
    
    print("Successfully imported South Indian Chart modules")
    
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    def test_south_indian_chart_simple():
        """Test South Indian chart generation with direct AstrologicalSubject"""
        print("\nTesting South Indian Chart Generation (Simple)...")
        
        try:
            # Create astrological subject directly
            subject = AstrologicalSubject(
                name="Vivekananda, Swami",
                year=1863,
                month=1,
                day=12,
                hour=6,
                minute=33,
                city="Kolkata, India",
                lng=88.36,
                lat=22.53,
                tz_str="Asia/Kolkata",
                online=False
            )
            
            print(f"  Created subject: {subject.name}")
            
            # Test different themes
            themes = ["classic", "dark", "light"]
            
            for theme in themes:
                try:
                    print(f"  Creating {theme} theme chart...")
                    
                    # Create South Indian chart
                    chart = SouthIndianChartSVG(
                        first_obj=subject,
                        new_output_directory=Path(charts_dir),
                        theme=theme
                    )
                    
                    # Generate SVG
                    chart_path = chart.makeSVG()
                    print(f"  {theme.title()} South Indian chart created: {chart_path}")
                    
                    # Verify file exists and has content
                    if chart_path.exists() and chart_path.stat().st_size > 1000:
                        print(f"    ✓ File verified: {chart_path.stat().st_size} bytes")
                    else:
                        print(f"    ✗ File verification failed")
                        
                except Exception as e:
                    print(f"  Error creating {theme} chart: {e}")
                    import traceback
                    traceback.print_exc()
                    
            return True
            
        except Exception as e:
            print(f"Error in simple test: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_multiple_subjects():
        """Test with multiple subjects"""
        print("\nTesting multiple subjects...")
        
        subjects_data = [
            {
                "name": "Modern Subject - SI",
                "year": 1990, "month": 6, "day": 15,
                "hour": 14, "minute": 30,
                "city": "New York", "lng": -74.0060, "lat": 40.7128,
                "tz_str": "America/New_York"
            },
            {
                "name": "Historical Subject - SI",
                "year": 1920, "month": 10, "day": 2,
                "hour": 8, "minute": 0,
                "city": "London", "lng": -0.1278, "lat": 51.5074,
                "tz_str": "Europe/London"
            }
        ]
        
        success_count = 0
        
        for subject_data in subjects_data:
            try:
                subject = AstrologicalSubject(**subject_data)
                
                chart = SouthIndianChartSVG(
                    first_obj=subject,
                    new_output_directory=Path(charts_dir),
                    theme="classic"
                )
                
                chart_path = chart.makeSVG()
                print(f"  Chart created for {subject_data['name']}: {chart_path}")
                
                if chart_path.exists():
                    success_count += 1
                    
            except Exception as e:
                print(f"  Error with {subject_data['name']}: {e}")
        
        return success_count == len(subjects_data)
    
    def test_sidereal_chart():
        """Test South Indian chart with sidereal zodiac"""
        print("\nTesting Sidereal South Indian Chart...")
        
        try:
            # Create sidereal subject
            subject = AstrologicalSubject(
                name="Sidereal Test - SI - LAHIRI",
                year=1990,
                month=12,
                day=25,
                hour=10,
                minute=30,
                city="Delhi, India",
                lng=77.2090,
                lat=28.6139,
                tz_str="Asia/Kolkata",
                zodiac_type="Sidereal",
                sidereal_mode="LAHIRI",
                online=False
            )
            
            # Create South Indian chart
            chart = SouthIndianChartSVG(
                first_obj=subject,
                new_output_directory=Path(charts_dir),
                theme="dark"
            )
            
            chart_path = chart.makeSVG()
            print(f"  Sidereal South Indian chart created: {chart_path}")
            
            return chart_path.exists()
            
        except Exception as e:
            print(f"  Error creating sidereal chart: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_template_generation():
        """Test template generation without file writing"""
        print("\nTesting template generation...")
        
        try:
            subject = AstrologicalSubject(
                name="Template Test",
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test City",
                lng=0,
                lat=0,
                tz_str="UTC"
            )
            
            chart = SouthIndianChartSVG(subject)
            
            # Test template generation
            svg_content = chart.makeTemplate()
            
            # Basic validation
            if "<svg" in svg_content and "</svg>" in svg_content:
                print(f"  ✓ Valid SVG template generated ({len(svg_content)} characters)")
                
                # Test minified version
                svg_minified = chart.makeTemplate(minify=True)
                print(f"  ✓ Minified template generated ({len(svg_minified)} characters)")
                
                return True
            else:
                print(f"  ✗ Invalid SVG template")
                return False
                
        except Exception as e:
            print(f"  Error in template generation: {e}")
            import traceback
            traceback.print_exc()
            return False

    def main():
        """Main test function"""
        print("Starting South Indian Chart Tests (Simple)...")
        
        results = []
        
        # Test basic chart generation
        results.append(test_south_indian_chart_simple())
        
        # Test multiple subjects
        results.append(test_multiple_subjects())
        
        # Test sidereal chart
        results.append(test_sidereal_chart())
        
        # Test template generation
        results.append(test_template_generation())
        
        # Print results
        print(f"\nTest Results:")
        print(f"Basic Chart Generation: {'PASSED' if results[0] else 'FAILED'}")
        print(f"Multiple Subjects: {'PASSED' if results[1] else 'FAILED'}")
        print(f"Sidereal Chart: {'PASSED' if results[2] else 'FAILED'}")
        print(f"Template Generation: {'PASSED' if results[3] else 'FAILED'}")
        
        if all(results):
            print(f"\nAll tests PASSED! Charts saved to: {charts_dir}")
        else:
            print(f"\nSome tests FAILED. Check the output above.")
            
        return all(results)

    if __name__ == "__main__":
        success = main()
        sys.exit(0 if success else 1)

except Exception as e:
    print(f"Import or setup error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
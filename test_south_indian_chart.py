#!/usr/bin/env python3
"""
Test script for South Indian Vedic Chart generation
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import jyotishyamitra as jm
    from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter
    from kerykeion.charts.south_indian_chart_svg import SouthIndianChartSVG
    
    print("Successfully imported South Indian Chart modules")
    
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    def test_south_indian_chart():
        """Test South Indian chart generation"""
        print("\nTesting South Indian Chart Generation...")
        
        # Input birth data for Swami Vivekananda
        jm.input_birthdata(
            name="Vivekananda, Swami",
            gender="Male",
            place="Kolkata, India",
            longitude="88.36",
            lattitude="22.53",
            timezone="5.883",
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
            return False
        
        # Get validated birth data
        birthdata = jm.get_birthdata()
        
        # Create astrological subject
        subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
        
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
                
            except Exception as e:
                print(f"  Error creating {theme} chart: {e}")
                import traceback
                traceback.print_exc()
                
        return True
    
    def test_convenience_method():
        """Test convenience method for South Indian chart"""
        print("\nTesting convenience method...")
        
        try:
            # Test direct creation from birth data
            chart = SouthIndianChartSVG.from_jyotishyamitra(
                name="Test Subject - SI",
                gender="Female",
                place="Mumbai, India", 
                longitude="72.8777",
                latitude="19.0760",
                timezone="5.5",
                year="1980",
                month="6",
                day="15",
                hour="14",
                minute="30"
            )
            
            # Set output directory
            chart.output_directory = Path(charts_dir)
            
            # Generate chart
            chart_path = chart.makeSVG()
            print(f"  Convenience method chart created: {chart_path}")
            return True
            
        except Exception as e:
            print(f"  Error in convenience method: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_sidereal_chart():
        """Test South Indian chart with sidereal zodiac"""
        print("\nTesting Sidereal South Indian Chart...")
        
        try:
            # Input birth data
            jm.input_birthdata(
                name="Sidereal Test - SI",
                gender="Male",
                place="Delhi, India",
                longitude="77.2090",
                lattitude="28.6139", 
                timezone="5.5",
                year="1990",
                month="12",
                day="25",
                hour="10",
                min="30",
                online=False
            )
            
            validation_result = jm.validate_birthdata()
            if validation_result != "SUCCESS":
                print(f"  Validation failed: {validation_result}")
                return False
                
            birthdata = jm.get_birthdata()
            base_subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
            
            # Create sidereal subject
            from kerykeion.astrological_subject import AstrologicalSubject
            sidereal_subject = AstrologicalSubject(
                name="Sidereal Test - SI - LAHIRI",
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
                sidereal_mode="LAHIRI",
                online=False
            )
            
            # Create South Indian chart
            chart = SouthIndianChartSVG(
                first_obj=sidereal_subject,
                new_output_directory=Path(charts_dir),
                theme="classic"
            )
            
            chart_path = chart.makeSVG()
            print(f"  Sidereal South Indian chart created: {chart_path}")
            return True
            
        except Exception as e:
            print(f"  Error creating sidereal chart: {e}")
            import traceback
            traceback.print_exc()
            return False

    def main():
        """Main test function"""
        print("Starting South Indian Chart Tests...")
        
        results = []
        
        # Test basic chart generation
        results.append(test_south_indian_chart())
        
        # Test convenience method
        results.append(test_convenience_method())
        
        # Test sidereal chart
        results.append(test_sidereal_chart())
        
        # Print results
        print(f"\nTest Results:")
        print(f"Basic Chart Generation: {'PASSED' if results[0] else 'FAILED'}")
        print(f"Convenience Method: {'PASSED' if results[1] else 'FAILED'}")
        print(f"Sidereal Chart: {'PASSED' if results[2] else 'FAILED'}")
        
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
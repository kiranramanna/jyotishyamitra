import pytest
import os
import tempfile
from pathlib import Path
import jyotishyamitra as jm
from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter
from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
from kerykeion.astrological_subject import AstrologicalSubject


class TestComprehensiveIntegration:
    """Comprehensive integration tests covering end-to-end workflows"""
    
    @pytest.mark.integration
    def test_complete_workflow_from_input_to_chart(self, charts_dir):
        """Test complete workflow from birth data input to chart generation"""
        # Step 1: Input birth data
        jm.input_birthdata(
            name="Integration Test Subject",
            gender="Male",
            place="Mumbai, India",
            longitude="72.8777",
            lattitude="19.0760",
            timezone="5.5",
            year="1975",
            month="8",
            day="15",
            hour="14",
            min="30",
            sec="0",
            online=False
        )
        
        # Step 2: Validate birth data
        validation_result = jm.validate_birthdata()
        assert validation_result == "SUCCESS"
        
        # Step 3: Get validated birth data
        birthdata = jm.get_birthdata()
        assert birthdata is not None
        
        # Step 4: Create astrological subject
        subject = JyotishyamitraAdapter.create_astrological_subject(birthdata)
        assert subject is not None
        assert subject.name == "Integration Test Subject"
        
        # Step 5: Generate chart
        chart = KerykeionChartSVG(subject)
        chart.output_directory = charts_dir
        chart.makeSVG()
        
        # Step 6: Verify chart file was created
        expected_file = charts_dir / "Integration Test Subject - Natal Chart.svg"
        assert expected_file.exists()
        assert expected_file.stat().st_size > 1000  # Chart should be substantial
    
    @pytest.mark.integration
    def test_multiple_chart_types_workflow(self, sample_birthdata, charts_dir):
        """Test generating multiple chart types for the same subject"""
        base_subject = JyotishyamitraAdapter.create_astrological_subject(sample_birthdata)
        
        # Test different zodiac types
        zodiac_types = [
            ("Tropic", None),
            ("Sidereal", "LAHIRI"),
            ("Sidereal", "RAMAN")
        ]
        
        generated_files = []
        
        for zodiac_type, sidereal_mode in zodiac_types:
            kwargs = {
                "name": f"{base_subject.name} - {zodiac_type}",
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
            
            if sidereal_mode:
                kwargs["sidereal_mode"] = sidereal_mode
                kwargs["name"] += f" {sidereal_mode}"
            
            subject = AstrologicalSubject(**kwargs)
            chart = KerykeionChartSVG(subject)
            chart.output_directory = charts_dir
            chart.makeSVG()
            
            expected_file = charts_dir / f"{subject.name} - Natal Chart.svg"
            assert expected_file.exists()
            generated_files.append(expected_file)
        
        # Verify all files are different (different content)
        file_sizes = [f.stat().st_size for f in generated_files]
        assert len(set(file_sizes)) > 1  # At least some files should be different sizes
    
    @pytest.mark.integration
    def test_house_systems_comparison(self, sample_birthdata, charts_dir):
        """Test generating charts with different house systems and compare"""
        base_subject = JyotishyamitraAdapter.create_astrological_subject(sample_birthdata)
        
        house_systems = [
            ("P", "Placidus"),
            ("K", "Koch"),
            ("W", "Whole Sign"),
            ("R", "Regiomontanus")
        ]
        
        subjects = []
        charts = []
        
        for system_id, system_name in house_systems:
            subject = AstrologicalSubject(
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
            
            chart = KerykeionChartSVG(subject)
            chart.output_directory = charts_dir
            chart.makeSVG()
            
            subjects.append(subject)
            charts.append(chart)
            
            expected_file = charts_dir / f"{subject.name} - Natal Chart.svg"
            assert expected_file.exists()
        
        # Compare house positions between different systems
        for i in range(len(subjects) - 1):
            subject1 = subjects[i]
            subject2 = subjects[i + 1]
            
            # At least some house cusps should be different
            houses_different = False
            house_attrs = [
                'first_house', 'second_house', 'third_house', 'fourth_house',
                'fifth_house', 'sixth_house', 'seventh_house', 'eighth_house',
                'ninth_house', 'tenth_house', 'eleventh_house', 'twelfth_house'
            ]
            
            for house_attr in house_attrs:
                if hasattr(subject1, house_attr) and hasattr(subject2, house_attr):
                    pos1 = getattr(subject1, house_attr).abs_pos
                    pos2 = getattr(subject2, house_attr).abs_pos
                    if abs(pos1 - pos2) > 1:  # Difference > 1 degree
                        houses_different = True
                        break
            
            # Some house systems should produce different results
            if i == 0:  # At least first comparison should show differences
                assert houses_different, f"House systems should produce different results"
    
    @pytest.mark.integration 
    def test_batch_chart_generation(self, charts_dir):
        """Test generating multiple charts in batch"""
        subjects_data = [
            {
                "name": "Batch Subject 1",
                "year": 1980, "month": 1, "day": 1,
                "hour": 10, "minute": 0,
                "city": "New York", "lng": -74.0060, "lat": 40.7128,
                "tz_str": "America/New_York"
            },
            {
                "name": "Batch Subject 2", 
                "year": 1985, "month": 6, "day": 15,
                "hour": 14, "minute": 30,
                "city": "London", "lng": 0.0, "lat": 51.5074,
                "tz_str": "Europe/London"
            },
            {
                "name": "Batch Subject 3",
                "year": 1990, "month": 12, "day": 25,
                "hour": 18, "minute": 45,
                "city": "Tokyo", "lng": 139.6917, "lat": 35.6895,
                "tz_str": "Asia/Tokyo"
            }
        ]
        
        generated_files = []
        
        for subject_data in subjects_data:
            subject = AstrologicalSubject(**subject_data)
            chart = KerykeionChartSVG(subject)
            chart.output_directory = charts_dir
            chart.makeSVG()
            
            expected_file = charts_dir / f"{subject_data['name']} - Natal Chart.svg"
            assert expected_file.exists()
            generated_files.append(expected_file)
        
        # Verify all files were created and are substantial
        for file in generated_files:
            assert file.stat().st_size > 1000
        
        # Verify files are different
        file_contents = []
        for file in generated_files:
            with open(file, 'r') as f:
                content = f.read()[:1000]  # First 1000 chars for comparison
                file_contents.append(content)
        
        # All files should have different content
        assert len(set(file_contents)) == len(file_contents)
    
    @pytest.mark.integration
    def test_error_recovery_workflow(self, charts_dir):
        """Test error recovery in workflow"""
        # Start with invalid data
        jm.input_birthdata(
            name="Error Recovery Test",
            year="invalid"
        )
        
        # Should fail validation
        result = jm.validate_birthdata()
        assert result != "SUCCESS"
        
        # Correct the data
        jm.input_birthdata(
            name="Error Recovery Test",
            gender="Female",
            place="Paris, France",
            longitude="2.3522",
            lattitude="48.8566",
            timezone="1",
            year="1995",
            month="5",
            day="10",
            hour="12",
            min="0",
            online=False
        )
        
        # Should now pass validation
        result = jm.validate_birthdata()
        assert result == "SUCCESS"
        
        # Should be able to generate chart
        birthdata = jm.get_birthdata()
        chart = JyotishyamitraAdapter.generate_chart(birthdata)
        chart.output_directory = charts_dir
        chart.makeSVG()
        
        expected_file = charts_dir / "Error Recovery Test - Natal Chart.svg"
        assert expected_file.exists()
    
    @pytest.mark.integration
    def test_performance_multiple_charts(self, sample_birthdata, charts_dir):
        """Test performance with multiple chart generations"""
        import time
        
        base_subject = JyotishyamitraAdapter.create_astrological_subject(sample_birthdata)
        
        start_time = time.time()
        
        # Generate 5 charts with different house systems
        house_systems = [("P", "Placidus"), ("K", "Koch"), ("W", "Whole Sign"), 
                         ("R", "Regiomontanus"), ("C", "Campanus")]
        
        for system_id, system_name in house_systems:
            subject = AstrologicalSubject(
                name=f"Performance Test - {system_name}",
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
            
            chart = KerykeionChartSVG(subject)
            chart.output_directory = charts_dir
            chart.makeSVG()
            
            expected_file = charts_dir / f"Performance Test - {system_name} - Natal Chart.svg"
            assert expected_file.exists()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete within reasonable time (adjust as needed)
        assert total_time < 60  # 60 seconds for 5 charts
        
        print(f"Generated 5 charts in {total_time:.2f} seconds")
    
    @pytest.mark.integration
    def test_file_system_permissions(self):
        """Test chart generation with various file system scenarios"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test with temporary directory
            subject = AstrologicalSubject(
                name="File System Test",
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
            
            chart = KerykeionChartSVG(subject)
            chart.output_directory = temp_path
            chart.makeSVG()
            
            expected_file = temp_path / "File System Test - Natal Chart.svg"
            assert expected_file.exists()
            
            # Test file is readable
            with open(expected_file, 'r') as f:
                content = f.read()
                assert len(content) > 0
                assert 'svg' in content.lower()  # Should be SVG content
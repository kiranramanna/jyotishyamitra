import pytest
import os
from pathlib import Path
from kerykeion.astrological_subject import AstrologicalSubject
from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter


class TestChartGeneration:
    """Test various chart generation scenarios"""
    
    def test_basic_natal_chart(self, test_subject_data, charts_dir):
        """Test basic natal chart generation"""
        subject = AstrologicalSubject(**test_subject_data)
        chart = KerykeionChartSVG(subject)
        
        chart.output_directory = charts_dir
        chart.makeSVG()
        
        expected_file = charts_dir / "Test Subject - Natal Chart.svg"
        assert expected_file.exists()
        
        # Check file is not empty
        assert expected_file.stat().st_size > 0
    
    def test_different_zodiac_types(self, sample_birthdata, charts_dir):
        """Test charts with different zodiac types"""
        base_subject = JyotishyamitraAdapter.create_astrological_subject(sample_birthdata)
        
        zodiac_configs = [
            {"type": "Tropic", "mode": None},
            {"type": "Sidereal", "mode": "LAHIRI"},
            {"type": "Sidereal", "mode": "RAMAN"},
            {"type": "Sidereal", "mode": "FAGAN_BRADLEY"}
        ]
        
        for config in zodiac_configs:
            zodiac_type = config["type"]
            mode = config["mode"]
            
            test_name = f"{zodiac_type} {mode}" if mode else zodiac_type
            
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
            
            zodiac_subject = AstrologicalSubject(**kwargs)
            chart = KerykeionChartSVG(zodiac_subject)
            chart.output_directory = charts_dir
            chart.makeSVG()
            
            expected_file = charts_dir / f"{zodiac_subject.name} - Natal Chart.svg"
            assert expected_file.exists()
    
    def test_different_house_systems(self, sample_birthdata, charts_dir):
        """Test charts with different house systems"""
        base_subject = JyotishyamitraAdapter.create_astrological_subject(sample_birthdata)
        
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
        
        for system_id, system_name in house_systems:
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
            
            chart = KerykeionChartSVG(house_subject)
            chart.output_directory = charts_dir
            chart.makeSVG()
            
            expected_file = charts_dir / f"{house_subject.name} - Natal Chart.svg"
            assert expected_file.exists()
    
    def test_chart_with_invalid_house_system(self, test_subject_data):
        """Test chart creation with invalid house system"""
        with pytest.raises(Exception):
            test_subject_data["houses_system_identifier"] = "Z"  # Invalid system
            AstrologicalSubject(**test_subject_data)
    
    def test_chart_file_cleanup(self, charts_dir):
        """Test that old chart files can be overwritten"""
        subject = AstrologicalSubject(
            name="Cleanup Test",
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
        chart.output_directory = charts_dir
        
        # Create chart twice
        chart.makeSVG()
        first_time = (charts_dir / "Cleanup Test - Natal Chart.svg").stat().st_mtime
        
        chart.makeSVG()
        second_time = (charts_dir / "Cleanup Test - Natal Chart.svg").stat().st_mtime
        
        # File should have been updated
        assert second_time >= first_time
    
    def test_multiple_subjects_same_session(self, charts_dir):
        """Test creating multiple charts in the same session"""
        subjects_data = [
            {"name": "Subject 1", "year": 1990, "month": 1, "day": 1},
            {"name": "Subject 2", "year": 1991, "month": 2, "day": 2},
            {"name": "Subject 3", "year": 1992, "month": 3, "day": 3}
        ]
        
        for subject_data in subjects_data:
            full_data = {
                **subject_data,
                "hour": 12,
                "minute": 0,
                "city": "Test City",
                "lng": 0,
                "lat": 0,
                "tz_str": "UTC"
            }
            
            subject = AstrologicalSubject(**full_data)
            chart = KerykeionChartSVG(subject)
            chart.output_directory = charts_dir
            chart.makeSVG()
            
            expected_file = charts_dir / f"{subject_data['name']} - Natal Chart.svg"
            assert expected_file.exists()
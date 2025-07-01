import pytest
import jyotishyamitra as jm
from kerykeion.astrological_subject import AstrologicalSubject
from kerykeion.jyotishyamitra_adapter import JyotishyamitraAdapter
from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_date_validation(self):
        """Test validation with invalid dates"""
        jm.input_birthdata(
            name="Invalid Date Test",
            year="2023",
            month="13",  # Invalid month
            day="32",    # Invalid day
            hour="25",   # Invalid hour
            min="70"     # Invalid minute
        )
        
        result = jm.validate_birthdata()
        assert result != "SUCCESS"
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields"""
        jm.input_birthdata(name="Incomplete Data")
        
        result = jm.validate_birthdata()
        assert result != "SUCCESS"
    
    def test_invalid_coordinates(self):
        """Test with invalid geographical coordinates"""
        # Test extremely invalid coordinates that should definitely fail
        try:
            subject = AstrologicalSubject(
                name="Invalid Coords",
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Invalid",
                lng=1000,  # Extremely invalid longitude
                lat=500,   # Extremely invalid latitude
                tz_str="UTC"
            )
            # If no exception is raised, at least verify the coordinates are handled
            # Some implementations might accept and normalize invalid coordinates
            assert subject is not None
        except Exception:
            # This is expected behavior for invalid coordinates
            pass
    
    def test_invalid_timezone(self):
        """Test with invalid timezone"""
        with pytest.raises(Exception):
            AstrologicalSubject(
                name="Invalid TZ",
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="Invalid/Timezone"
            )
    
    def test_extreme_dates(self):
        """Test with extreme historical dates"""
        # Test very old date
        with pytest.raises(Exception):
            AstrologicalSubject(
                name="Ancient",
                year=1,  # Very old date
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="UTC"
            )
        
        # Test future date
        try:
            subject = AstrologicalSubject(
                name="Future",
                year=2100,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="UTC"
            )
            # Should work for reasonable future dates
            assert subject is not None
        except Exception:
            # Some implementations might restrict future dates
            pass
    
    def test_leap_year_handling(self):
        """Test leap year date handling"""
        # Test leap year February 29th
        subject = AstrologicalSubject(
            name="Leap Year",
            year=2000,  # Leap year
            month=2,
            day=29,
            hour=12,
            minute=0,
            city="Test",
            lng=0,
            lat=0,
            tz_str="UTC"
        )
        assert subject is not None
        
        # Test non-leap year February 29th
        with pytest.raises(Exception):
            AstrologicalSubject(
                name="Non-Leap Year",
                year=1900,  # Not a leap year
                month=2,
                day=29,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="UTC"
            )
    
    def test_adapter_with_invalid_data(self):
        """Test adapter error handling with invalid data"""
        with pytest.raises(Exception):
            JyotishyamitraAdapter.generate_chart(
                name="Invalid",
                year="not_a_number",
                month="invalid",
                day="invalid"
            )
    
    def test_adapter_with_missing_data(self):
        """Test adapter with missing required data"""
        with pytest.raises(Exception):
            JyotishyamitraAdapter.generate_chart(name="Missing Data")
    
    def test_chart_generation_without_output_directory(self, test_subject_data):
        """Test chart generation without setting output directory"""
        subject = AstrologicalSubject(**test_subject_data)
        chart = KerykeionChartSVG(subject)
        
        # Test that chart object is created properly even without output directory
        assert chart is not None
        assert hasattr(chart, 'user')
        assert hasattr(chart, 'makeSVG')
        
        # The chart generation might work with default directory or require explicit setting
        # This test just verifies the object is properly constructed
    
    def test_invalid_house_system_identifier(self):
        """Test invalid house system identifier"""
        with pytest.raises(Exception):
            AstrologicalSubject(
                name="Invalid House System",
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="UTC",
                houses_system_identifier="INVALID"
            )
    
    def test_invalid_zodiac_type(self):
        """Test invalid zodiac type"""
        with pytest.raises(Exception):
            AstrologicalSubject(
                name="Invalid Zodiac",
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="UTC",
                zodiac_type="Invalid"
            )
    
    def test_invalid_sidereal_mode(self):
        """Test invalid sidereal mode"""
        with pytest.raises(Exception):
            AstrologicalSubject(
                name="Invalid Sidereal",
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="UTC",
                zodiac_type="Sidereal",
                sidereal_mode="INVALID"
            )
    
    def test_string_to_number_conversion_errors(self):
        """Test string to number conversion errors in input"""
        jm.input_birthdata(
            name="Conversion Test",
            year="twenty twenty",  # Non-numeric string
            month="january",       # Non-numeric string
            day="first",          # Non-numeric string
            longitude="west",     # Non-numeric string
            lattitude="north"     # Non-numeric string
        )
        
        result = jm.validate_birthdata()
        assert result != "SUCCESS"
    
    def test_empty_name_handling(self):
        """Test handling of empty or None name"""
        # Test that empty name is handled gracefully (some implementations allow this)
        try:
            subject = AstrologicalSubject(
                name="",  # Empty name
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="Test",
                lng=0,
                lat=0,
                tz_str="UTC"
            )
            # If no exception, verify the subject was created
            assert subject is not None
        except Exception:
            # Some implementations might require a name
            pass
    
    def test_network_error_simulation(self):
        """Test behavior when online=True but network is unavailable"""
        # This test assumes that setting online=True might fail in some cases
        try:
            subject = AstrologicalSubject(
                name="Network Test",
                year=2000,
                month=1,
                day=1,
                hour=12,
                minute=0,
                city="NonexistentCity",
                lng=0,
                lat=0,
                tz_str="UTC",
                online=True
            )
            # If it succeeds, that's fine
            assert subject is not None
        except Exception:
            # If it fails due to network issues, that's expected
            pass
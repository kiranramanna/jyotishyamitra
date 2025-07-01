import pytest
import jyotishyamitra as jm
from input.birthdata import birthdata, birthdatastr


class TestJyotishyamitraCore:
    """Test core jyotishyamitra functionality"""
    
    def test_input_birthdata_basic(self):
        """Test basic birth data input"""
        jm.input_birthdata(
            name="John Doe",
            gender="Male",
            place="New York",
            longitude="-74.0060",
            lattitude="40.7128",
            timezone="-5",
            year="1980",
            month="6",
            day="15",
            hour="10",
            min="30"
        )
        
        assert birthdatastr["name"] == "John Doe"
        assert birthdatastr["Gender"] == "Male"
        assert birthdatastr["POB"]["name"] == "New York"
        assert birthdatastr["POB"]["lon"] == "-74.0060"
        assert birthdatastr["POB"]["lat"] == "40.7128"
        assert birthdatastr["POB"]["timezone"] == "-5"
        assert birthdatastr["DOB"]["year"] == "1980"
        assert birthdatastr["DOB"]["month"] == "6"
        assert birthdatastr["DOB"]["day"] == "15"
        assert birthdatastr["TOB"]["hour"] == "10"
        assert birthdatastr["TOB"]["min"] == "30"
    
    def test_validate_birthdata_success(self, sample_birthdata):
        """Test successful birth data validation"""
        result = jm.validate_birthdata()
        assert result == "SUCCESS"
    
    def test_validate_birthdata_failure(self):
        """Test birth data validation with invalid data"""
        jm.input_birthdata(
            name="Invalid",
            year="invalid_year"
        )
        result = jm.validate_birthdata()
        assert result != "SUCCESS"
    
    def test_get_birthdata(self, sample_birthdata):
        """Test getting validated birth data"""
        data = jm.get_birthdata()
        assert data is not None
        assert isinstance(data, dict)
        assert "name" in data
        assert "DOB" in data
        assert "TOB" in data
        assert "POB" in data
    
    def test_isfloat_function(self):
        """Test isfloat utility function"""
        assert jm.isfloat("123.45") == 123.45
        assert jm.isfloat("123") == 123.0
        assert jm.isfloat("-123.45") == -123.45
        assert jm.isfloat("not_a_number") is False
        assert jm.isfloat("") is False
    
    def test_month_constants(self):
        """Test month constants"""
        assert jm.January == "1"
        assert jm.February == "2"
        assert jm.March == "3"
        assert jm.April == "4"
        assert jm.May == "5"
        assert jm.June == "6"
        assert jm.July == "7"
        assert jm.August == "8"
        assert jm.September == "9"
        assert jm.October == "10"
        assert jm.November == "11"
        assert jm.December == "12"
    
    def test_partial_birthdata_input(self):
        """Test partial birth data input"""
        jm.input_birthdata(name="Test Name")
        assert birthdatastr["name"] == "Test Name"
        
        jm.input_birthdata(gender="Female")
        assert birthdatastr["Gender"] == "Female"
        assert birthdatastr["name"] == "Test Name"  # Previous value should remain
    
    def test_empty_string_handling(self):
        """Test handling of empty strings in input"""
        original_name = birthdatastr.get("name", "")
        jm.input_birthdata(name="")
        assert birthdatastr.get("name", "") == original_name
    
    def test_string_conversion(self):
        """Test that all inputs are converted to strings"""
        jm.input_birthdata(
            year=1990,
            month=12,
            day=25,
            hour=15,
            min=30
        )
        
        assert birthdatastr["DOB"]["year"] == "1990"
        assert birthdatastr["DOB"]["month"] == "12"
        assert birthdatastr["DOB"]["day"] == "25"
        assert birthdatastr["TOB"]["hour"] == "15"
        assert birthdatastr["TOB"]["min"] == "30"
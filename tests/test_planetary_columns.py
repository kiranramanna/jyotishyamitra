import pytest
import sys
from pathlib import Path

# Add the parent directory to sys.path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import jyotishyamitra as jsm


class TestPlanetaryColumns:
    """Test class for validating the new planetary columns functionality."""
    
    @pytest.fixture
    def sample_birth_data(self):
        """Provides sample birth data for testing."""
        return {
            "name": "Test Person",
            "gender": "male",
            "year": "1990",
            "month": "1",
            "day": "1",
            "hour": "12",
            "min": "0",
            "sec": "0",
            "place": "New Delhi, India",
            "longitude": "+77.2090",
            "lattitude": "+28.6139",
            "timezone": "+5.5"
        }
    
    @pytest.fixture
    def computed_astro_data(self, sample_birth_data):
        """Generates astrological data for testing."""
        # Clear any previous data
        jsm.clear_birthdata()
        
        # Input birth data
        jsm.input_birthdata(**sample_birth_data)
        
        # Validate birth data
        jsm.validate_birthdata()
        
        # Check if birth data is valid
        assert jsm.IsBirthdataValid(), "Birth data validation failed"
        
        # Get validated birth data
        birthdata = jsm.get_birthdata()
        
        # Generate astrological data as dictionary
        return jsm.generate_astrologicalData(birthdata, returnval="ASTRODATA_DICTIONARY")
    
    def test_planetary_columns_presence(self, computed_astro_data):
        """Test that all new planetary columns are present."""
        planets = computed_astro_data["D1"]["planets"]
        expected_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        new_columns = ["longitude", "lon_speed", "latitude", "lat_speed", "distance", "dist_speed"]
        
        for planet_name in expected_planets:
            assert planet_name in planets, f"Missing planet {planet_name}"
            planet_data = planets[planet_name]
            
            for column in new_columns:
                assert column in planet_data, f"Missing column '{column}' in {planet_name} data"
    
    def test_longitude_values(self, computed_astro_data):
        """Test longitude values are within valid range."""
        planets = computed_astro_data["D1"]["planets"]
        
        for planet_name, planet_data in planets.items():
            longitude = planet_data["longitude"]
            assert isinstance(longitude, (int, float)), f"Longitude should be numeric for {planet_name}"
            assert 0 <= longitude < 360, f"Longitude should be 0-360 degrees for {planet_name}, got {longitude}"
    
    def test_longitude_speed_values(self, computed_astro_data):
        """Test longitude speed values are reasonable."""
        planets = computed_astro_data["D1"]["planets"]
        
        for planet_name, planet_data in planets.items():
            lon_speed = planet_data["lon_speed"]
            assert isinstance(lon_speed, (int, float)), f"Longitude speed should be numeric for {planet_name}"
            
            # Check specific reasonable ranges for different planets
            if planet_name == "Moon":
                assert 10 <= abs(lon_speed) <= 15, f"Moon speed should be ~13 deg/day, got {lon_speed}"
            elif planet_name == "Sun":
                assert 0.5 <= lon_speed <= 1.5, f"Sun speed should be ~1 deg/day, got {lon_speed}"
            elif planet_name in ["Rahu", "Ketu"]:
                assert abs(lon_speed) <= 0.1, f"Rahu/Ketu speed should be very slow, got {lon_speed}"
    
    def test_latitude_values(self, computed_astro_data):
        """Test latitude values are within valid range."""
        planets = computed_astro_data["D1"]["planets"]
        
        for planet_name, planet_data in planets.items():
            latitude = planet_data["latitude"]
            assert isinstance(latitude, (int, float)), f"Latitude should be numeric for {planet_name}"
            assert -90 <= latitude <= 90, f"Latitude should be -90 to +90 degrees for {planet_name}, got {latitude}"
            
            # Sun should have very small latitude (close to ecliptic)
            if planet_name == "Sun":
                assert abs(latitude) < 1, f"Sun latitude should be very small, got {latitude}"
    
    def test_distance_values(self, computed_astro_data):
        """Test distance values are reasonable."""
        planets = computed_astro_data["D1"]["planets"]
        
        for planet_name, planet_data in planets.items():
            distance = planet_data["distance"]
            assert isinstance(distance, (int, float)), f"Distance should be numeric for {planet_name}"
            assert distance > 0, f"Distance should be positive for {planet_name}, got {distance}"
            
            # Check reasonable distance ranges
            if planet_name == "Moon":
                assert 0.002 <= distance <= 0.003, f"Moon distance should be ~0.0026 AU, got {distance}"
            elif planet_name == "Sun":
                assert 0.98 <= distance <= 1.02, f"Sun distance should be ~1 AU, got {distance}"
            elif planet_name == "Jupiter":
                assert 4 <= distance <= 7, f"Jupiter distance should be 4-7 AU, got {distance}"
            elif planet_name == "Saturn":
                assert 8 <= distance <= 12, f"Saturn distance should be 8-12 AU, got {distance}"
    
    def test_speed_consistency(self, computed_astro_data):
        """Test that speed values are consistent with retrograde status."""
        planets = computed_astro_data["D1"]["planets"]
        
        for planet_name, planet_data in planets.items():
            retro = planet_data["retro"]
            lon_speed = planet_data["lon_speed"]
            
            # For non-shadow planets, retrograde should correlate with negative longitude speed
            if planet_name not in ["Rahu", "Ketu"]:
                if retro == 1:  # retrograde
                    assert lon_speed < 0, f"Retrograde planet {planet_name} should have negative longitude speed, got {lon_speed}"
                else:  # direct motion
                    assert lon_speed > 0, f"Direct motion planet {planet_name} should have positive longitude speed, got {lon_speed}"
    
    def test_ketu_rahu_relationship(self, computed_astro_data):
        """Test that Ketu and Rahu have opposite positions and speeds."""
        planets = computed_astro_data["D1"]["planets"]
        rahu_data = planets["Rahu"]
        ketu_data = planets["Ketu"]
        
        # Ketu should be 180 degrees opposite to Rahu
        expected_ketu_longitude = (rahu_data["longitude"] + 180) % 360
        assert abs(ketu_data["longitude"] - expected_ketu_longitude) < 0.001, \
            f"Ketu longitude should be 180° from Rahu. Rahu: {rahu_data['longitude']}, Ketu: {ketu_data['longitude']}"
        
        # Ketu longitude speed should be opposite to Rahu
        assert abs(ketu_data["lon_speed"] + rahu_data["lon_speed"]) < 0.001, \
            f"Ketu lon_speed should be opposite to Rahu. Rahu: {rahu_data['lon_speed']}, Ketu: {ketu_data['lon_speed']}"
        
        # Ketu latitude should be opposite to Rahu
        assert abs(ketu_data["latitude"] + rahu_data["latitude"]) < 0.001, \
            f"Ketu latitude should be opposite to Rahu. Rahu: {rahu_data['latitude']}, Ketu: {ketu_data['latitude']}"
    
    def test_data_types(self, computed_astro_data):
        """Test that all new columns have correct data types."""
        planets = computed_astro_data["D1"]["planets"]
        numeric_columns = ["longitude", "lon_speed", "latitude", "lat_speed", "distance", "dist_speed"]
        
        for planet_name, planet_data in planets.items():
            for column in numeric_columns:
                value = planet_data[column]
                assert isinstance(value, (int, float)), \
                    f"Column '{column}' should be numeric for {planet_name}, got {type(value)}: {value}"
                assert not (isinstance(value, float) and (value != value)), \
                    f"Column '{column}' should not be NaN for {planet_name}"
    
    def test_realistic_planetary_positions(self, computed_astro_data):
        """Test that planetary positions are astronomically realistic for the given date."""
        planets = computed_astro_data["D1"]["planets"]
        
        # For January 1, 1990, 12:00 UTC, these are approximate expected ranges
        # These are rough checks to ensure the calculations are reasonable
        
        # Sun should be in Sagittarius/Capricorn around this date
        sun_long = planets["Sun"]["longitude"]
        assert 240 <= sun_long <= 300 or 270 <= sun_long <= 330, \
            f"Sun longitude seems unrealistic for Jan 1, 1990: {sun_long}"
        
        # All planets should have realistic distances
        for planet_name in ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
            distance = planets[planet_name]["distance"]
            assert 0.3 <= distance <= 15, \
                f"{planet_name} distance seems unrealistic: {distance} AU"
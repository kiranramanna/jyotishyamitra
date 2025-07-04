import pytest
import sys
from pathlib import Path
import json

# Add the parent directory to sys.path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import jyotishyamitra as jsm


@pytest.fixture
def vivekananda_birth_data():
    """Provides Swami Vivekananda's birth data."""
    return {
        "name": "Vivekananda, Swami",
        "gender": "male",
        "year": "1863",
        "month": "1",  # January
        "day": "12",
        "hour": "6",
        "min": "33",
        "sec": "0",
        "place": "Kolkata, India",
        "longitude": "+88.36",
        "lattitude": "+22.53", 
        "timezone": "+5.88"  # +05:53 converted to decimal
    }


@pytest.fixture
def vivekananda_astro_data(vivekananda_birth_data):
    """Generates complete astrological data for Swami Vivekananda using Lahiri ayanamsa."""
    # Clear any previous data
    jsm.clear_birthdata()
    
    # Input birth data
    jsm.input_birthdata(**vivekananda_birth_data)
    
    # Validate birth data
    jsm.validate_birthdata()
    
    # Check if birth data is valid
    assert jsm.IsBirthdataValid(), "Birth data validation failed"
    
    # Get validated birth data
    birthdata = jsm.get_birthdata()
    
    # Generate astrological data as dictionary
    astro_data = jsm.generate_astrologicalData(birthdata, returnval="ASTRODATA_DICTIONARY")
    
    return astro_data


class TestSwamiVivekanandaChartLahiri:
    """Test class for validating Swami Vivekananda's chart calculations using Lahiri ayanamsa."""
    
    def test_chart_generation_success(self, vivekananda_astro_data):
        """Test that the chart is generated successfully."""
        assert isinstance(vivekananda_astro_data, dict)
        assert "D1" in vivekananda_astro_data
        assert "user_details" in vivekananda_astro_data
        
    def test_user_details_accuracy(self, vivekananda_astro_data, vivekananda_birth_data):
        """Test that user details match the input birth data."""
        user_details = vivekananda_astro_data["user_details"]
        
        assert user_details["name"] == vivekananda_birth_data["name"]
        
        birth_details = user_details["birthdetails"]
        assert birth_details["DOB"]["year"] == int(vivekananda_birth_data["year"])
        assert birth_details["DOB"]["month"] == int(vivekananda_birth_data["month"])
        assert birth_details["DOB"]["day"] == int(vivekananda_birth_data["day"])
        assert birth_details["TOB"]["hour"] == int(vivekananda_birth_data["hour"])
        assert birth_details["TOB"]["min"] == int(vivekananda_birth_data["min"])
        assert birth_details["POB"]["name"] == vivekananda_birth_data["place"]
        
    def test_lagna_calculation_sagittarius(self, vivekananda_astro_data):
        """Test that Lagna (Ascendant) is correctly calculated as Sagittarius."""
        d1_chart = vivekananda_astro_data["D1"]
        ascendant = d1_chart["ascendant"]
        
        # Check that ascendant sign is Sagittarius (expected for this birth data)
        assert ascendant["sign"] == "Saggitarius"
        assert ascendant["rashi"] == "Dhanu"
        
        # Check exact ascendant nirayana_long position (Sagittarius range: 240-270 degrees)
        ascendant_nirayana = ascendant["nirayana_long"]
        assert abs(ascendant_nirayana - 266.20768646861745) < 0.001, f"Ascendant nirayana_long {ascendant_nirayana} doesn't match expected value"
        
    def test_planetary_positions_d1_chart(self, vivekananda_astro_data):
        """Test planetary positions in D1 chart."""
        d1_chart = vivekananda_astro_data["D1"]
        planets = d1_chart["planets"]
        
        # Verify all 9 planets are present
        expected_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        for planet in expected_planets:
            assert planet in planets, f"Missing planet: {planet}"
            
        # Test specific planetary positions for Vivekananda's chart
        # Sun should be in Sagittarius
        sun = planets["Sun"]
        assert sun["sign"] == "Saggitarius"
        
        # Check exact nirayana_long position
        sun_nirayana = sun["nirayana_long"]
        assert abs(sun_nirayana - 269.4236087970634) < 0.001, f"Sun nirayana_long {sun_nirayana} doesn't match expected value"
        
        # Moon should be in Virgo
        moon = planets["Moon"]
        assert moon["sign"] == "Virgo"
        
        # Check exact nirayana_long position
        moon_nirayana = moon["nirayana_long"]
        assert abs(moon_nirayana - 167.45278994803067) < 0.001, f"Moon nirayana_long {moon_nirayana} doesn't match expected value"
        
        # Jupiter should be in Libra
        jupiter = planets["Jupiter"]
        assert jupiter["sign"] == "Libra"
        
        # Check exact nirayana_long position
        jupiter_nirayana = jupiter["nirayana_long"]
        assert abs(jupiter_nirayana - 184.0138463553967) < 0.001, f"Jupiter nirayana_long {jupiter_nirayana} doesn't match expected value"
        
    def test_moon_nakshatra_hasta(self, vivekananda_astro_data):
        """Test that Moon is in Hasta nakshatra."""
        d1_chart = vivekananda_astro_data["D1"]
        moon = d1_chart["planets"]["Moon"]
        
        # Moon should be in Hasta nakshatra for this birth data
        assert moon["nakshatra"] == "Hasta"
        
    def test_vimshottari_dasha_system(self, vivekananda_astro_data):
        """Test Vimshottari Dasha calculations."""
        dashas = vivekananda_astro_data["Dashas"]
        
        assert "Vimshottari" in dashas
        vimshottari = dashas["Vimshottari"]
        
        # Check that mahadashas are present
        assert "mahadashas" in vimshottari
        
        # For Virgo Moon (Hasta nakshatra), the first Mahadasha should be Moon
        # Note: This depends on the exact implementation and nakshatra pada
        mahadashas = vimshottari["mahadashas"]
        if mahadashas:  # If mahadashas are populated
            # Test the structure exists
            assert isinstance(mahadashas, dict)
            
    def test_planetary_strengths_shadbala(self, vivekananda_astro_data):
        """Test planetary strength calculations (Shadbala)."""
        balas = vivekananda_astro_data["Balas"]
        
        assert "Shadbala" in balas
        shadbala = balas["Shadbala"]
        
        # Check that all required Shadbala components are present
        expected_shadbala_keys = ["Sthanabala", "Digbala", "Kaalabala", "Cheshtabala", "Naisargikabala", "Drikbala", "Total", "Rupas"]
        for key in expected_shadbala_keys:
            assert key in shadbala, f"Missing Shadbala component: {key}"
            
        # Check that planets have Shadbala values
        total_shadbala = shadbala["Total"]
        expected_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        for planet in expected_planets:
            assert planet in total_shadbala, f"Missing Shadbala for planet: {planet}"
            assert isinstance(total_shadbala[planet], (int, float)), f"Invalid Shadbala value for {planet}"
            
    def test_ashtakavarga_calculations(self, vivekananda_astro_data):
        """Test Ashtakavarga calculations."""
        ashtakavarga = vivekananda_astro_data["AshtakaVarga"]
        
        # Ashtakavarga should be a dictionary
        assert isinstance(ashtakavarga, dict)
        
        # Check for Sarvashtakavarga if it exists
        # Note: The exact structure depends on implementation
        
    def test_divisional_charts_present(self, vivekananda_astro_data):
        """Test that divisional charts are generated."""
        # Check for main divisional charts
        expected_charts = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]
        
        for chart in expected_charts:
            assert chart in vivekananda_astro_data, f"Missing divisional chart: {chart}"
            
            # Each chart should have basic structure
            chart_data = vivekananda_astro_data[chart]
            assert "planets" in chart_data
            assert "ascendant" in chart_data
            assert "classifications" in chart_data
            
    def test_navamsa_chart_d9(self, vivekananda_astro_data):
        """Test specific D9 (Navamsa) chart calculations."""
        d9_chart = vivekananda_astro_data["D9"]
        
        assert d9_chart["name"] == "Navamsa"
        assert d9_chart["symbol"] == "D9"
        
        # D9 should have all planets
        planets = d9_chart["planets"]
        expected_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        for planet in expected_planets:
            assert planet in planets
            
    def test_planetary_classifications(self, vivekananda_astro_data):
        """Test planetary classifications (benefics, malefics, etc.)."""
        d1_chart = vivekananda_astro_data["D1"]
        classifications = d1_chart["classifications"]
        
        # Check that classification categories exist
        expected_categories = ["benefics", "malefics", "neutral", "kendra", "trikona", "trik", "upachaya"]
        for category in expected_categories:
            assert category in classifications, f"Missing classification: {category}"
            assert isinstance(classifications[category], list), f"Classification {category} should be a list"
            
    def test_lahiri_ayanamsa_usage(self, vivekananda_astro_data):
        """Test that calculations use Lahiri ayanamsa (implicit test through known values)."""
        # This is tested implicitly through the expected planetary positions
        # Lahiri ayanamsa should give specific planetary positions for Vivekananda's birth data
        
        d1_chart = vivekananda_astro_data["D1"]
        ascendant = d1_chart["ascendant"]
        
        # With Lahiri ayanamsa, the ascendant should be in Sagittarius
        # (this would be different with other ayanamsas)
        assert ascendant["sign"] == "Saggitarius"
        
        # Additional validation through Moon position
        moon = d1_chart["planets"]["Moon"]
        assert moon["sign"] == "Virgo"
        assert moon["nakshatra"] == "Hasta"
        
    @pytest.mark.parametrize("planet_name,expected_sign", [
        ("Sun", "Saggitarius"),
        ("Moon", "Virgo"),
        ("Jupiter", "Libra"),
        ("Mars", "Aries"),
        ("Mercury", "Capricorn"),
        ("Venus", "Capricorn"),
        ("Saturn", "Virgo"),
    ])
    def test_specific_planetary_signs(self, vivekananda_astro_data, planet_name, expected_sign):
        """Test specific planetary sign placements for Vivekananda's chart."""
        d1_chart = vivekananda_astro_data["D1"]
        planet = d1_chart["planets"][planet_name]
        
        assert planet["sign"] == expected_sign, f"{planet_name} should be in {expected_sign}, got {planet['sign']}"
        
    def test_house_placements(self, vivekananda_astro_data):
        """Test house placements and structure."""
        d1_chart = vivekananda_astro_data["D1"]
        
        # Check houses structure exists
        assert "houses" in d1_chart
        houses = d1_chart["houses"]
        
        # Houses should be a list of 12 elements (if populated)
        if houses:
            assert len(houses) == 12, "Should have 12 houses"
            
    def test_json_serialization(self, vivekananda_astro_data):
        """Test that the astrological data can be serialized to JSON."""
        try:
            json_string = json.dumps(vivekananda_astro_data, default=str)
            # Try to parse it back
            parsed_data = json.loads(json_string)
            assert isinstance(parsed_data, dict)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Failed to serialize astrological data to JSON: {e}")
            
    def test_exact_nirayana_long_values(self, vivekananda_astro_data):
        """Test exact nirayana_long values for all planets and ascendant using Lahiri ayanamsa."""
        d1_chart = vivekananda_astro_data["D1"]
        
        # Expected nirayana_long values for Vivekananda's chart
        expected_nirayana_values = {
            "ascendant": 266.20768646861745,
            "Sun": 269.4236087970634,
            "Moon": 167.45278994803067,
            "Mars": 6.32368839459579,
            "Mercury": 281.7734328924978,
            "Jupiter": 184.0138463553967,
            "Venus": 277.10337076675853,
            "Saturn": 163.57360714380087
        }
        
        # Test ascendant
        ascendant = d1_chart["ascendant"]
        ascendant_nirayana = ascendant["nirayana_long"]
        expected_ascendant = expected_nirayana_values["ascendant"]
        assert abs(ascendant_nirayana - expected_ascendant) < 0.001, f"Ascendant nirayana_long {ascendant_nirayana} doesn't match expected {expected_ascendant}"
        
        # Test planets
        planets = d1_chart["planets"]
        for planet_name, expected_value in expected_nirayana_values.items():
            if planet_name == "ascendant":
                continue
                
            planet = planets[planet_name]
            actual_nirayana = planet["nirayana_long"]
            assert abs(actual_nirayana - expected_value) < 0.001, f"{planet_name} nirayana_long {actual_nirayana} doesn't match expected {expected_value}"

    def test_data_completeness(self, vivekananda_astro_data):
        """Test that all major components of astrological data are present."""
        # Top-level structure
        expected_top_level = ["D1", "Balas", "AshtakaVarga", "Dashas", "user_details"]
        for key in expected_top_level:
            assert key in vivekananda_astro_data, f"Missing top-level key: {key}"
            
        # D1 chart completeness
        d1 = vivekananda_astro_data["D1"]
        expected_d1_keys = ["name", "symbol", "ascendant", "planets", "houses", "classifications"]
        for key in expected_d1_keys:
            assert key in d1, f"Missing D1 key: {key}"
            
        # Planets completeness
        planets = d1["planets"]
        for planet_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            planet = planets[planet_name]
            expected_planet_keys = ["name", "symbol", "retro", "pos", "nakshatra", "sign", "rashi", "nirayana_long"]
            for key in expected_planet_keys:
                assert key in planet, f"Missing key '{key}' in planet {planet_name}"
                
        # Ascendant completeness
        ascendant = d1["ascendant"]
        expected_ascendant_keys = ["name", "symbol", "pos", "nakshatra", "sign", "rashi", "nirayana_long"]
        for key in expected_ascendant_keys:
            assert key in ascendant, f"Missing key '{key}' in ascendant"
    
    def test_new_planetary_columns_data_types_and_ranges(self, vivekananda_astro_data):
        """Test the new planetary columns for correct data types and realistic value ranges."""
        d1_chart = vivekananda_astro_data["D1"]
        planets = d1_chart["planets"]
        new_columns = ["longitude", "lon_speed", "latitude", "lat_speed", "distance", "dist_speed"]
        
        # Test all planets have the new columns
        for planet_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            planet_data = planets[planet_name]
            
            # Test presence and data types
            for column in new_columns:
                assert column in planet_data, f"Missing '{column}' in {planet_name} data"
                value = planet_data[column]
                assert isinstance(value, (int, float)), f"Column '{column}' should be numeric for {planet_name}, got {type(value)}"
                assert not (isinstance(value, float) and (value != value)), f"Column '{column}' should not be NaN for {planet_name}"
            
            # Test longitude ranges
            longitude = planet_data["longitude"]
            assert 0 <= longitude < 360, f"Longitude should be 0-360° for {planet_name}, got {longitude}"
            
            # Test latitude ranges
            latitude = planet_data["latitude"]
            assert -90 <= latitude <= 90, f"Latitude should be -90 to +90° for {planet_name}, got {latitude}"
            
            # Test distance is positive
            distance = planet_data["distance"]
            assert distance > 0, f"Distance should be positive for {planet_name}, got {distance}"
        
        # Test specific known values for Vivekananda's chart
        
        # Sun longitude should match the nirayana_long
        sun = planets["Sun"]
        assert abs(sun["longitude"] - sun["nirayana_long"]) < 0.001, "Sun longitude should match nirayana_long"
        
        # Sun should have positive longitude speed (direct motion)
        assert sun["lon_speed"] > 0, f"Sun should have positive longitude speed, got {sun['lon_speed']}"
        assert 0.8 <= sun["lon_speed"] <= 1.2, f"Sun speed should be ~1°/day, got {sun['lon_speed']}"
        
        # Moon should have high longitude speed
        moon = planets["Moon"]
        assert abs(moon["lon_speed"]) > 10, f"Moon should have high speed (~13°/day), got {moon['lon_speed']}"
        
        # Sun distance should be around 1 AU
        assert 0.98 <= sun["distance"] <= 1.02, f"Sun distance should be ~1 AU, got {sun['distance']}"
        
        # Moon distance should be much smaller
        assert 0.002 <= moon["distance"] <= 0.003, f"Moon distance should be ~0.0026 AU, got {moon['distance']}"
        
        # Test Rahu-Ketu relationship
        rahu = planets["Rahu"]
        ketu = planets["Ketu"]
        
        # Ketu longitude should be 180° opposite to Rahu
        expected_ketu_longitude = (rahu["longitude"] + 180) % 360
        assert abs(ketu["longitude"] - expected_ketu_longitude) < 0.001, \
            f"Ketu longitude should be 180° from Rahu. Rahu: {rahu['longitude']}, Ketu: {ketu['longitude']}"
        
        # Ketu longitude speed should be opposite to Rahu
        assert abs(ketu["lon_speed"] + rahu["lon_speed"]) < 0.001, \
            f"Ketu lon_speed should be opposite to Rahu. Rahu: {rahu['lon_speed']}, Ketu: {ketu['lon_speed']}"
import pytest
import json
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the charts dictionary from mod_astrodata for testing
from support.mod_astrodata import charts


class TestJyotishyamitraJsonStructure:
    """Test class for validating jyotishyamitra JSON structure."""
    
    def test_charts_structure(self):
        """Test the basic structure of the charts dictionary."""
        # Verify that the charts dictionary exists and has the expected structure
        assert isinstance(charts, dict), "Charts should be a dictionary"
        
        # Check for D1 chart existence
        assert "D1" in charts, "Missing D1 chart in charts dictionary"
        
        # Check D1 chart structure
        d1_chart = charts["D1"]
        assert isinstance(d1_chart, dict), "D1 chart should be a dictionary"
        
        # Check for key components in D1 chart
        expected_d1_keys = ["planets", "ascendant", "classifications", "name", "symbol", "houses"]
        for key in expected_d1_keys:
            assert key in d1_chart, f"Missing key '{key}' in D1 chart"
            
        # Check for top-level keys in charts
        expected_top_keys = ["Balas", "AshtakaVarga", "Dashas", "user_details"]
        for key in expected_top_keys:
            assert key in charts, f"Missing key '{key}' in charts"
    
    def test_planets_structure(self):
        """Test the structure of planets in the D1 chart."""
        planets = charts["D1"]["planets"]
        assert isinstance(planets, dict), "Planets should be a dictionary"
        
        # Check for all planets
        expected_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        for planet in expected_planets:
            assert planet in planets, f"Missing planet '{planet}' in planets dictionary"
            
            # Check planet structure
            planet_data = planets[planet]
            expected_planet_keys = ["name", "symbol", "retro", "pos", "nakshatra", "sign", "rashi", 
                                   "longitude", "lon_speed", "latitude", "lat_speed", "distance", "dist_speed"]
            for key in expected_planet_keys:
                assert key in planet_data, f"Missing key '{key}' in {planet} data"
    
    def test_planetary_columns_structure(self):
        """Test the new planetary columns for data types and structure."""
        planets = charts["D1"]["planets"]
        
        for planet_name, planet_data in planets.items():
            # Test longitude column
            assert "longitude" in planet_data, f"Missing 'longitude' in {planet_name} data"
            assert isinstance(planet_data["longitude"], (int, float)), f"longitude should be numeric in {planet_name}"
            # Note: Default values are 0.0 in static data structure, so we just check they exist and are numeric
            
            # Test longitude speed column
            assert "lon_speed" in planet_data, f"Missing 'lon_speed' in {planet_name} data"
            assert isinstance(planet_data["lon_speed"], (int, float)), f"lon_speed should be numeric in {planet_name}"
            
            # Test latitude column
            assert "latitude" in planet_data, f"Missing 'latitude' in {planet_name} data"
            assert isinstance(planet_data["latitude"], (int, float)), f"latitude should be numeric in {planet_name}"
            
            # Test latitude speed column
            assert "lat_speed" in planet_data, f"Missing 'lat_speed' in {planet_name} data"
            assert isinstance(planet_data["lat_speed"], (int, float)), f"lat_speed should be numeric in {planet_name}"
            
            # Test distance column
            assert "distance" in planet_data, f"Missing 'distance' in {planet_name} data"
            assert isinstance(planet_data["distance"], (int, float)), f"distance should be numeric in {planet_name}"
            # Note: Default values are 0.0 in static data structure, so we just check they exist and are numeric
            
            # Test distance speed column
            assert "dist_speed" in planet_data, f"Missing 'dist_speed' in {planet_name} data"
            assert isinstance(planet_data["dist_speed"], (int, float)), f"dist_speed should be numeric in {planet_name}"
    
    def test_ascendant_structure(self):
        """Test the structure of the ascendant in the D1 chart."""
        ascendant = charts["D1"]["ascendant"]
        assert isinstance(ascendant, dict), "Ascendant should be a dictionary"
        
        # Check ascendant structure
        expected_keys = ["name", "symbol", "pos", "nakshatra", "sign", "rashi"]
        for key in expected_keys:
            assert key in ascendant, f"Missing key '{key}' in ascendant data"
        
        # Verify ascendant name
        assert ascendant["name"] == "Ascendant", f"Expected name 'Ascendant', got '{ascendant.get('name')}'"
    
    def test_user_details_structure(self):
        """Test the structure of user details in the charts."""
        user_details = charts["user_details"]
        assert isinstance(user_details, dict), "User details should be a dictionary"
        
        # Check user details structure
        assert "name" in user_details, "Missing 'name' in user details"
        assert "birthdetails" in user_details, "Missing 'birthdetails' in user details"
        
        # Check birth details structure
        birth_details = user_details["birthdetails"]
        assert "DOB" in birth_details, "Missing 'DOB' in birth details"
        assert "TOB" in birth_details, "Missing 'TOB' in birth details"
        assert "POB" in birth_details, "Missing 'POB' in birth details"
    
    def test_dashas_structure(self):
        """Test the structure of dashas in the charts."""
        dashas = charts["Dashas"]
        assert isinstance(dashas, dict), "Dashas should be a dictionary"
        
        # Check for Vimshottari dasha
        assert "Vimshottari" in dashas, "Missing 'Vimshottari' in dashas"
        
        # Check Vimshottari structure
        vimshottari = dashas["Vimshottari"]
        expected_keys = ["mahadashas", "antardashas", "paryantardashas", "current"]
        for key in expected_keys:
            assert key in vimshottari, f"Missing key '{key}' in Vimshottari dasha"
    
    def test_balas_structure(self):
        """Test the structure of balas in the charts."""
        balas = charts["Balas"]
        assert isinstance(balas, dict), "Balas should be a dictionary"
        
        # Check for Shadbala
        assert "Shadbala" in balas, "Missing 'Shadbala' in balas"
        
        # Check Shadbala structure
        shadbala = balas["Shadbala"]
        expected_keys = ["Sthanabala", "Digbala", "Kaalabala", "Cheshtabala", "Naisargikabala", "Drikbala"]
        for key in expected_keys:
            assert key in shadbala, f"Missing key '{key}' in Shadbala"
    
    def test_ashtakavarga_structure(self):
        """Test the structure of AshtakaVarga in the charts."""
        ashtakavarga = charts["AshtakaVarga"]
        assert isinstance(ashtakavarga, dict), "AshtakaVarga should be a dictionary"

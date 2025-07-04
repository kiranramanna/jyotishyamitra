#!/usr/bin/env python3
"""
Simple script to validate the structure of jyotishyamitra JSON output.
This script doesn't depend on pytest or any other external libraries.
"""

import json
import os
import sys
from pathlib import Path

def validate_json_structure(json_data):
    """Validate the structure of jyotishyamitra JSON output."""
    print("Validating JSON structure...")
    
    # Check if it's a dictionary
    if not isinstance(json_data, dict):
        print("ERROR: JSON data is not a dictionary")
        return False
    
    # Check for D1 chart
    if "D1" not in json_data:
        print("ERROR: Missing D1 chart in JSON data")
        return False
    
    d1_chart = json_data["D1"]
    
    # Check D1 chart structure
    required_d1_keys = ["planets", "ascendant", "classifications", "name", "symbol", "houses"]
    for key in required_d1_keys:
        if key not in d1_chart:
            print(f"ERROR: Missing '{key}' in D1 chart")
            return False
    
    # Check for top-level keys in main JSON
    required_top_keys = ["Balas", "AshtakaVarga", "Dashas", "user_details"]
    for key in required_top_keys:
        if key not in json_data:
            print(f"ERROR: Missing '{key}' in main JSON")
            return False
    
    # Check planets
    planets = d1_chart["planets"]
    expected_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    for planet in expected_planets:
        if planet not in planets:
            print(f"WARNING: Missing planet '{planet}' in planets data")
    
    # Check a sample planet (Sun)
    if "Sun" in planets:
        sun = planets["Sun"]
        required_sun_keys = ["name", "symbol", "retro", "pos", "nakshatra", "sign", "rashi"]
        for key in required_sun_keys:
            if key not in sun:
                print(f"ERROR: Missing '{key}' in Sun data")
                return False
        
        # Check position data
        pos = sun["pos"]
        required_pos_keys = ["deg", "min", "sec", "dec_deg"]
        for key in required_pos_keys:
            if key not in pos:
                print(f"ERROR: Missing '{key}' in Sun position data")
                return False
    
    # Check ascendant
    ascendant = d1_chart["ascendant"]
    required_asc_keys = ["name", "symbol", "pos", "nakshatra", "sign", "rashi"]
    for key in required_asc_keys:
        if key not in ascendant:
            print(f"ERROR: Missing '{key}' in ascendant data")
            return False
    
    # Check user details
    user_details = json_data["user_details"]
    if "name" not in user_details:
        print("ERROR: Missing 'name' in user details")
        return False
    
    if "birthdetails" not in user_details:
        print("ERROR: Missing 'birthdetails' in user details")
        return False
    
    birth_details = user_details["birthdetails"]
    required_birth_keys = ["DOB", "TOB", "POB"]
    for key in required_birth_keys:
        if key not in birth_details:
            print(f"ERROR: Missing '{key}' in birth details")
            return False
    
    # Check Dashas
    dashas = json_data["Dashas"]
    if "Vimshottari" not in dashas:
        print("ERROR: Missing 'Vimshottari' in dashas")
        return False
    
    vimshottari = dashas["Vimshottari"]
    required_vimshottari_keys = ["mahadashas", "antardashas", "paryantardashas", "current"]
    for key in required_vimshottari_keys:
        if key not in vimshottari:
            print(f"ERROR: Missing '{key}' in Vimshottari dasha")
            return False
    
    # Check Balas
    balas = json_data["Balas"]
    if "Shadbala" not in balas:
        print("ERROR: Missing 'Shadbala' in balas")
        return False
    
    shadbala = balas["Shadbala"]
    required_shadbala_keys = ["Sthanabala", "Digbala", "Kaalabala", "Cheshtabala", "Naisargikabala", "Drikbala"]
    for key in required_shadbala_keys:
        if key not in shadbala:
            print(f"ERROR: Missing '{key}' in Shadbala")
            return False
    
    print("JSON structure validation PASSED!")
    return True

def create_sample_json():
    """Create a sample JSON structure for testing."""
    sample_json = {
        "D1": {
            "planets": {
                "Sun": {
                    "name": "Sun",
                    "symbol": "Su",
                    "retro": 0,
                    "pos": {"deg": 15, "min": 30, "sec": 0, "dec_deg": 15.5},
                    "nakshatra": "Pushya",
                    "sign": "Cancer",
                    "rashi": "Karka"
                },
                "Moon": {
                    "name": "Moon",
                    "symbol": "Mo",
                    "retro": 0,
                    "pos": {"deg": 10, "min": 20, "sec": 0, "dec_deg": 10.33},
                    "nakshatra": "Ardra",
                    "sign": "Gemini",
                    "rashi": "Mithuna"
                },
                "Mars": {
                    "name": "Mars",
                    "symbol": "Ma",
                    "retro": 0,
                    "pos": {"deg": 5, "min": 10, "sec": 0, "dec_deg": 5.17},
                    "nakshatra": "Bharani",
                    "sign": "Aries",
                    "rashi": "Mesha"
                },
                "Mercury": {
                    "name": "Mercury",
                    "symbol": "Me",
                    "retro": 0,
                    "pos": {"deg": 20, "min": 15, "sec": 0, "dec_deg": 20.25},
                    "nakshatra": "Pushya",
                    "sign": "Cancer",
                    "rashi": "Karka"
                },
                "Jupiter": {
                    "name": "Jupiter",
                    "symbol": "Ju",
                    "retro": 0,
                    "pos": {"deg": 25, "min": 45, "sec": 0, "dec_deg": 25.75},
                    "nakshatra": "Purva Phalguni",
                    "sign": "Leo",
                    "rashi": "Simha"
                },
                "Venus": {
                    "name": "Venus",
                    "symbol": "Ve",
                    "retro": 0,
                    "pos": {"deg": 18, "min": 30, "sec": 0, "dec_deg": 18.5},
                    "nakshatra": "Swati",
                    "sign": "Libra",
                    "rashi": "Tula"
                },
                "Saturn": {
                    "name": "Saturn",
                    "symbol": "Sa",
                    "retro": 1,
                    "pos": {"deg": 12, "min": 20, "sec": 0, "dec_deg": 12.33},
                    "nakshatra": "Shravana",
                    "sign": "Capricorn",
                    "rashi": "Makara"
                },
                "Rahu": {
                    "name": "Rahu",
                    "symbol": "Ra",
                    "retro": 1,
                    "pos": {"deg": 8, "min": 15, "sec": 0, "dec_deg": 8.25},
                    "nakshatra": "Ardra",
                    "sign": "Gemini",
                    "rashi": "Mithuna"
                },
                "Ketu": {
                    "name": "Ketu",
                    "symbol": "Ke",
                    "retro": 1,
                    "pos": {"deg": 8, "min": 15, "sec": 0, "dec_deg": 8.25},
                    "nakshatra": "Mula",
                    "sign": "Sagittarius",
                    "rashi": "Dhanu"
                }
            },
            "ascendant": {
                "name": "Ascendant",
                "symbol": "Asc",
                "pos": {"deg": 5, "min": 10, "sec": 0, "dec_deg": 5.17},
                "nakshatra": "Ashwini",
                "sign": "Aries",
                "rashi": "Mesha"
            },
            "classifications": {
                "benefics": ["Jupiter", "Venus", "Moon"],
                "malefics": ["Sun", "Mars", "Saturn", "Rahu", "Ketu"],
                "neutral": ["Mercury"],
                "kendra": [1, 4, 7, 10],
                "trikona": [1, 5, 9],
                "trik": [6, 8, 12],
                "upachaya": [3, 6, 10, 11]
            },
            "houses": [],
            "Balas": {
                "Shadbala": {
                    "Sthanabala": {"Sun": 30, "Moon": 25},
                    "Digbala": {"Sun": 15, "Moon": 20},
                    "Kaalabala": {"Sun": 20, "Moon": 15},
                    "Cheshtabala": {"Sun": 10, "Moon": 5},
                    "Naisargikabala": {"Sun": 60, "Moon": 51.4},
                    "Drikbala": {"Sun": 5, "Moon": 10}
                },
                "Ishtabala": {"Sun": 45, "Moon": 50},
                "Kashtabala": {"Sun": 10, "Moon": 15},
                "BhavaBala": {"Total": [30, 25, 20, 15, 10, 5, 30, 25, 20, 15, 10, 5]}
            },
            "AshtakaVarga": {},
            "Dashas": {
                "Vimshottari": {
                    "mahadashas": {},
                    "antardashas": {},
                    "paryantardashas": {},
                    "current": {
                        "date": "2025-07-01",
                        "dasha": "Venus",
                        "bhukti": "Sun",
                        "paryantardasha": "Moon"
                    }
                }
            },
            "user_details": {
                "name": "Test Person",
                "birthdetails": {
                    "DOB": {
                        "year": 1990,
                        "month": 1,
                        "day": 1
                    },
                    "TOB": {
                        "hour": 12,
                        "min": 0,
                        "sec": 0
                    },
                    "POB": {
                        "name": "New Delhi",
                        "lat": 28.7041,
                        "lon": 77.1025,
                        "timezone": 5.5
                    }
                }
            }
        }
    }
    return sample_json

def main():
    """Main function."""
    print("Jyotishyamitra JSON Structure Validator")
    print("======================================")
    
    # Check if a JSON file was provided
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        if not os.path.exists(json_file):
            print(f"ERROR: File '{json_file}' not found")
            return 1
        
        print(f"Validating JSON file: {json_file}")
        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
            
            if validate_json_structure(json_data):
                print(f"File '{json_file}' has a valid jyotishyamitra JSON structure")
                return 0
            else:
                print(f"File '{json_file}' has an invalid jyotishyamitra JSON structure")
                return 1
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON format in file '{json_file}': {e}")
            return 1
    else:
        # No file provided, use sample data
        print("No JSON file provided. Using sample data...")
        sample_json = create_sample_json()
        
        if validate_json_structure(sample_json):
            # Save sample JSON to a file
            sample_file = "sample_jyotishyamitra.json"
            with open(sample_file, 'w') as f:
                json.dump(sample_json, f, indent=2)
            print(f"Sample JSON saved to '{sample_file}'")
            return 0
        else:
            print("Sample JSON has an invalid structure (this should not happen)")
            return 1

if __name__ == "__main__":
    sys.exit(main())

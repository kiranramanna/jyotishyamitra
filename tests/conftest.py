import pytest
import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jyotishyamitra as jm

@pytest.fixture
def sample_birthdata():
    """Fixture providing validated birth data for Swami Vivekananda"""
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
    
    validation_result = jm.validate_birthdata()
    if validation_result != "SUCCESS":
        pytest.fail(f"Birth data validation failed: {validation_result}")
    
    return jm.get_birthdata()

@pytest.fixture
def charts_dir():
    """Fixture providing charts output directory"""
    charts_dir = Path(__file__).parent.parent / "charts"
    charts_dir.mkdir(exist_ok=True)
    return charts_dir

@pytest.fixture
def test_subject_data():
    """Fixture providing simple test subject data"""
    return {
        "name": "Test Subject",
        "year": 1990,
        "month": 1,
        "day": 1,
        "hour": 12,
        "minute": 0,
        "city": "New York",
        "lng": -74.0060,
        "lat": 40.7128,
        "tz_str": "America/New_York"
    }
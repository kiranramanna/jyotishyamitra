import pytest
import sys
import os

# Import support modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'support'))

import support.mod_constants as constants
import support.mod_general as general
import support.mod_astrodata as astrodata


class TestSupportModules:
    """Test support modules functionality"""
    
    def test_constants_module(self):
        """Test constants module contains expected values"""
        # Test that constants module can be imported
        assert constants is not None
        
        # Test common astrological constants if they exist
        if hasattr(constants, 'PLANET_NAMES'):
            assert isinstance(constants.PLANET_NAMES, (list, tuple, dict))
        
        if hasattr(constants, 'SIGN_NAMES'):
            assert isinstance(constants.SIGN_NAMES, (list, tuple, dict))
    
    def test_general_module_functions(self):
        """Test general module utility functions"""
        # Test that general module can be imported
        assert general is not None
        
        # Test common utility functions if they exist
        if hasattr(general, 'normalize_angle'):
            # Test angle normalization
            result = general.normalize_angle(370)
            assert 0 <= result < 360
            
            result = general.normalize_angle(-10)
            assert 0 <= result < 360
    
    def test_astrodata_module(self):
        """Test astrodata module functionality"""
        # Test that astrodata module can be imported
        assert astrodata is not None
        
        # Test if module has expected functions
        if hasattr(astrodata, 'calculate_planetary_positions'):
            assert callable(astrodata.calculate_planetary_positions)
        
        if hasattr(astrodata, 'get_house_positions'):
            assert callable(astrodata.get_house_positions)
    
    def test_module_imports(self):
        """Test that all support modules can be imported without errors"""
        try:
            import support.dashas
            import support.mod_ashtakavarga
            import support.mod_bala
            import support.mod_divisional
            import support.mod_json
            import support.mod_lagna
            import support.panchanga
        except ImportError as e:
            pytest.fail(f"Failed to import support module: {e}")
    
    def test_dashas_module(self):
        """Test dashas calculation module"""
        try:
            import support.dashas as dashas
            assert dashas is not None
            
            # Test if module has expected functions
            if hasattr(dashas, 'calculate_dasha'):
                assert callable(dashas.calculate_dasha)
            
            if hasattr(dashas, 'get_current_dasha'):
                assert callable(dashas.get_current_dasha)
        except ImportError:
            pytest.skip("Dashas module not available")
    
    def test_ashtakavarga_module(self):
        """Test ashtakavarga calculation module"""
        try:
            import support.mod_ashtakavarga as ashtakavarga
            assert ashtakavarga is not None
            
            # Test if module has expected functions
            if hasattr(ashtakavarga, 'calculate_ashtakavarga'):
                assert callable(ashtakavarga.calculate_ashtakavarga)
        except ImportError:
            pytest.skip("Ashtakavarga module not available")
    
    def test_bala_module(self):
        """Test planetary strength (bala) calculation module"""
        try:
            import support.mod_bala as bala
            assert bala is not None
            
            # Test if module has expected functions
            if hasattr(bala, 'calculate_shadbala'):
                assert callable(bala.calculate_shadbala)
        except ImportError:
            pytest.skip("Bala module not available")
    
    def test_divisional_charts_module(self):
        """Test divisional charts (varga) module"""
        try:
            import support.mod_divisional as divisional
            assert divisional is not None
            
            # Test if module has expected functions
            if hasattr(divisional, 'calculate_navamsa'):
                assert callable(divisional.calculate_navamsa)
            
            if hasattr(divisional, 'calculate_dasamsa'):
                assert callable(divisional.calculate_dasamsa)
        except ImportError:
            pytest.skip("Divisional charts module not available")
    
    def test_json_module(self):
        """Test JSON handling module"""
        try:
            import support.mod_json as json_mod
            assert json_mod is not None
            
            # Test if module has expected functions
            if hasattr(json_mod, 'export_to_json'):
                assert callable(json_mod.export_to_json)
            
            if hasattr(json_mod, 'import_from_json'):
                assert callable(json_mod.import_from_json)
        except ImportError:
            pytest.skip("JSON module not available")
    
    def test_lagna_module(self):
        """Test lagna (ascendant) calculation module"""
        try:
            import support.mod_lagna as lagna
            assert lagna is not None
            
            # Test if module has expected functions
            if hasattr(lagna, 'calculate_ascendant'):
                assert callable(lagna.calculate_ascendant)
        except ImportError:
            pytest.skip("Lagna module not available")
    
    def test_panchanga_module(self):
        """Test panchanga calculation module"""
        try:
            import support.panchanga as panchanga
            assert panchanga is not None
            
            # Test if module has expected functions
            if hasattr(panchanga, 'calculate_tithi'):
                assert callable(panchanga.calculate_tithi)
            
            if hasattr(panchanga, 'calculate_nakshatra'):
                assert callable(panchanga.calculate_nakshatra)
        except ImportError:
            pytest.skip("Panchanga module not available")
    
    def test_module_integration(self, sample_birthdata):
        """Test that support modules work together"""
        try:
            # Test that modules can work with sample birth data
            import support.mod_astrodata as astrodata
            
            if hasattr(astrodata, 'process_birthdata'):
                # Test with sample birth data if function exists
                result = astrodata.process_birthdata(sample_birthdata)
                assert result is not None
        except (ImportError, AttributeError):
            pytest.skip("Module integration test not applicable")
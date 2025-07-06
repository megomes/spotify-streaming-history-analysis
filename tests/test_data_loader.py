"""
Tests for the data loader module.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import json
import os

# Add src to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spotify_analysis.core.data_loader import SpotifyDataLoader


class TestSpotifyDataLoader:
    """Test cases for SpotifyDataLoader."""
    
    def test_loader_initialization(self):
        """Test loader initialization."""
        loader = SpotifyDataLoader()
        assert loader.data_path == Path("Spotify Extended Streaming History")
        assert loader.data is None
        
        # Test with custom path
        custom_path = "/custom/path"
        loader = SpotifyDataLoader(custom_path)
        assert loader.data_path == Path(custom_path)
    
    def test_load_json_file(self):
        """Test loading a single JSON file."""
        loader = SpotifyDataLoader()
        
        # Create temporary test data
        test_data = [
            {"ts": "2023-01-01T10:00:00Z", "ms_played": 180000, "track": "Test Track"},
            {"ts": "2023-01-01T11:00:00Z", "ms_played": 240000, "track": "Test Track 2"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            result = loader._load_json_file(temp_file)
            assert len(result) == 2
            assert result[0]["track"] == "Test Track"
            assert result[1]["track"] == "Test Track 2"
        finally:
            os.unlink(temp_file)
    
    def test_validate_data(self):
        """Test data validation."""
        loader = SpotifyDataLoader()
        
        # Test with valid data
        valid_data = pd.DataFrame({
            'ts': ['2023-01-01T10:00:00Z', '2023-01-01T11:00:00Z'],
            'ms_played': [180000, 240000],
            'master_metadata_track_name': ['Track 1', 'Track 2']
        })
        
        validation = loader.validate_data(valid_data)
        assert validation["valid"] is True
        assert len(validation["missing_columns"]) == 0
        
        # Test with missing columns
        invalid_data = pd.DataFrame({
            'ts': ['2023-01-01T10:00:00Z'],
            'ms_played': [180000]
            # Missing master_metadata_track_name
        })
        
        validation = loader.validate_data(invalid_data)
        assert validation["valid"] is False
        assert "master_metadata_track_name" in validation["missing_columns"]
    
    def test_get_data_info(self):
        """Test getting data information."""
        loader = SpotifyDataLoader()
        
        test_data = pd.DataFrame({
            'ts': ['2023-01-01T10:00:00Z', '2023-01-01T11:00:00Z'],
            'ms_played': [180000, 240000],
            'master_metadata_track_name': ['Track 1', 'Track 2'],
            'master_metadata_album_artist_name': ['Artist 1', 'Artist 2']
        })
        
        info = loader.get_data_info(test_data)
        
        assert info["total_records"] == 2
        assert "ts" in info["columns"]
        assert "ms_played" in info["columns"]
        assert info["unique_tracks"] == 2
        assert info["unique_artists"] == 2


if __name__ == "__main__":
    pytest.main([__file__]) 
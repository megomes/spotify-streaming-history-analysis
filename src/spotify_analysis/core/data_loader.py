"""
Data loading functionality for Spotify streaming history.

This module handles loading and validation of Spotify data files.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


class SpotifyDataLoader:
    """Handles loading and validation of Spotify streaming history data."""
    
    def __init__(self, data_path: Optional[Union[str, Path]] = None):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the directory containing Spotify data files
        """
        self.data_path = Path(data_path) if data_path else Path("Spotify Extended Streaming History")
        self.data = None
        
    def load_from_directory(self, directory_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
        """
        Load all JSON files from a directory.
        
        Args:
            directory_path: Path to directory containing JSON files
            
        Returns:
            DataFrame containing all loaded data
            
        Raises:
            FileNotFoundError: If directory doesn't exist
            ValueError: If no valid JSON files found
        """
        if directory_path:
            self.data_path = Path(directory_path)
            
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_path}")
            
        json_files = list(self.data_path.glob("*.json"))
        
        if not json_files:
            raise ValueError(f"No JSON files found in {self.data_path}")
            
        logger.info(f"Found {len(json_files)} JSON files to load")
        
        all_data = []
        for file_path in json_files:
            try:
                data = self._load_json_file(file_path)
                all_data.extend(data)
                logger.info(f"Loaded {len(data)} records from {file_path.name}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                continue
                
        if not all_data:
            raise ValueError("No data was successfully loaded")
            
        self.data = pd.DataFrame(all_data)
        logger.info(f"Successfully loaded {len(self.data)} total records")
        
        return self.data
    
    def load_from_files(self, file_paths: List[Union[str, Path]]) -> pd.DataFrame:
        """
        Load data from specific file paths.
        
        Args:
            file_paths: List of paths to JSON files
            
        Returns:
            DataFrame containing all loaded data
        """
        all_data = []
        
        for file_path in file_paths:
            try:
                data = self._load_json_file(file_path)
                all_data.extend(data)
                logger.info(f"Loaded {len(data)} records from {Path(file_path).name}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                continue
                
        if not all_data:
            raise ValueError("No data was successfully loaded")
            
        self.data = pd.DataFrame(all_data)
        logger.info(f"Successfully loaded {len(self.data)} total records")
        
        return self.data
    
    def _load_json_file(self, file_path: Union[str, Path]) -> List[Dict]:
        """
        Load a single JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of dictionaries from JSON file
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            return data
        else:
            return [data]
    
    def validate_data(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Union[bool, str]]:
        """
        Validate loaded data for required columns and data types.
        
        Args:
            df: DataFrame to validate (uses self.data if None)
            
        Returns:
            Dictionary with validation results
        """
        if df is None:
            df = self.data
            
        if df is None:
            return {"valid": False, "error": "No data loaded"}
            
        required_columns = ['ts', 'ms_played', 'master_metadata_track_name']
        validation_results = {"valid": True, "missing_columns": [], "data_types": {}}
        
        # Check required columns
        for col in required_columns:
            if col not in df.columns:
                validation_results["missing_columns"].append(col)
                validation_results["valid"] = False
                
        # Check data types
        if 'ts' in df.columns:
            try:
                pd.to_datetime(df['ts'])
                validation_results["data_types"]["timestamp"] = "valid"
            except:
                validation_results["data_types"]["timestamp"] = "invalid"
                validation_results["valid"] = False
                
        if 'ms_played' in df.columns:
            if pd.api.types.is_numeric_dtype(df['ms_played']):
                validation_results["data_types"]["duration"] = "valid"
            else:
                validation_results["data_types"]["duration"] = "invalid"
                validation_results["valid"] = False
                
        return validation_results
    
    def get_data_info(self, df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Get information about the loaded data.
        
        Args:
            df: DataFrame to analyze (uses self.data if None)
            
        Returns:
            Dictionary with data information
        """
        if df is None:
            df = self.data
            
        if df is None:
            return {"error": "No data loaded"}
            
        info = {
            "total_records": len(df),
            "columns": list(df.columns),
            "date_range": None,
            "unique_tracks": None,
            "unique_artists": None
        }
        
        if 'ts' in df.columns:
            try:
                df_copy = df.copy()
                df_copy['ts'] = pd.to_datetime(df_copy['ts'])
                info["date_range"] = {
                    "start": df_copy['ts'].min().date().isoformat(),
                    "end": df_copy['ts'].max().date().isoformat()
                }
            except:
                pass
                
        if 'master_metadata_track_name' in df.columns:
            info["unique_tracks"] = df['master_metadata_track_name'].nunique()
            
        if 'master_metadata_album_artist_name' in df.columns:
            info["unique_artists"] = df['master_metadata_album_artist_name'].nunique()
            
        return info


def load_spotify_data(data_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Convenience function to load Spotify data.
    
    Args:
        data_path: Path to directory containing Spotify data files
        
    Returns:
        DataFrame containing loaded Spotify data
    """
    loader = SpotifyDataLoader(data_path)
    return loader.load_from_directory()


# Backward compatibility
def load_data():
    """Legacy function for Streamlit compatibility."""
    return load_spotify_data() 
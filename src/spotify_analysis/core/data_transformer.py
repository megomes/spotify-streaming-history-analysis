"""
Data transformation and enrichment functionality.

This module handles cleaning, transforming, and enriching Spotify data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SpotifyDataTransformer:
    """Handles transformation and enrichment of Spotify streaming data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the transformer with data.
        
        Args:
            df: DataFrame containing Spotify streaming data
        """
        self.df = df.copy()
        self.transformed_df = None
        
    def process_timestamps(self) -> pd.DataFrame:
        """
        Process and enrich timestamp data.
        
        Returns:
            DataFrame with processed timestamp columns
        """
        if 'ts' not in self.df.columns:
            logger.warning("No timestamp column found")
            return self.df
            
        # Convert to datetime
        self.df['ts'] = pd.to_datetime(self.df['ts'])
        
        # Extract temporal features
        self.df['date'] = self.df['ts'].dt.date
        self.df['hour'] = self.df['ts'].dt.hour
        self.df['day_of_week'] = self.df['ts'].dt.day_name()
        self.df['month'] = self.df['ts'].dt.month
        self.df['year'] = self.df['ts'].dt.year
        self.df['is_weekend'] = self.df['ts'].dt.weekday >= 5
        
        # Time periods
        self.df['time_period'] = self.df['hour'].apply(self._categorize_time_period)
        self.df['is_sleep_time'] = self.df['hour'].apply(self._is_sleep_time)
        
        logger.info("Timestamp processing completed")
        return self.df
    
    def _categorize_time_period(self, hour: int) -> str:
        """Categorize hour into time periods."""
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
    
    def _is_sleep_time(self, hour: int) -> bool:
        """Determine if hour is during typical sleep time."""
        return 22 <= hour or hour <= 6
    
    def process_duration(self) -> pd.DataFrame:
        """
        Process and analyze duration data.
        
        Returns:
            DataFrame with processed duration columns
        """
        if 'ms_played' not in self.df.columns:
            logger.warning("No duration column found")
            return self.df
            
        # Convert to seconds and minutes
        self.df['seconds_played'] = self.df['ms_played'] / 1000
        self.df['minutes_played'] = self.df['seconds_played'] / 60
        
        # Calculate completion percentage (if track duration available)
        if 'master_metadata_track_duration_ms' in self.df.columns:
            self.df['completion_percentage'] = (
                self.df['ms_played'] / self.df['master_metadata_track_duration_ms'] * 100
            )
            self.df['completion_percentage'] = self.df['completion_percentage'].clip(0, 100)
            
            # Categorize completion
            self.df['completion_category'] = self.df['completion_percentage'].apply(
                lambda x: 'Complete' if x >= 90 else 'Partial' if x >= 30 else 'Skip'
            )
        
        logger.info("Duration processing completed")
        return self.df
    
    def clean_duplicates(self) -> pd.DataFrame:
        """
        Remove duplicate records.
        
        Returns:
            DataFrame with duplicates removed
        """
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        final_count = len(self.df)
        
        removed_count = initial_count - final_count
        logger.info(f"Removed {removed_count} duplicate records")
        
        return self.df
    
    def add_session_features(self) -> pd.DataFrame:
        """
        Add session-based features.
        
        Returns:
            DataFrame with session features
        """
        if 'ts' not in self.df.columns:
            logger.warning("No timestamp column found for session analysis")
            return self.df
            
        # Sort by timestamp
        self.df = self.df.sort_values('ts')
        
        # Calculate time between plays
        self.df['time_since_last_play'] = self.df['ts'].diff().dt.total_seconds()
        
        # Define session breaks (30 minutes of inactivity)
        session_break_threshold = 30 * 60  # 30 minutes in seconds
        self.df['new_session'] = (
            self.df['time_since_last_play'] > session_break_threshold
        )
        
        # Create session IDs
        self.df['session_id'] = self.df['new_session'].cumsum()
        
        # Session features
        session_features = self.df.groupby('session_id').agg({
            'ts': ['min', 'max', 'count'],
            'ms_played': 'sum',
            'master_metadata_track_name': 'nunique'
        }).reset_index()
        
        session_features.columns = [
            'session_id', 'session_start', 'session_end', 'plays_in_session',
            'total_duration_ms', 'unique_tracks'
        ]
        
        # Merge back to main dataframe
        self.df = self.df.merge(session_features, on='session_id', how='left')
        
        logger.info("Session features added")
        return self.df
    
    def add_artist_features(self) -> pd.DataFrame:
        """
        Add artist-based features.
        
        Returns:
            DataFrame with artist features
        """
        if 'master_metadata_album_artist_name' not in self.df.columns:
            logger.warning("No artist column found")
            return self.df
            
        # Artist play counts
        artist_counts = self.df['master_metadata_album_artist_name'].value_counts()
        self.df = self.df.merge(
            artist_counts.reset_index().rename(columns={
                'master_metadata_album_artist_name': 'artist',
                'count': 'artist_play_count'
            }),
            left_on='master_metadata_album_artist_name',
            right_on='artist',
            how='left'
        ).drop('artist', axis=1)
        
        # Artist loyalty (percentage of plays by top artist)
        total_plays = len(self.df)
        top_artist_plays = artist_counts.iloc[0] if len(artist_counts) > 0 else 0
        self.df['artist_loyalty'] = top_artist_plays / total_plays
        
        logger.info("Artist features added")
        return self.df
    
    def add_track_features(self) -> pd.DataFrame:
        """
        Add track-based features.
        
        Returns:
            DataFrame with track features
        """
        if 'master_metadata_track_name' not in self.df.columns:
            logger.warning("No track column found")
            return self.df
            
        # Track play counts
        track_counts = self.df['master_metadata_track_name'].value_counts()
        self.df = self.df.merge(
            track_counts.reset_index().rename(columns={
                'master_metadata_track_name': 'track',
                'count': 'track_play_count'
            }),
            left_on='master_metadata_track_name',
            right_on='track',
            how='left'
        ).drop('track', axis=1)
        
        # Track popularity (relative to most played track)
        max_plays = track_counts.max() if len(track_counts) > 0 else 1
        self.df['track_popularity'] = self.df['track_play_count'] / max_plays
        
        logger.info("Track features added")
        return self.df
    
    def transform(self, steps: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Apply all transformations.
        
        Args:
            steps: List of transformation steps to apply. If None, applies all.
            
        Returns:
            Transformed DataFrame
        """
        if steps is None:
            steps = [
                'process_timestamps',
                'process_duration', 
                'clean_duplicates',
                'add_session_features',
                'add_artist_features',
                'add_track_features'
            ]
        
        for step in steps:
            if hasattr(self, step):
                method = getattr(self, step)
                self.df = method()
                logger.info(f"Applied transformation: {step}")
            else:
                logger.warning(f"Unknown transformation step: {step}")
        
        self.transformed_df = self.df.copy()
        return self.df
    
    def get_transformation_summary(self) -> Dict:
        """
        Get summary of transformations applied.
        
        Returns:
            Dictionary with transformation summary
        """
        if self.transformed_df is None:
            return {"error": "No transformations applied"}
            
        summary = {
            "original_records": len(self.df),
            "final_records": len(self.transformed_df),
            "columns_added": list(set(self.transformed_df.columns) - set(self.df.columns)),
            "date_range": None,
            "unique_artists": None,
            "unique_tracks": None
        }
        
        if 'ts' in self.transformed_df.columns:
            summary["date_range"] = {
                "start": self.transformed_df['ts'].min().date().isoformat(),
                "end": self.transformed_df['ts'].max().date().isoformat()
            }
            
        if 'master_metadata_album_artist_name' in self.transformed_df.columns:
            summary["unique_artists"] = self.transformed_df['master_metadata_album_artist_name'].nunique()
            
        if 'master_metadata_track_name' in self.transformed_df.columns:
            summary["unique_tracks"] = self.transformed_df['master_metadata_track_name'].nunique()
            
        return summary


def transform_data(df: pd.DataFrame, steps: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Convenience function to transform Spotify data.
    
    Args:
        df: DataFrame containing Spotify data
        steps: List of transformation steps to apply
        
    Returns:
        Transformed DataFrame
    """
    transformer = SpotifyDataTransformer(df)
    return transformer.transform(steps)


# Backward compatibility
def transform_data_legacy():
    """Legacy function for Streamlit compatibility."""
    # This would need to be implemented based on the original transform.py
    pass 
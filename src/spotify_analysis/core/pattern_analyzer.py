"""
Pattern analysis functionality for Spotify data.

This module analyzes temporal patterns, sleep-related behaviors, and listening habits.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SpotifyPatternAnalyzer:
    """Analyzes patterns in Spotify streaming data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the analyzer with data.
        
        Args:
            df: DataFrame containing processed Spotify data
        """
        self.df = df.copy()
        self.analysis_results = {}
        
    def analyze_temporal_patterns(self) -> Dict:
        """
        Analyze temporal listening patterns.
        
        Returns:
            Dictionary with temporal analysis results
        """
        if 'ts' not in self.df.columns:
            return {"error": "No timestamp data available"}
            
        results = {
            "hourly_distribution": {},
            "daily_distribution": {},
            "monthly_distribution": {},
            "peak_hours": [],
            "sleep_time_analysis": {}
        }
        
        # Hourly distribution
        if 'hour' in self.df.columns:
            hourly_counts = self.df['hour'].value_counts().sort_index()
            results["hourly_distribution"] = hourly_counts.to_dict()
            
            # Peak hours (top 3)
            peak_hours = hourly_counts.nlargest(3)
            results["peak_hours"] = [
                {"hour": int(hour), "plays": int(count)} 
                for hour, count in peak_hours.items()
            ]
        
        # Daily distribution
        if 'day_of_week' in self.df.columns:
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_counts = self.df['day_of_week'].value_counts()
            daily_counts = daily_counts.reindex(day_order, fill_value=0)
            results["daily_distribution"] = daily_counts.to_dict()
        
        # Monthly distribution
        if 'month' in self.df.columns:
            monthly_counts = self.df['month'].value_counts().sort_index()
            results["monthly_distribution"] = monthly_counts.to_dict()
        
        # Sleep time analysis
        if 'is_sleep_time' in self.df.columns:
            sleep_data = self.df[self.df['is_sleep_time']]
            wake_data = self.df[~self.df['is_sleep_time']]
            
            results["sleep_time_analysis"] = {
                "sleep_time_plays": len(sleep_data),
                "wake_time_plays": len(wake_data),
                "sleep_percentage": len(sleep_data) / len(self.df) * 100,
                "avg_sleep_session_duration": sleep_data['minutes_played'].mean() if 'minutes_played' in sleep_data.columns else 0,
                "avg_wake_session_duration": wake_data['minutes_played'].mean() if 'minutes_played' in wake_data.columns else 0
            }
        
        self.analysis_results["temporal"] = results
        return results
    
    def analyze_artist_patterns(self) -> Dict:
        """
        Analyze artist listening patterns.
        
        Returns:
            Dictionary with artist analysis results
        """
        if 'master_metadata_album_artist_name' not in self.df.columns:
            return {"error": "No artist data available"}
            
        results = {
            "top_artists": [],
            "artist_loyalty": {},
            "artist_time_preferences": {}
        }
        
        # Top artists
        artist_counts = self.df['master_metadata_album_artist_name'].value_counts()
        results["top_artists"] = [
            {"artist": artist, "plays": int(count)}
            for artist, count in artist_counts.head(10).items()
        ]
        
        # Artist loyalty analysis
        total_plays = len(self.df)
        if total_plays > 0:
            top_artist_plays = artist_counts.iloc[0] if len(artist_counts) > 0 else 0
            results["artist_loyalty"] = {
                "top_artist_percentage": top_artist_plays / total_plays * 100,
                "top_5_artists_percentage": artist_counts.head(5).sum() / total_plays * 100,
                "diversity_score": len(artist_counts) / total_plays * 1000  # Artists per 1000 plays
            }
        
        # Artist time preferences
        if 'time_period' in self.df.columns:
            artist_time = self.df.groupby(['master_metadata_album_artist_name', 'time_period']).size().reset_index(name='plays')
            artist_time_pivot = artist_time.pivot(
                index='master_metadata_album_artist_name', 
                columns='time_period', 
                values='plays'
            ).fillna(0)
            
            # Find preferred time for each artist
            for artist in artist_time_pivot.index:
                preferred_time = artist_time_pivot.loc[artist].idxmax()
                results["artist_time_preferences"][artist] = preferred_time
        
        self.analysis_results["artist"] = results
        return results
    
    def analyze_track_patterns(self) -> Dict:
        """
        Analyze track listening patterns.
        
        Returns:
            Dictionary with track analysis results
        """
        if 'master_metadata_track_name' not in self.df.columns:
            return {"error": "No track data available"}
            
        results = {
            "top_tracks": [],
            "repeat_listening": {},
            "track_completion": {}
        }
        
        # Top tracks
        track_counts = self.df['master_metadata_track_name'].value_counts()
        results["top_tracks"] = [
            {"track": track, "plays": int(count)}
            for track, count in track_counts.head(10).items()
        ]
        
        # Repeat listening analysis
        total_plays = len(self.df)
        unique_tracks = len(track_counts)
        results["repeat_listening"] = {
            "avg_plays_per_track": total_plays / unique_tracks if unique_tracks > 0 else 0,
            "most_repeated_track": track_counts.iloc[0] if len(track_counts) > 0 else 0,
            "single_play_tracks": (track_counts == 1).sum(),
            "repeat_percentage": (track_counts > 1).sum() / unique_tracks * 100 if unique_tracks > 0 else 0
        }
        
        # Track completion analysis
        if 'completion_percentage' in self.df.columns:
            completion_stats = self.df['completion_percentage'].describe()
            results["track_completion"] = {
                "avg_completion": completion_stats['mean'],
                "median_completion": completion_stats['50%'],
                "complete_plays": (self.df['completion_percentage'] >= 90).sum(),
                "partial_plays": ((self.df['completion_percentage'] >= 30) & (self.df['completion_percentage'] < 90)).sum(),
                "skipped_plays": (self.df['completion_percentage'] < 30).sum()
            }
        
        self.analysis_results["track"] = results
        return results
    
    def analyze_session_patterns(self) -> Dict:
        """
        Analyze listening session patterns.
        
        Returns:
            Dictionary with session analysis results
        """
        if 'session_id' not in self.df.columns:
            return {"error": "No session data available"}
            
        results = {
            "session_statistics": {},
            "session_duration_patterns": {},
            "session_time_patterns": {}
        }
        
        # Session statistics
        session_stats = self.df.groupby('session_id').agg({
            'ts': ['min', 'max', 'count'],
            'ms_played': 'sum',
            'master_metadata_track_name': 'nunique'
        }).reset_index()
        
        session_stats.columns = [
            'session_id', 'start_time', 'end_time', 'plays', 
            'total_duration_ms', 'unique_tracks'
        ]
        
        session_stats['duration_minutes'] = session_stats['total_duration_ms'] / 1000 / 60
        
        results["session_statistics"] = {
            "total_sessions": len(session_stats),
            "avg_session_duration": session_stats['duration_minutes'].mean(),
            "avg_plays_per_session": session_stats['plays'].mean(),
            "avg_tracks_per_session": session_stats['unique_tracks'].mean(),
            "longest_session": session_stats['duration_minutes'].max(),
            "shortest_session": session_stats['duration_minutes'].min()
        }
        
        # Session duration patterns
        duration_bins = [0, 5, 15, 30, 60, float('inf')]
        duration_labels = ['0-5min', '5-15min', '15-30min', '30-60min', '60min+']
        session_stats['duration_category'] = pd.cut(
            session_stats['duration_minutes'], 
            bins=duration_bins, 
            labels=duration_labels
        )
        
        duration_dist = session_stats['duration_category'].value_counts()
        results["session_duration_patterns"] = duration_dist.to_dict()
        
        # Session time patterns
        if 'hour' in self.df.columns:
            session_hour_dist = self.df.groupby('session_id')['hour'].agg(['min', 'max', 'mean']).reset_index()
            results["session_time_patterns"] = {
                "avg_session_start_hour": session_hour_dist['min'].mean(),
                "avg_session_end_hour": session_hour_dist['max'].mean(),
                "avg_session_hour": session_hour_dist['mean'].mean()
            }
        
        self.analysis_results["session"] = results
        return results
    
    def analyze_sleep_patterns(self) -> Dict:
        """
        Analyze sleep-related listening patterns.
        
        Returns:
            Dictionary with sleep analysis results
        """
        if 'is_sleep_time' not in self.df.columns:
            return {"error": "No sleep time data available"}
            
        results = {
            "sleep_time_listening": {},
            "sleep_time_preferences": {},
            "sleep_quality_indicators": {}
        }
        
        sleep_data = self.df[self.df['is_sleep_time']]
        wake_data = self.df[~self.df['is_sleep_time']]
        
        # Sleep time listening statistics
        results["sleep_time_listening"] = {
            "total_sleep_plays": len(sleep_data),
            "sleep_plays_percentage": len(sleep_data) / len(self.df) * 100,
            "avg_sleep_session_length": sleep_data['minutes_played'].mean() if 'minutes_played' in sleep_data.columns else 0,
            "sleep_sessions_count": sleep_data['session_id'].nunique() if 'session_id' in sleep_data.columns else 0
        }
        
        # Sleep time preferences
        if 'master_metadata_album_artist_name' in sleep_data.columns:
            sleep_artists = sleep_data['master_metadata_album_artist_name'].value_counts().head(5)
            results["sleep_time_preferences"]["top_sleep_artists"] = [
                {"artist": artist, "plays": int(count)}
                for artist, count in sleep_artists.items()
            ]
        
        if 'master_metadata_track_name' in sleep_data.columns:
            sleep_tracks = sleep_data['master_metadata_track_name'].value_counts().head(5)
            results["sleep_time_preferences"]["top_sleep_tracks"] = [
                {"track": track, "plays": int(count)}
                for track, count in sleep_tracks.items()
            ]
        
        # Sleep quality indicators
        if 'completion_percentage' in sleep_data.columns:
            sleep_completion = sleep_data['completion_percentage'].mean()
            wake_completion = wake_data['completion_percentage'].mean()
            
            results["sleep_quality_indicators"] = {
                "sleep_completion_rate": sleep_completion,
                "wake_completion_rate": wake_completion,
                "completion_difference": sleep_completion - wake_completion,
                "sleep_skip_rate": (sleep_data['completion_percentage'] < 30).sum() / len(sleep_data) * 100 if len(sleep_data) > 0 else 0
            }
        
        self.analysis_results["sleep"] = results
        return results
    
    def analyze_all_patterns(self) -> Dict:
        """
        Run all pattern analyses.
        
        Returns:
            Dictionary with all analysis results
        """
        logger.info("Starting comprehensive pattern analysis...")
        
        all_results = {
            "temporal": self.analyze_temporal_patterns(),
            "artist": self.analyze_artist_patterns(),
            "track": self.analyze_track_patterns(),
            "session": self.analyze_session_patterns(),
            "sleep": self.analyze_sleep_patterns()
        }
        
        # Add summary statistics
        all_results["summary"] = {
            "total_records": len(self.df),
            "analysis_timestamp": datetime.now().isoformat(),
            "data_quality": self._assess_data_quality()
        }
        
        self.analysis_results = all_results
        return all_results
    
    def _assess_data_quality(self) -> Dict:
        """Assess the quality of the data."""
        quality_metrics = {
            "completeness": {},
            "consistency": {},
            "coverage": {}
        }
        
        # Completeness
        total_records = len(self.df)
        required_columns = ['ts', 'ms_played', 'master_metadata_track_name']
        
        for col in required_columns:
            if col in self.df.columns:
                non_null_count = self.df[col].notna().sum()
                quality_metrics["completeness"][col] = non_null_count / total_records * 100
            else:
                quality_metrics["completeness"][col] = 0
        
        # Consistency
        if 'ts' in self.df.columns:
            try:
                pd.to_datetime(self.df['ts'])
                quality_metrics["consistency"]["timestamp_format"] = "valid"
            except:
                quality_metrics["consistency"]["timestamp_format"] = "invalid"
        
        if 'ms_played' in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df['ms_played']):
                quality_metrics["consistency"]["duration_format"] = "valid"
            else:
                quality_metrics["consistency"]["duration_format"] = "invalid"
        
        # Coverage
        if 'ts' in self.df.columns:
            date_range = self.df['ts'].max() - self.df['ts'].min()
            quality_metrics["coverage"]["date_range_days"] = date_range.days
        
        return quality_metrics


def analyze_patterns(df: pd.DataFrame) -> Dict:
    """
    Convenience function to analyze patterns in Spotify data.
    
    Args:
        df: DataFrame containing processed Spotify data
        
    Returns:
        Dictionary with pattern analysis results
    """
    analyzer = SpotifyPatternAnalyzer(df)
    return analyzer.analyze_all_patterns() 
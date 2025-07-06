"""
Spotify Analysis Sleep Apnea - Main Application

A comprehensive Streamlit application for analyzing Spotify streaming history
with focus on sleep-related listening patterns.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from spotify_analysis.core.data_loader import load_spotify_data, SpotifyDataLoader
    from spotify_analysis.core.data_transformer import transform_data, SpotifyDataTransformer
    from spotify_analysis.core.pattern_analyzer import analyze_patterns, SpotifyPatternAnalyzer
except ImportError:
    # Fallback to old modules if new structure not available
    from modules.load import load_data
    from modules.transform import transform_data
    from modules.visualize import visualize_data


def main():
    """Main application function."""
    st.set_page_config(
        page_title="Spotify Analysis Sleep Apnea",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1DB954;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .sidebar-section {
        margin: 1rem 0;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🎵 Spotify Analysis Sleep Apnea</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📊 Analysis Dashboard")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose Analysis Section:",
        [
            "🏠 Overview",
            "📂 Data Loading", 
            "🔄 Data Transformation",
            "📈 Pattern Analysis",
            "📊 Visualizations",
            "💤 Sleep Analysis",
            "📋 Reports"
        ]
    )
    
    # Initialize session state
    if 'spotify_data' not in st.session_state:
        st.session_state.spotify_data = None
    if 'transformed_data' not in st.session_state:
        st.session_state.transformed_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Page routing
    if page == "🏠 Overview":
        show_overview()
    elif page == "📂 Data Loading":
        show_data_loading()
    elif page == "🔄 Data Transformation":
        show_data_transformation()
    elif page == "📈 Pattern Analysis":
        show_pattern_analysis()
    elif page == "📊 Visualizations":
        show_visualizations()
    elif page == "💤 Sleep Analysis":
        show_sleep_analysis()
    elif page == "📋 Reports":
        show_reports()


def show_overview():
    """Show project overview and status."""
    st.header("🏠 Project Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### About This Project
        
        This application analyzes your Spotify streaming history to understand 
        music listening patterns, with particular focus on sleep-related behaviors.
        
        **Key Features:**
        - 📊 **Temporal Analysis**: When you listen to music throughout the day
        - 💤 **Sleep Pattern Analysis**: Music listening during sleep hours
        - 🎵 **Genre & Artist Analysis**: How your taste varies by time
        - 📈 **Behavioral Patterns**: Skip rates, session duration, repeat listening
        - 📅 **Seasonal Trends**: How habits change over time
        
        **Research Focus:**
        - Sleep apnea and music listening patterns
        - Night-time music preferences
        - Behavioral correlation analysis
        """)
    
    with col2:
        st.markdown("### 📊 Current Status")
        
        # Data status
        if st.session_state.spotify_data is not None:
            st.success(f"✅ Data Loaded: {len(st.session_state.spotify_data)} records")
        else:
            st.warning("⚠️ No data loaded")
            
        if st.session_state.transformed_data is not None:
            st.success("✅ Data Transformed")
        else:
            st.info("ℹ️ Data not yet transformed")
            
        if st.session_state.analysis_results is not None:
            st.success("✅ Analysis Complete")
        else:
            st.info("ℹ️ Analysis not yet run")
    
    # Quick start guide
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    1. **Load Data**: Go to "Data Loading" section and load your Spotify data
    2. **Transform Data**: Process and enrich your data in "Data Transformation"
    3. **Analyze Patterns**: Run comprehensive analysis in "Pattern Analysis"
    4. **Explore Visualizations**: View interactive charts in "Visualizations"
    5. **Sleep Analysis**: Focus on sleep-related patterns
    6. **Generate Reports**: Export your findings
    """)


def show_data_loading():
    """Show data loading interface."""
    st.header("📂 Data Loading")
    
    st.markdown("""
    ### How to Get Your Spotify Data
    
    1. **Request Data**: Go to [Spotify Privacy Settings](https://www.spotify.com/account/privacy/)
    2. **Download**: Request "Extended streaming history"
    3. **Extract**: Place JSON files in the `Spotify Extended Streaming History/` folder
    4. **Load**: Use the interface below to load your data
    """)
    
    # Data loading options
    load_option = st.radio(
        "Choose loading method:",
        ["Use Default Directory", "Upload Files", "Manual Path"]
    )
    
    if load_option == "Use Default Directory":
        if st.button("🔄 Load from Default Directory"):
            try:
                data = load_spotify_data()
                st.session_state.spotify_data = data
                st.success(f"✅ Successfully loaded {len(data)} records!")
                st.dataframe(data.head())
            except Exception as e:
                st.error(f"❌ Error loading data: {str(e)}")
                
    elif load_option == "Upload Files":
        uploaded_files = st.file_uploader(
            "Choose Spotify JSON files",
            type=['json'],
            accept_multiple_files=True
        )
        
        if uploaded_files and st.button("🔄 Load Uploaded Files"):
            try:
                # Implementation for uploaded files
                st.info("Upload functionality to be implemented")
            except Exception as e:
                st.error(f"❌ Error loading files: {str(e)}")
                
    elif load_option == "Manual Path":
        data_path = st.text_input("Enter data directory path:")
        if data_path and st.button("🔄 Load from Path"):
            try:
                data = load_spotify_data(data_path)
                st.session_state.spotify_data = data
                st.success(f"✅ Successfully loaded {len(data)} records!")
                st.dataframe(data.head())
            except Exception as e:
                st.error(f"❌ Error loading data: {str(e)}")
    
    # Show loaded data info
    if st.session_state.spotify_data is not None:
        st.subheader("📊 Loaded Data Information")
        df = st.session_state.spotify_data
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            if 'ts' in df.columns:
                st.metric("Date Range", f"{df['ts'].min()[:10]} to {df['ts'].max()[:10]}")
        
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10))


def show_data_transformation():
    """Show data transformation interface."""
    st.header("🔄 Data Transformation")
    
    if st.session_state.spotify_data is None:
        st.warning("⚠️ Please load data first in the Data Loading section.")
        return
    
    st.success(f"✅ Data available for transformation: {len(st.session_state.spotify_data)} records")
    
    # Transformation options
    st.subheader("⚙️ Transformation Options")
    
    transform_steps = st.multiselect(
        "Select transformations to apply:",
        [
            "Process Timestamps",
            "Process Duration", 
            "Clean Duplicates",
            "Add Session Features",
            "Add Artist Features",
            "Add Track Features"
        ],
        default=["Process Timestamps", "Process Duration", "Clean Duplicates"]
    )
    
    if st.button("🚀 Apply Transformations"):
        with st.spinner("Transforming data..."):
            try:
                transformed_data = transform_data(
                    st.session_state.spotify_data, 
                    steps=transform_steps
                )
                st.session_state.transformed_data = transformed_data
                st.success("✅ Data transformation completed!")
                
                # Show transformation summary
                st.subheader("📊 Transformation Summary")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Original Records", len(st.session_state.spotify_data))
                    st.metric("Final Records", len(transformed_data))
                
                with col2:
                    new_columns = set(transformed_data.columns) - set(st.session_state.spotify_data.columns)
                    st.metric("New Columns", len(new_columns))
                    st.metric("Columns Total", len(transformed_data.columns))
                
                st.subheader("🆕 New Columns Added")
                st.write(list(new_columns))
                
            except Exception as e:
                st.error(f"❌ Error during transformation: {str(e)}")
    
    # Show transformed data
    if st.session_state.transformed_data is not None:
        st.subheader("📋 Transformed Data Preview")
        st.dataframe(st.session_state.transformed_data.head(10))


def show_pattern_analysis():
    """Show pattern analysis interface."""
    st.header("📈 Pattern Analysis")
    
    if st.session_state.transformed_data is None:
        st.warning("⚠️ Please transform data first in the Data Transformation section.")
        return
    
    st.success(f"✅ Transformed data available: {len(st.session_state.transformed_data)} records")
    
    # Analysis options
    st.subheader("🔍 Analysis Options")
    
    analysis_types = st.multiselect(
        "Select analysis types:",
        [
            "Temporal Patterns",
            "Artist Patterns", 
            "Track Patterns",
            "Session Patterns",
            "Sleep Patterns"
        ],
        default=["Temporal Patterns", "Artist Patterns", "Track Patterns"]
    )
    
    if st.button("🔬 Run Analysis"):
        with st.spinner("Analyzing patterns..."):
            try:
                results = analyze_patterns(st.session_state.transformed_data)
                st.session_state.analysis_results = results
                st.success("✅ Pattern analysis completed!")
                
                # Show key insights
                st.subheader("💡 Key Insights")
                
                if "temporal" in results:
                    temp_results = results["temporal"]
                    if "peak_hours" in temp_results:
                        peak_hours = temp_results["peak_hours"]
                        st.write("**Peak Listening Hours:**")
                        for peak in peak_hours[:3]:
                            st.write(f"- Hour {peak['hour']}: {peak['plays']} plays")
                
                if "artist" in results:
                    artist_results = results["artist"]
                    if "top_artists" in artist_results:
                        top_artists = artist_results["top_artists"]
                        st.write("**Top Artists:**")
                        for artist in top_artists[:3]:
                            st.write(f"- {artist['artist']}: {artist['plays']} plays")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
    
    # Show analysis results
    if st.session_state.analysis_results is not None:
        st.subheader("📊 Analysis Results")
        
        # Create tabs for different analysis types
        tabs = st.tabs(["Temporal", "Artist", "Track", "Session", "Sleep"])
        
        results = st.session_state.analysis_results
        
        with tabs[0]:
            if "temporal" in results:
                st.json(results["temporal"])
        
        with tabs[1]:
            if "artist" in results:
                st.json(results["artist"])
        
        with tabs[2]:
            if "track" in results:
                st.json(results["track"])
        
        with tabs[3]:
            if "session" in results:
                st.json(results["session"])
        
        with tabs[4]:
            if "sleep" in results:
                st.json(results["sleep"])


def show_visualizations():
    """Show visualization interface."""
    st.header("📊 Visualizations")
    
    if st.session_state.transformed_data is None:
        st.warning("⚠️ Please transform data first.")
        return
    
    st.info("📈 Visualization features coming soon!")
    st.write("This section will include interactive charts and graphs.")


def show_sleep_analysis():
    """Show sleep-specific analysis."""
    st.header("💤 Sleep Analysis")
    
    if st.session_state.analysis_results is None:
        st.warning("⚠️ Please run pattern analysis first.")
        return
    
    st.info("🌙 Sleep analysis features coming soon!")
    st.write("This section will focus on sleep-related listening patterns.")


def show_reports():
    """Show reporting interface."""
    st.header("📋 Reports")
    
    if st.session_state.analysis_results is None:
        st.warning("⚠️ Please run analysis first.")
        return
    
    st.info("📄 Report generation features coming soon!")
    st.write("This section will allow you to export analysis results.")


if __name__ == "__main__":
    main() 
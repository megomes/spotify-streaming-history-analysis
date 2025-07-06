import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def visualize_data():
    """
    Visualizes data with charts and analysis
    """
    st.subheader("3. Data Visualization")
    
    # Check if there's data to visualize
    if 'transformed_data' in st.session_state:
        df = st.session_state['transformed_data']
        st.success(f"✅ Transformed data available: {len(df)} records")
    elif 'spotify_data' in st.session_state:
        df = st.session_state['spotify_data']
        st.success(f"✅ Original data available: {len(df)} records")
    else:
        st.warning("⚠️ No data available for visualization!")
        st.write("Load and transform data first in the previous sections.")
        return None
    
    # Show basic data information
    st.subheader("📋 Data Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        st.metric("Total Columns", len(df.columns))
    
    with col3:
        if 'ts' in df.columns:
            date_range = f"{df['ts'].min().date()} to {df['ts'].max().date()}"
            st.metric("Period", date_range)
    
    # Select visualization type
    st.subheader("📈 Visualization Types")
    
    viz_type = st.selectbox(
        "Choose visualization type:",
        [
            "Overview",
            "Temporal Analysis",
            "Top Tracks and Artists",
            "Hourly Patterns",
            "Duration Analysis",
            "Custom Data"
        ]
    )
    
    if viz_type == "Overview":
        show_overview(df)
    elif viz_type == "Temporal Analysis":
        show_temporal_analysis(df)
    elif viz_type == "Top Tracks and Artists":
        show_top_analysis(df)
    elif viz_type == "Hourly Patterns":
        show_hourly_patterns(df)
    elif viz_type == "Duration Analysis":
        show_duration_analysis(df)
    elif viz_type == "Custom Data":
        show_custom_analysis(df)

def show_overview(df):
    """Shows data overview"""
    st.subheader("👀 Overview")
    
    # Basic statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Basic Statistics:**")
        if 'ms_played' in df.columns:
            st.write(f"- Total time listened: {df['ms_played'].sum() / 1000 / 60 / 60:.1f} hours")
            st.write(f"- Average per session: {df['ms_played'].mean() / 1000 / 60:.1f} minutes")
        
        if 'ts' in df.columns:
            st.write(f"- Period: {df['ts'].min().date()} to {df['ts'].max().date()}")
            st.write(f"- Unique days: {df['ts'].dt.date.nunique()}")
    
    with col2:
        st.write("**Available Columns:**")
        for col in df.columns:
            st.write(f"- {col}")
    
    # Temporal line chart (if timestamp exists)
    if 'ts' in df.columns:
        st.subheader("📅 Activity Over Time")
        
        # Group by date
        daily_activity = df.groupby(df['ts'].dt.date).size().reset_index(name='count')
        daily_activity['date'] = pd.to_datetime(daily_activity['ts'])
        
        fig = px.line(daily_activity, x='date', y='count', 
                     title="Number of Plays per Day")
        fig.update_layout(xaxis_title="Date", yaxis_title="Number of Plays")
        st.plotly_chart(fig, use_container_width=True)

def show_temporal_analysis(df):
    """Shows temporal data analysis"""
    st.subheader("🕐 Temporal Analysis")
    
    if 'ts' not in df.columns:
        st.warning("⚠️ Temporal data not available!")
        return
    
    # Convert timestamp if necessary
    if not pd.api.types.is_datetime64_any_dtype(df['ts']):
        df['ts'] = pd.to_datetime(df['ts'])
    
    # Analysis by hour of day
    if 'hour' not in df.columns:
        df['hour'] = df['ts'].dt.hour
    
    hourly_activity = df.groupby('hour').size().reset_index(name='count')
    
    fig = px.bar(hourly_activity, x='hour', y='count',
                 title="Activity by Hour of Day")
    fig.update_layout(xaxis_title="Hour", yaxis_title="Number of Plays")
    st.plotly_chart(fig, use_container_width=True)
    
    # Analysis by day of week
    if 'day_of_week' not in df.columns:
        df['day_of_week'] = df['ts'].dt.day_name()
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_activity = df.groupby('day_of_week').size().reset_index(name='count')
    daily_activity['day_of_week'] = pd.Categorical(daily_activity['day_of_week'], categories=day_order, ordered=True)
    daily_activity = daily_activity.sort_values('day_of_week')
    
    fig2 = px.bar(daily_activity, x='day_of_week', y='count',
                  title="Activity by Day of Week")
    fig2.update_layout(xaxis_title="Day of Week", yaxis_title="Number of Plays")
    st.plotly_chart(fig2, use_container_width=True)

def show_top_analysis(df):
    """Shows top tracks and artists"""
    st.subheader("🏆 Top Tracks and Artists")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'master_metadata_track_name' in df.columns:
            st.write("**Top 10 Tracks:**")
            top_tracks = df['master_metadata_track_name'].value_counts().head(10)
            
            fig = px.bar(x=top_tracks.values, y=top_tracks.index, orientation='h',
                        title="Top 10 Most Played Tracks")
            fig.update_layout(xaxis_title="Number of Plays", yaxis_title="Track")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'master_metadata_album_artist_name' in df.columns:
            st.write("**Top 10 Artists:**")
            top_artists = df['master_metadata_album_artist_name'].value_counts().head(10)
            
            fig2 = px.bar(x=top_artists.values, y=top_artists.index, orientation='h',
                         title="Top 10 Most Played Artists")
            fig2.update_layout(xaxis_title="Number of Plays", yaxis_title="Artist")
            st.plotly_chart(fig2, use_container_width=True)

def show_hourly_patterns(df):
    """Shows hourly patterns"""
    st.subheader("🌙 Hourly Patterns")
    
    if 'ts' not in df.columns:
        st.warning("⚠️ Temporal data not available!")
        return
    
    # Convert timestamp if necessary
    if not pd.api.types.is_datetime64_any_dtype(df['ts']):
        df['ts'] = pd.to_datetime(df['ts'])
    
    if 'hour' not in df.columns:
        df['hour'] = df['ts'].dt.hour
    
    # Heatmap of activity by hour and day of week
    if 'day_of_week' not in df.columns:
        df['day_of_week'] = df['ts'].dt.day_name()
    
    hourly_daily = df.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
    
    # Pivot to create heatmap
    heatmap_data = hourly_daily.pivot(index='day_of_week', columns='hour', values='count')
    
    fig = px.imshow(heatmap_data, 
                    title="Activity Heatmap by Hour and Day of Week",
                    labels=dict(x="Hour", y="Day of Week", color="Plays"))
    st.plotly_chart(fig, use_container_width=True)

def show_duration_analysis(df):
    """Shows track duration analysis"""
    st.subheader("⏱️ Duration Analysis")
    
    if 'ms_played' not in df.columns:
        st.warning("⚠️ Duration data not available!")
        return
    
    # Convert to minutes
    df['minutes_played'] = df['ms_played'] / 1000 / 60
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Duration distribution
        fig = px.histogram(df, x='minutes_played', nbins=50,
                          title="Track Duration Distribution")
        fig.update_layout(xaxis_title="Duration (minutes)", yaxis_title="Frequency")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Duration box plot
        fig2 = px.box(df, y='minutes_played',
                      title="Track Duration Box Plot")
        fig2.update_layout(yaxis_title="Duration (minutes)")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Duration statistics
    st.write("**Duration Statistics:**")
    st.write(f"- Mean: {df['minutes_played'].mean():.2f} minutes")
    st.write(f"- Median: {df['minutes_played'].median():.2f} minutes")
    st.write(f"- Minimum: {df['minutes_played'].min():.2f} minutes")
    st.write(f"- Maximum: {df['minutes_played'].max():.2f} minutes")

def show_custom_analysis(df):
    """Allows custom analysis"""
    st.subheader("🔧 Custom Analysis")
    
    st.write("**Select columns for analysis:**")
    
    # Select columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if numeric_cols:
            selected_numeric = st.selectbox("Numeric Column:", numeric_cols)
        else:
            selected_numeric = None
            st.write("No numeric columns available")
    
    with col2:
        if categorical_cols:
            selected_categorical = st.selectbox("Categorical Column:", categorical_cols)
        else:
            selected_categorical = None
            st.write("No categorical columns available")
    
    # Custom chart
    if selected_numeric and selected_categorical:
        st.subheader(f"📊 {selected_numeric} vs {selected_categorical}")
        
        # Group data
        grouped_data = df.groupby(selected_categorical)[selected_numeric].mean().reset_index()
        
        fig = px.bar(grouped_data, x=selected_categorical, y=selected_numeric,
                    title=f"Average {selected_numeric} by {selected_categorical}")
        st.plotly_chart(fig, use_container_width=True)
    
    # Show filtered data
    st.subheader("🔍 Custom Filters")
    
    # Filter by column
    if categorical_cols:
        filter_col = st.selectbox("Filter by:", categorical_cols)
        if filter_col:
            unique_values = df[filter_col].unique()
            selected_values = st.multiselect(f"Select values from {filter_col}:", unique_values)
            
            if selected_values:
                filtered_df = df[df[filter_col].isin(selected_values)]
                st.write(f"**Filtered data:** {len(filtered_df)} records")
                st.dataframe(filtered_df.head()) 
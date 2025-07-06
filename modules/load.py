import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path

def load_data():
    """
    Loads Spotify data from JSON files
    """
    st.subheader("1. Data Loading")
    
    # File selection options
    st.write("**Choose how to load your Spotify data:**")
    
    # Option 1: Use default path
    use_default = st.checkbox("Use default path (Spotify Extended Streaming History folder inside code directory)", value=True)
    
    if use_default:
        data_path = Path("Spotify Extended Streaming History")
        
        if not data_path.exists():
            st.error("❌ Default data directory not found!")
            st.write("Make sure the data files are in the 'Spotify Extended Streaming History' folder")
            st.write("Or uncheck this option to select files manually.")
            return None
        
        # List of available files
        json_files = list(data_path.glob("*.json"))
        
        if not json_files:
            st.error("❌ No JSON files found in default directory!")
            return None
        
        st.success(f"✅ Found {len(json_files)} data files in default directory")
        
        # Show available files
        st.write("**Available files:**")
        for file in json_files:
            st.write(f"- {file.name}")
        
        # Load data from default path
        if st.button("🔄 Load All Data"):
            with st.spinner("Loading data..."):
                all_data = []
                
                for file in json_files:
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                all_data.extend(data)
                            else:
                                all_data.append(data)
                        
                        st.success(f"✅ {file.name} loaded successfully")
                        
                    except Exception as e:
                        st.error(f"❌ Error loading {file.name}: {str(e)}")
                
                if all_data:
                    # Convert to DataFrame
                    df = pd.DataFrame(all_data)
                    
                    # Save to session state
                    st.session_state['spotify_data'] = df
                    
                    st.success(f"🎉 Data loaded successfully! Total records: {len(df)}")
                    
                    # Show basic information
                    st.subheader("📊 Data Information")
                    st.write(f"**Columns:** {list(df.columns)}")
                    st.write(f"**Records:** {len(df)}")
                    
                    # Show first rows
                    st.subheader("👀 First Rows")
                    st.dataframe(df.head())
                    
                    return df
                else:
                    st.error("❌ No data was loaded!")
                    return None
    
    # Option 2: Manual file selection
    else:
        st.write("**Select your Spotify data files manually:**")
        
        # File uploader for multiple JSON files
        uploaded_files = st.file_uploader(
            "Choose JSON files",
            type=['json'],
            accept_multiple_files=True,
            help="Select all your Spotify streaming history JSON files"
        )
        
        if not uploaded_files:
            st.info("📁 Please select your Spotify data JSON files")
            return None
        
        st.success(f"✅ Selected {len(uploaded_files)} files")
        
        # Show selected files
        st.write("**Selected files:**")
        for file in uploaded_files:
            st.write(f"- {file.name}")
        
        # Process uploaded files
        if st.button("🔄 Load Selected Files"):
            with st.spinner("Loading data..."):
                all_data = []
                
                for uploaded_file in uploaded_files:
                    try:
                        # Read the uploaded file
                        data = json.load(uploaded_file)
                        if isinstance(data, list):
                            all_data.extend(data)
                        else:
                            all_data.append(data)
                        
                        st.success(f"✅ {uploaded_file.name} loaded successfully")
                        
                    except Exception as e:
                        st.error(f"❌ Error loading {uploaded_file.name}: {str(e)}")
                
                if all_data:
                    # Convert to DataFrame
                    df = pd.DataFrame(all_data)
                    
                    # Save to session state
                    st.session_state['spotify_data'] = df
                    
                    st.success(f"🎉 Data loaded successfully! Total records: {len(df)}")
                    
                    # Show basic information
                    st.subheader("📊 Data Information")
                    st.write(f"**Columns:** {list(df.columns)}")
                    st.write(f"**Records:** {len(df)}")
                    
                    # Show first rows
                    st.subheader("👀 First Rows")
                    st.dataframe(df.head())
                    
                    return df
                else:
                    st.error("❌ No data was loaded!")
                    return None
    
    # Check if data is already loaded
    if 'spotify_data' in st.session_state:
        st.success("✅ Data already loaded in session!")
        df = st.session_state['spotify_data']
        st.write(f"**Loaded records:** {len(df)}")
        
        if st.button("🗑️ Clear Data"):
            del st.session_state['spotify_data']
            st.success("✅ Data removed from session!")
            st.rerun()
    
    return None 
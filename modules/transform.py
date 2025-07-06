import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

def transform_data():
    """
    Transforms and enriches data with ListenBrainz API information
    """
    st.subheader("2. Data Transformation and Enrichment")
    
    # Check if data is loaded
    if 'spotify_data' not in st.session_state:
        st.warning("⚠️ No data loaded! Load data first in the 'Load Data' section.")
        return None
    
    df = st.session_state['spotify_data']
    st.success(f"✅ Data available for transformation: {len(df)} records")
    
    # ListenBrainz API configuration
    st.subheader("🔑 ListenBrainz API Configuration")
    
    # User token field
    user_token = st.text_input("User Token", type="password", help="Your ListenBrainz User Token")
    
    # Or use environment variables
    if st.checkbox("Use environment variables (.env)", value=True):
        env_user_token = os.getenv('LISTENBRAINZ_USER_TOKEN')
        
        if env_user_token:
            user_token = env_user_token
            st.success("✅ User token loaded from .env file")
        else:
            st.error("❌ Environment variable not found!")
            st.write("Create a .env file with LISTENBRAINZ_USER_TOKEN")
    
    # Check if we have credentials
    if not user_token:
        st.warning("⚠️ Configure ListenBrainz API credentials to continue")
        st.info("💡 To get a user token, visit: https://listenbrainz.org/profile/")
        return None
    
    # Test ListenBrainz API connection
    try:
        st.write("🔍 Testing ListenBrainz API connection...")
        
        # Debug: Show API configuration
        st.write("**🔧 API Configuration:**")
        st.write(f"- **Base URL:** `https://api.listenbrainz.org/1/`")
        st.write(f"- **Token provided:** {'Yes' if user_token else 'No'}")
        st.write(f"- **Token length:** {len(user_token) if user_token else 0} characters")
        st.write(f"- **Token preview:** `{user_token[:10]}...`" if user_token and len(user_token) > 10 else f"- **Token:** `{user_token}`")
        
        headers = {
            'Authorization': f'Token {user_token}',
            'Content-Type': 'application/json'
        }
        
        st.write("**📤 Request Headers:**")
        st.json(headers)
        
        # Test with a simple API call to get user info
        test_response = requests.get(
            'https://api.listenbrainz.org/1/validate-token',
            headers=headers
        )
        
        if test_response.status_code == 200:
            st.success("✅ ListenBrainz API connection established and working!")
            st.write(f"**Response details:**")
            st.json(test_response.json())
        else:
            st.error(f"❌ API connection failed with status code: {test_response.status_code}")
            st.write(f"**Full response:**")
            st.code(test_response.text)
            st.write(f"**Response headers:**")
            st.json(dict(test_response.headers))
            st.write(f"**Request URL:** `{test_response.url}`")
            st.write(f"**Request headers:**")
            st.json(dict(test_response.request.headers))
            return None
            
    except Exception as e:
        st.error(f"❌ Error connecting to ListenBrainz API: {str(e)}")
        return None
    
    # Transformation options
    st.subheader("⚙️ Transformation Options")
    
    transform_options = st.multiselect(
        "Select desired transformations:",
        [
            "Enrich with track information (basic)",
            "Enrich with track information (with audio features)",
            "Enrich with artist information",
            "Enrich with album information",
            "Calculate audio features",
            "Process timestamps",
            "Clean duplicate data"
        ],
        default=["Process timestamps", "Enrich with track information (basic)"]
    )
    
    if st.button("🚀 Execute Transformations"):
        if not transform_options:
            st.warning("⚠️ Select at least one transformation option!")
            return None
        
        with st.spinner("Transforming data..."):
            transformed_df = df.copy()
            
            # Process timestamps
            if "Process timestamps" in transform_options:
                st.write("🕐 Processing timestamps...")
                if 'ts' in transformed_df.columns:
                    transformed_df['ts'] = pd.to_datetime(transformed_df['ts'])
                    transformed_df['date'] = transformed_df['ts'].dt.date
                    transformed_df['hour'] = transformed_df['ts'].dt.hour
                    transformed_df['day_of_week'] = transformed_df['ts'].dt.day_name()
                    st.success("✅ Timestamps processed!")
            
            # Clean duplicate data
            if "Clean duplicate data" in transform_options:
                st.write("🧹 Removing duplicates...")
                initial_count = len(transformed_df)
                transformed_df = transformed_df.drop_duplicates()
                final_count = len(transformed_df)
                st.success(f"✅ Duplicates removed! {initial_count - final_count} records removed")
            
            # Enrich with track information (basic)
            if "Enrich with track information (basic)" in transform_options:
                st.write("🎵 Enriching with track information...")
                
                # Get unique tracks to avoid API rate limits
                unique_tracks = transformed_df[['master_metadata_track_name', 'master_metadata_album_artist_name']].drop_duplicates()
                
                # TEMPORARY: Limit to first 15 tracks for testing
                if len(unique_tracks) > 15:
                    st.warning("⚠️ TEMPORARY LIMIT: Processing only first 15 tracks for testing")
                    unique_tracks = unique_tracks.head(15)
                
                st.write(f"Found {len(unique_tracks)} unique tracks to enrich")
                
                # Show sample of tracks to be processed
                st.write("**Sample tracks to process:**")
                sample_tracks = unique_tracks.head(5)
                for _, track in sample_tracks.iterrows():
                    st.write(f"- {track['master_metadata_track_name']} by {track['master_metadata_album_artist_name']}")
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Dictionary to store track features
                track_features = {}
                
                headers = {
                    'Authorization': f'Token {user_token}',
                    'Content-Type': 'application/json'
                }
                
                for idx, (_, track) in enumerate(unique_tracks.iterrows()):
                    track_name = track['master_metadata_track_name']
                    artist_name = track['master_metadata_album_artist_name']
                    
                    status_text.text(f"Processing: {track_name} - {artist_name}")
                    
                    try:
                        # Search for track in ListenBrainz
                        search_url = 'https://api.listenbrainz.org/1/metadata/recording'
                        search_params = {
                            'recording_name': track_name,
                            'artist_name': artist_name
                        }
                        
                        search_response = requests.get(search_url, params=search_params, headers=headers)
                        
                        if search_response.status_code == 200:
                            search_data = search_response.json()
                            st.write(f"🔍 **Search response for {track_name}:**")
                            st.json(search_data)
                            
                            if search_data.get('recordings'):
                                recording = search_data['recordings'][0]
                                
                                # Get additional metadata if available
                                recording_mbid = recording.get('id')
                                
                                if recording_mbid:
                                    # Get detailed recording info
                                    detail_url = f'https://api.listenbrainz.org/1/metadata/recording/{recording_mbid}'
                                    detail_response = requests.get(detail_url, headers=headers)
                                    
                                    if detail_response.status_code == 200:
                                        detail_data = detail_response.json()
                                        recording_detail = detail_data.get('recordings', [{}])[0]
                                        
                                        # Store available features
                                        track_features[f"{track_name}|{artist_name}"] = {
                                            'recording_mbid': recording_mbid,
                                            'title': recording_detail.get('title', track_name),
                                            'artist': recording_detail.get('artist-credit-phrase', artist_name),
                                            'length': recording_detail.get('length'),
                                            'disambiguation': recording_detail.get('disambiguation'),
                                            'releases': len(recording_detail.get('releases', [])),
                                            'tags': len(recording_detail.get('tags', [])),
                                            'rating': recording_detail.get('rating', {}).get('average', 0)
                                        }
                                        
                                        st.write(f"✅ Found: {track_name} - {artist_name} (MBID: {recording_mbid})")
                                    else:
                                        st.warning(f"⚠️ Could not get detailed info for: {track_name} - {artist_name}")
                                else:
                                    # Store basic info without MBID
                                    track_features[f"{track_name}|{artist_name}"] = {
                                        'recording_mbid': None,
                                        'title': recording.get('title', track_name),
                                        'artist': recording.get('artist-credit-phrase', artist_name),
                                        'length': recording.get('length'),
                                        'disambiguation': recording.get('disambiguation'),
                                        'releases': len(recording.get('releases', [])),
                                        'tags': len(recording.get('tags', [])),
                                        'rating': recording.get('rating', {}).get('average', 0)
                                    }
                                    
                                    st.write(f"✅ Found basic info for: {track_name} - {artist_name}")
                            else:
                                st.warning(f"❌ Not found: {track_name} - {artist_name}")
                        else:
                            st.error(f"❌ API error for: {track_name} - {artist_name} (Status: {search_response.status_code})")
                            st.write(f"**Error response:**")
                            st.code(search_response.text)
                            st.write(f"**Request URL:** `{search_response.url}`")
                            st.write(f"**Request params:**")
                            st.json(search_params)
                        
                        # Rate limiting - ListenBrainz allows 1 request per second
                        time.sleep(1)
                        
                    except Exception as e:
                        st.warning(f"❌ Error processing: {track_name} - {artist_name} | Error: {str(e)}")
                    
                    # Update progress
                    progress_bar.progress((idx + 1) / len(unique_tracks))
                
                # Add features to dataframe
                st.write("📊 Adding features to dataset...")
                
                # Create new columns
                feature_columns = [
                    'recording_mbid', 'title', 'artist', 'length', 'disambiguation',
                    'releases', 'tags', 'rating'
                ]
                
                for col in feature_columns:
                    transformed_df[col] = None
                
                # Fill in features for each track
                for idx, row in transformed_df.iterrows():
                    track_name = row['master_metadata_track_name']
                    artist_name = row['master_metadata_album_artist_name']
                    key = f"{track_name}|{artist_name}"
                    
                    if key in track_features:
                        features = track_features[key]
                        for col in feature_columns:
                            transformed_df.at[idx, col] = features[col]
                
                # Show enrichment summary
                enriched_count = sum(1 for key in track_features.keys())
                st.success(f"✅ Track enrichment completed! {enriched_count}/{len(unique_tracks)} tracks enriched")
                
                # Show sample of enriched data
                st.subheader("🎵 Sample Enriched Tracks")
                sample_columns = ['master_metadata_track_name', 'master_metadata_album_artist_name', 'recording_mbid', 'rating']
                st.dataframe(transformed_df[sample_columns].head())
            
            # Enrich with track information (with audio features)
            if "Enrich with track information (with audio features)" in transform_options:
                st.write("🎵 Enriching with track information and audio features...")
                st.warning("⚠️ Audio features are not directly available through ListenBrainz API")
                st.info("💡 ListenBrainz focuses on listening history and metadata, not audio analysis")
                
                # Note: ListenBrainz doesn't provide audio features like Spotify
                # This would need to be implemented with a different service if needed
            
            # Enrich with artist information
            if "Enrich with artist information" in transform_options:
                st.write("👨‍🎤 Enriching with artist information...")
                
                # Get unique artists
                unique_artists = transformed_df['master_metadata_album_artist_name'].drop_duplicates()
                
                if len(unique_artists) > 10:
                    st.warning("⚠️ TEMPORARY LIMIT: Processing only first 10 artists for testing")
                    unique_artists = unique_artists.head(10)
                
                st.write(f"Found {len(unique_artists)} unique artists to enrich")
                
                # Dictionary to store artist features
                artist_features = {}
                
                headers = {
                    'Authorization': f'Token {user_token}',
                    'Content-Type': 'application/json'
                }
                
                for artist_name in unique_artists:
                    try:
                        # Search for artist in ListenBrainz
                        search_url = 'https://api.listenbrainz.org/1/metadata/artist'
                        search_params = {'artist_name': artist_name}
                        
                        search_response = requests.get(search_url, params=search_params, headers=headers)
                        
                        if search_response.status_code == 200:
                            search_data = search_response.json()
                            st.write(f"🔍 **Artist search response for {artist_name}:**")
                            st.json(search_data)
                            
                            if search_data.get('artists'):
                                artist = search_data['artists'][0]
                                artist_mbid = artist.get('id')
                                
                                if artist_mbid:
                                    # Get detailed artist info
                                    detail_url = f'https://api.listenbrainz.org/1/metadata/artist/{artist_mbid}'
                                    detail_response = requests.get(detail_url, headers=headers)
                                    
                                    if detail_response.status_code == 200:
                                        detail_data = detail_response.json()
                                        artist_detail = detail_data.get('artists', [{}])[0]
                                        
                                        artist_features[artist_name] = {
                                            'artist_mbid': artist_mbid,
                                            'name': artist_detail.get('name', artist_name),
                                            'disambiguation': artist_detail.get('disambiguation'),
                                            'country': artist_detail.get('country'),
                                            'type': artist_detail.get('type'),
                                            'gender': artist_detail.get('gender'),
                                            'tags': len(artist_detail.get('tags', [])),
                                            'rating': artist_detail.get('rating', {}).get('average', 0)
                                        }
                                        
                                        st.write(f"✅ Found artist: {artist_name} (MBID: {artist_mbid})")
                                    else:
                                        st.warning(f"⚠️ Could not get detailed info for artist: {artist_name}")
                                else:
                                    artist_features[artist_name] = {
                                        'artist_mbid': None,
                                        'name': artist.get('name', artist_name),
                                        'disambiguation': artist.get('disambiguation'),
                                        'country': artist.get('country'),
                                        'type': artist.get('type'),
                                        'gender': artist.get('gender'),
                                        'tags': len(artist.get('tags', [])),
                                        'rating': artist.get('rating', {}).get('average', 0)
                                    }
                            else:
                                st.warning(f"❌ Artist not found: {artist_name}")
                        else:
                            st.error(f"❌ API error for artist: {artist_name} (Status: {search_response.status_code})")
                            st.write(f"**Error response:**")
                            st.code(search_response.text)
                            st.write(f"**Request URL:** `{search_response.url}`")
                            st.write(f"**Request params:**")
                            st.json(search_params)
                        
                        # Rate limiting
                        time.sleep(1)
                        
                    except Exception as e:
                        st.warning(f"❌ Error processing artist: {artist_name} | Error: {str(e)}")
                
                # Add artist features to dataframe
                artist_columns = [
                    'artist_mbid', 'artist_name', 'artist_disambiguation', 'artist_country',
                    'artist_type', 'artist_gender', 'artist_tags', 'artist_rating'
                ]
                
                for col in artist_columns:
                    transformed_df[col] = None
                
                for idx, row in transformed_df.iterrows():
                    artist_name = row['master_metadata_album_artist_name']
                    if artist_name in artist_features:
                        features = artist_features[artist_name]
                        transformed_df.at[idx, 'artist_mbid'] = features['artist_mbid']
                        transformed_df.at[idx, 'artist_name'] = features['name']
                        transformed_df.at[idx, 'artist_disambiguation'] = features['disambiguation']
                        transformed_df.at[idx, 'artist_country'] = features['country']
                        transformed_df.at[idx, 'artist_type'] = features['type']
                        transformed_df.at[idx, 'artist_gender'] = features['gender']
                        transformed_df.at[idx, 'artist_tags'] = features['tags']
                        transformed_df.at[idx, 'artist_rating'] = features['rating']
                
                st.success(f"✅ Artist enrichment completed! {len(artist_features)} artists enriched")
            
            # Enrich with album information
            if "Enrich with album information" in transform_options:
                st.write("💿 Enriching with album information...")
                st.info("ℹ️ Album enrichment functionality will be implemented")
                # This would require album MBID lookup and detailed album information
            
            # Calculate audio features
            if "Calculate audio features" in transform_options:
                st.write("🎼 Calculating derived features...")
                
                # Since ListenBrainz doesn't provide audio features, we'll calculate derived features
                # from the metadata we have
                
                st.write("📊 Calculating derived features from metadata...")
                
                # Length categories (if we have length data)
                if 'length' in transformed_df.columns:
                    transformed_df['length_minutes'] = transformed_df['length'] / 60 if transformed_df['length'].notna().any() else None
                    
                    # Length categories
                    transformed_df['length_category'] = pd.cut(
                        transformed_df['length_minutes'],
                        bins=[0, 2, 4, 6, 10, 100],
                        labels=['Very Short', 'Short', 'Medium', 'Long', 'Very Long']
                    )
                
                # Rating categories
                if 'rating' in transformed_df.columns:
                    transformed_df['rating_category'] = pd.cut(
                        transformed_df['rating'],
                        bins=[0, 2, 4, 6, 8, 10],
                        labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
                    )
                
                # Artist popularity based on tags count
                if 'artist_tags' in transformed_df.columns:
                    transformed_df['artist_popularity'] = pd.cut(
                        transformed_df['artist_tags'],
                        bins=[0, 5, 15, 30, 100],
                        labels=['Unknown', 'Emerging', 'Popular', 'Very Popular']
                    )
                
                # Release count categories
                if 'releases' in transformed_df.columns:
                    transformed_df['release_category'] = pd.cut(
                        transformed_df['releases'],
                        bins=[0, 1, 5, 15, 100],
                        labels=['Single Release', 'Few Releases', 'Many Releases', 'Extensive Catalog']
                    )
                
                # Create a composite popularity score
                if all(col in transformed_df.columns for col in ['rating', 'artist_tags', 'releases']):
                    transformed_df['popularity_score'] = (
                        (transformed_df['rating'] / 10) * 0.4 +
                        (transformed_df['artist_tags'] / 50) * 0.3 +
                        (transformed_df['releases'] / 20) * 0.3
                    )
                    
                    transformed_df['popularity_level'] = pd.cut(
                        transformed_df['popularity_score'],
                        bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
                    )
                
                st.success("✅ Derived features calculated!")
                
                # Show feature summary
                st.subheader("📈 Derived Features Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'length_category' in transformed_df.columns:
                        st.write("**Length Distribution:**")
                        length_counts = transformed_df['length_category'].value_counts()
                        st.write(length_counts)
                    
                    if 'rating_category' in transformed_df.columns:
                        st.write("**Rating Distribution:**")
                        rating_counts = transformed_df['rating_category'].value_counts()
                        st.write(rating_counts)
                
                with col2:
                    if 'artist_popularity' in transformed_df.columns:
                        st.write("**Artist Popularity:**")
                        artist_pop_counts = transformed_df['artist_popularity'].value_counts()
                        st.write(artist_pop_counts)
                    
                    if 'popularity_level' in transformed_df.columns:
                        st.write("**Overall Popularity:**")
                        pop_level_counts = transformed_df['popularity_level'].value_counts()
                        st.write(pop_level_counts)
                
                # Show sample with new features
                st.subheader("🎵 Sample with Derived Features")
                sample_columns = ['master_metadata_track_name', 'master_metadata_album_artist_name']
                if 'length_category' in transformed_df.columns:
                    sample_columns.append('length_category')
                if 'rating_category' in transformed_df.columns:
                    sample_columns.append('rating_category')
                if 'popularity_level' in transformed_df.columns:
                    sample_columns.append('popularity_level')
                
                st.dataframe(transformed_df[sample_columns].head())
            
            # Save transformed data
            st.session_state['transformed_data'] = transformed_df
            
            st.success("🎉 Transformation completed!")
            
            # Show summary
            st.subheader("📊 Transformation Summary")
            st.write(f"**Original records:** {len(df)}")
            st.write(f"**Transformed records:** {len(transformed_df)}")
            st.write(f"**Original columns:** {list(df.columns)}")
            st.write(f"**Transformed columns:** {list(transformed_df.columns)}")
            
            # Show first rows of transformed data
            st.subheader("👀 Transformed Data (First Rows)")
            st.dataframe(transformed_df.head())
            
            return transformed_df
    
    # Check if transformed data exists
    if 'transformed_data' in st.session_state:
        st.success("✅ Transformed data available!")
        transformed_df = st.session_state['transformed_data']
        st.write(f"**Transformed records:** {len(transformed_df)}")
        
        if st.button("🗑️ Clear Transformed Data"):
            del st.session_state['transformed_data']
            st.success("✅ Transformed data removed!")
            st.rerun()
    
    return None 
import streamlit as st
from modules.load import load_data
from modules.transform import transform_data
from modules.visualize import visualize_data

def main():
    st.set_page_config(
        page_title="Spotify Analysis",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 Spotify Analysis")
    
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Simple button navigation
    if st.sidebar.button("🏠 Home"):
        st.session_state['current_page'] = "Home"
    if st.sidebar.button("📂 1. Load Data"):
        st.session_state['current_page'] = "1. Load Data"
    if st.sidebar.button("🔄 2. Transform Data"):
        st.session_state['current_page'] = "2. Transform Data"
    if st.sidebar.button("📊 3. Visualize Data"):
        st.session_state['current_page'] = "3. Visualize Data"
    
    # Set default page if not set
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Home"
    
    page = st.session_state['current_page']

    if page == "Home":
        st.markdown("""
        ## 🎵 Welcome to Your Spotify Analysis Dashboard!
        
        Discover fascinating insights about your music listening habits with this comprehensive analysis tool.
        
        ### What you can do:
        - 📂 **1. Load Data**: Import your Spotify streaming history
        - 🔄 **2.Transform Data**: Clean and prepare your data for analysis  
        - 📊 **3. Visualize Data**: Explore interactive charts and insights
        
        ### Getting Started:
        1. First, load your Spotify data using the sidebar menu
        2. Transform the data to prepare it for analysis
        3. Explore visualizations to discover patterns in your listening habits
        
        ---
        """)

    elif page == "1. Load Data":
        st.header("📂 Load Data")
        load_data()
        
    elif page == "2. Transform Data":
        st.header("🔄 Transform Data")
        transform_data()
        
    elif page == "3. Visualize Data":
        st.header("📊 Visualize Data")
        visualize_data()

if __name__ == "__main__":
    main() 
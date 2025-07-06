# 🎵 Spotify Analysis Sleep Apnea Project

> **Advanced music listening pattern analysis** - A comprehensive data science project analyzing Spotify streaming history
>
> Project done in 2021 for my Data Science and Big Data postgraduate

[![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-research%20project-orange?style=for-the-badge)]()

## 📚 Related Documentation

For detailed technical implementation, methodology, and results, see the comprehensive case study:

**[⭐ Link to Technical Case Study](TechnicalCaseStudy.md)**

This document contains:
- ✅ **Complete methodology** and data engineering approach
- ✅ **Machine learning pipeline** with 82% accuracy results
- ✅ **User validation results** (78-95% approval rates)
- ✅ **Example playlists** and recommendation outcomes
- ✅ **Full tech stack** and architecture details
- ✅ **Data coverage** (35k+ plays, 700k+ tracks analyzed)

**The technical case study provides the complete research foundation and implementation details for this project.**



> [!IMPORTANT]  
> **This project is no longer fully replicable due to Spotify's API changes.** Spotify has restricted access to the Audio Features endpoint, which was crucial for detailed musical analysis. The project now focuses on:
> 
> - ✅ **Available**: Basic streaming history analysis
> - ✅ **Available**: Temporal pattern analysis  
> - ✅ **Available**: Genre and artist analysis
> - ❌ **Unavailable**: Audio features (danceability, energy, valence, etc.)

## 📋 Project Overview

This project analyzes Spotify streaming history data to understand music listening patterns, with particular focus on sleep-related behaviors. It combines data science techniques with music psychology to provide insights into how music consumption relates to sleep quality and patterns.

### Key Research Areas

- **Temporal Analysis**: When people listen to music throughout the day
- **Sleep Pattern Correlation**: Music listening during sleep hours
- **Genre Preferences**: How music choices vary by time of day
- **Behavioral Patterns**: Skip rates, session duration, repeat listening
- **Seasonal Trends**: How listening habits change over time

## 🏗️ Project Architecture

```bash
spotify-streaming-history-analysis/
│
├── 🎯 Application Layer
│   ├── 📊 app.py                     # Streamlit web interface
│   ├── ⚙️  setup.py                  # Package configuration
│   └── 📋 requirements.txt           # Dependencies
│
├── 💻 Source Code
│   └── 📦 src/spotify_analysis/
│       ├── 🔧 core/                  # Core processing engine
│       │   ├── data_loader.py        #   → Raw data ingestion
│       │   ├── data_transformer.py   #   → ETL pipeline
│       │   └── pattern_analyzer.py   #   → ML & analytics
│       ├── 🎨 visualization/         # Interactive dashboards
│       └── 🛠️  utils/                # Helper functions
│
├── 📚 Research & Analysis
│   ├── 📔 notebooks/                 # Jupyter notebooks
│   │   ├── 🧬 GenreNormalization     # Classification models
│   │   ├── 🤖 MusicSuggestion*       # Recommendation systems  
│   │   ├── ❤️  LikeScore             # Preference algorithms
│   │   └── 📥 downloader_v2          # Data acquisition
│   └── 📁 modules/                   # Legacy components
│
├── 🗄️ Data Infrastructure  
│   ├── 💾 database/                  # Schema & migrations
│   │   ├── create_tables.sql         #   → Main schema
│   │   └── schema/                   #   → Advanced configs
│   ├── ⚙️  config/                   # Environment settings
│   └── 📜 scripts/                   # Automation tools
│
└── 🔬 Development & Testing
    ├── 🧪 tests/                     # Test suite
    ├── 📖 README.md                  # Documentation
    ├── 📋 TechnicalCaseStudy.md      # Research methodology
    └── 📄 LICENSE                    # MIT License
```

## 🚀 Features

### Core Analysis Capabilities
- **📈 Complete Temporal Analysis**: Evolution of musical taste over time
- **🎨 Interactive Visualizations**: Dynamic charts with Streamlit
- **🎵 Musical Insights**: Analysis of genres, artists, and listening patterns
- **📱 Behavioral Patterns**: How you listen to music at different times
- **🔍 Automatic Discoveries**: Surprising insights about your data
- **📊 Exportable Reports**: PDFs and charts to share

### Advanced Analytics
- **Genre Normalization**: Standardized genre classification
- **Music Recommendation**: AI-powered music suggestions
- **Preference Scoring**: Like/dislike pattern analysis
- **Sleep Pattern Analysis**: Night-time listening behavior
- **Database Integration**: PostgreSQL schema for complex queries

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **Streamlit** - Interactive web interface
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive data visualization
- **NumPy** - Numerical computing

### Data Processing
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Relational database
- **JSON** - Data interchange format

### Development Tools
- **Jupyter Notebooks** - Exploratory data analysis
- **Git** - Version control
- **Environment Variables** - Secure configuration management

## 📦 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (optional, for advanced features)
- Spotify Extended Streaming History data

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/spotify-analysis-sleep-apnea.git
cd spotify-analysis-sleep-apnea

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Data Configuration

1. **Request Spotify Data**:
   - Go to [Spotify Privacy Settings](https://www.spotify.com/account/privacy/)
   - Request "Extended streaming history"
   - Wait for email notification (1-3 days)

2. **Prepare Data**:
   ```bash
   # Extract downloaded ZIP file
   # Place JSON files in: Spotify Extended Streaming History/
   ```

3. **Environment Setup** (Optional):
   ```bash
   # Copy example environment file
   cp env_example.txt .env
   
   # Edit .env with your credentials
   # LISTENBRAINZ_USER_TOKEN=your_token_here
   ```

## 🎯 Usage Guide

### Basic Analysis

1. **Load Data**: Use the sidebar to load your Spotify streaming history
2. **Transform Data**: Clean and enrich your data with additional metadata
3. **Visualize**: Explore interactive charts and insights

### Advanced Features

```bash
# Run specific analysis modules
python -m modules.load
python -m modules.transform
python -m modules.visualize

# Database operations (if configured)
python Create\ Tables/SpotifyTables/Main.py
```

### Jupyter Notebooks

```bash
# Launch Jupyter for advanced analysis
jupyter notebook Analytics/
```

## 📊 Key Insights & Findings

### Temporal Patterns
- **Peak Listening Hours**: Analysis of when users listen most actively
- **Sleep-Time Listening**: Patterns during typical sleep hours
- **Weekday vs Weekend**: Behavioral differences across the week

### Musical Preferences
- **Genre Evolution**: How taste changes over time
- **Artist Loyalty**: Repeat listening patterns
- **Mood Correlation**: Music choices by time of day
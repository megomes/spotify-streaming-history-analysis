# Spotify Analysis Sleep Apnea - Project Structure

## 📁 Complete Project Organization

```
spotify-analysis-sleep-apnea/
├── 📄 README.md                    # Main project documentation
├── 📄 setup.py                     # Package installation configuration
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 LICENSE                      # MIT License
├── 📄 PROJECT_STRUCTURE.md         # This file - project organization
│
├── 📊 app.py                       # Main Streamlit application
├── 📄 get_token.py                 # Spotify API token management
├── 📄 env_example.txt              # Environment variables template
│
├── 📁 src/                         # Source code package
│   └── spotify_analysis/           # Main package
│       ├── 📄 __init__.py          # Package initialization
│       ├── 📄 cli.py               # Command line interface
│       │
│       ├── 📁 core/                # Core functionality
│       │   ├── 📄 __init__.py      # Core module initialization
│       │   ├── 📄 data_loader.py   # Data loading utilities
│       │   ├── 📄 data_transformer.py # Data transformation
│       │   └── 📄 pattern_analyzer.py # Pattern analysis
│       │
│       ├── 📁 utils/               # Utility functions
│       │   ├── 📄 __init__.py      # Utils module initialization
│       │   ├── 📄 data_validation.py # Data validation utilities
│       │   ├── 📄 export_utils.py  # Export functionality
│       │   └── 📄 config_utils.py  # Configuration management
│       │
│       └── 📁 visualization/       # Visualization components
│           ├── 📄 __init__.py      # Visualization module initialization
│           ├── 📄 chart_creator.py # Chart creation utilities
│           ├── 📄 dashboard_builder.py # Dashboard components
│           └── 📄 plot_utils.py    # Plotting utilities
│
├── 📁 modules/                     # Legacy modules (for backward compatibility)
│   ├── 📄 __init__.py
│   ├── 📄 load.py                  # Legacy data loading
│   ├── 📄 transform.py             # Legacy data transformation
│   └── 📄 visualize.py             # Legacy visualization
│
├── 📁 Analytics/                   # Jupyter notebooks for analysis
│   ├── 📄 GenreNormalization.ipynb # Genre classification analysis
│   ├── 📄 MusicSuggestion.ipynb   # Music recommendation system
│   ├── 📄 MusicSuggestionV2.ipynb # Enhanced recommendation system
│   ├── 📄 MusicSuggestionV3.ipynb # Advanced recommendation system
│   ├── 📄 MusicSuggestionV4.ipynb # Latest recommendation system
│   ├── 📄 LikeScore.ipynb         # Preference scoring analysis
│   └── 📄 Test Sheet Creator.ipynb # Test data generation
│
├── 📁 Create Tables/               # Database schema and setup
│   ├── 📁 Analytics/               # Analytics database setup
│   ├── 📁 SpotifyTables/           # Main database schema
│   │   ├── 📄 create_tables.sql    # SQL schema definition
│   │   ├── 📄 Main.py             # Database setup script
│   │   ├── 📄 inputs_spotify.erv  # Environment configuration
│   │   └── 📁 Script/             # Database scripts
│   │       ├── 📄 Album.py         # Album management
│   │       ├── 📄 Artist.py        # Artist management
│   │       ├── 📄 Music.py         # Music management
│   │       ├── 📄 Genre.py         # Genre management
│   │       ├── 📄 Play.py          # Play tracking
│   │       ├── 📄 SQLConn.py       # Database connection
│   │       └── 📄 SQLData.py       # Data operations
│   │
│   ├── 📁 SpotifyTables V2/        # Updated database schema
│   │   ├── 📄 create_tables.sql    # Updated SQL schema
│   │   ├── 📄 Main.py             # Updated setup script
│   │   └── 📁 Script/             # Updated database scripts
│   │
│   └── 📁 StartSchema Creator/     # Star schema creator
│       ├── 📄 StarSchema Creator.ipynb # Schema creation notebook
│       ├── 📄 inputs_example.erv   # Example configuration
│       ├── 📁 output/              # Generated output
│       └── 📁 reference_files/     # Reference implementations
│
├── 📁 Spotify Extended Streaming History/  # Raw data storage (gitignored)
│   ├── 📄 Streaming_History_Audio_2015-2018_0.json
│   ├── 📄 Streaming_History_Audio_2018-2020_1.json
│   ├── 📄 Streaming_History_Audio_2020-2023_2.json
│   ├── 📄 Streaming_History_Audio_2023-2025_3.json
│   └── 📄 Streaming_History_Video_2017-2025.json
│
├── 📁 tests/                       # Test suite
│   ├── 📄 __init__.py             # Test package initialization
│   └── 📄 test_data_loader.py     # Data loader tests
│
├── 📁 docs/                        # Documentation
│   ├── 📄 api.md                  # API documentation
│   ├── 📄 user_guide.md           # User guide
│   └── 📄 development.md          # Development guide
│
└── 📁 data/                        # Processed data storage
    ├── 📄 raw/                     # Raw data files
    ├── 📄 processed/               # Processed data files
    └── 📄 results/                 # Analysis results
```

## 🔧 Key Components

### Core Application
- **`app.py`**: Main Streamlit web application
- **`src/spotify_analysis/`**: Modular Python package
- **`setup.py`**: Package installation configuration

### Data Processing Pipeline
1. **Data Loading** (`core/data_loader.py`): Load Spotify JSON files
2. **Data Transformation** (`core/data_transformer.py`): Clean and enrich data
3. **Pattern Analysis** (`core/pattern_analyzer.py`): Analyze listening patterns
4. **Visualization** (`visualization/`): Create charts and dashboards

### Analysis Notebooks
- **Genre Analysis**: Classification and normalization
- **Music Recommendation**: AI-powered suggestions
- **Preference Scoring**: Like/dislike pattern analysis

### Database Integration
- **PostgreSQL Schema**: Relational database design
- **SQL Scripts**: Database operations and management
- **Star Schema**: Optimized for analytics

## 🚀 Usage Patterns

### Web Application
```bash
streamlit run app.py
```

### Command Line Interface
```bash
# Load data
spotify-analysis load --path "Spotify Extended Streaming History"

# Transform data
spotify-analysis transform --input data.csv --output transformed.csv

# Analyze patterns
spotify-analysis analyze --input transformed.csv --output results/

# Full pipeline
spotify-analysis full --path "Spotify Extended Streaming History" --output results/
```

### Development
```bash
# Install in development mode
pip install -e .

# Run tests
pytest tests/

# Format code
black src/
isort src/
```

## 📊 Data Flow

1. **Raw Data**: Spotify JSON files → `Spotify Extended Streaming History/`
2. **Loading**: JSON files → Pandas DataFrame
3. **Transformation**: Raw DataFrame → Enriched DataFrame
4. **Analysis**: Enriched DataFrame → Pattern Analysis Results
5. **Visualization**: Results → Interactive Charts
6. **Storage**: Results → Database/CSV/JSON files

## 🔍 Research Focus

### Sleep Apnea Analysis
- **Temporal Patterns**: When people listen during sleep hours
- **Genre Preferences**: Music choices during sleep time
- **Behavioral Patterns**: Skip rates, session duration
- **Quality Indicators**: Completion rates, engagement patterns

### Technical Features
- **Modular Design**: Easy to extend and maintain
- **Type Safety**: Comprehensive type annotations
- **Testing**: Unit tests for core functionality
- **Documentation**: Professional documentation standards
- **CLI Interface**: Command-line tool for automation
- **Web Interface**: Streamlit dashboard for exploration

## ⚠️ Important Notes

### API Limitations
- **Spotify API**: Audio features endpoint no longer available
- **Focus**: Basic streaming history analysis
- **Alternative**: ListenBrainz API for metadata enrichment

### Data Privacy
- **Local Processing**: All data processed locally
- **GDPR Compliance**: User controls their own data
- **No External Sharing**: Data never leaves user's device

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computing

### Development Tools
- **Git**: Version control
- **Pytest**: Testing framework
- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking

### Database
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM for database operations

This structure provides a professional, scalable foundation for music listening pattern analysis with a specific focus on sleep-related behaviors and sleep apnea research. 
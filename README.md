# 🎵 Spotify Streaming History Analysis

> **Transforming data into musical insights** - A deep analysis of your Spotify streaming history with interactive visualizations

[![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-in%20development-orange?style=for-the-badge)]()

## 📋 Data Privacy & GDPR Compliance

### Requesting Your Spotify Data

Due to **GDPR (General Data Protection Regulation)** and **LGPD (Lei Geral de Proteção de Dados)**, you have the right to request a copy of all your personal data from Spotify. Here's how to do it:

#### Step-by-Step Process

1. **Access Spotify Privacy Settings**
   - Go to [Spotify Privacy Settings](https://www.spotify.com/account/privacy/)
   - Sign in to your Spotify account

2. **Request Your Data**
   - Scroll down to "Download your data"
   - Click "Request" under "Extended streaming history"
   - Confirm your request

3. **Wait for Processing**
   - Spotify will process your request (usually 1-3 days)
   - You'll receive an email when your data is ready

4. **Download Your Data**
   - Click the download link in the email
   - Extract the ZIP file to your project directory
   - Place the `Streaming_History_Audio_YYYY-YYYY_X.json` files in the `Spotify Extended Streaming History/` folder

#### What Data You'll Receive

Your extended streaming history includes:
- **Track information**: Name, artist, album, duration
- **Listening behavior**: Timestamps, play duration, skip behavior
- **Technical data**: Platform, country, IP address (anonymized)
- **Privacy settings**: Incognito mode usage

#### Privacy & Security Notes

- ✅ **Your data is processed locally** - No data is sent to external servers
- ✅ **GDPR compliant** - You have full control over your personal data
- ✅ **Secure handling** - Data files are in `.gitignore` to prevent accidental sharing
- ⚠️ **Keep private** - Don't share your raw data files publicly 

> **Note**: This tool respects your privacy and processes all data locally. Your streaming history never leaves your device.


## 📊 Dashboard Preview

> *Screenshots and GIFs of the dashboard will be added here*



## 🚀 Features

- **📈 Complete Temporal Analysis**: Evolution of musical taste over the years
- **🎨 Interactive Visualizations**: Dynamic charts with Streamlit
- **🎵 Musical Insights**: Analysis of genres, artists, and listening patterns
- **📱 Behavioral Patterns**: How you listen to music at different times
- **🔍 Automatic Discoveries**: Surprising insights about your data
- **📊 Exportable Reports**: PDFs and charts to share



## 🛠️ Technologies

- **Python 3.8+** - Main language
- **Streamlit** - Interactive web interface
- **Pandas** - Data processing
- **Plotly** - Interactive charts
- **Spotipy** - Spotify API (data enrichment)



## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Spotify data (Extended Streaming History)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/your-username/spotify-analysis.git
cd spotify-analysis

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Data Configuration

1. Download your Spotify data from [spotify.com/account](https://spotify.com/account)
2. Extract the `my_spotify_data.zip` file
3. Place the `Spotify Extended Streaming History` folder in the project directory
4. Run the processing: `python process_data.py`



## 🎯 How to Use

### Complete Analysis

```bash
# Process all data and generate insights
python main.py --full-analysis

# Run the dashboard
streamlit run app.py
```

### Quick Analysis

```bash
# Basic analysis for demonstration
python main.py --quick-demo
```



## 📊 Key Insights

- [ ] To-do



## 🏗️ Project Structure

- [ ] To-do


## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 📝 License

This project is under the MIT license. See the [LICENSE](LICENSE) file for more details.



## 🙏 Acknowledgments

- [Spotify](https://spotify.com) for providing the data
- [Streamlit](https://streamlit.io) for the visualization platform
- Python community for all the amazing libraries



</div> 
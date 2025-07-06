# 🎧 Spotify Personalized Recommendation System

> Matheus Ervilha Gomes – Specialist in Data Science & Big Data

**A full-stack data project analyzing 35k+ plays over 6+ years, leveraging Spotify’s API, user GDPR exports, advanced data engineering and machine learning to outperform Spotify's own recommendations.**

---

## 📌 Overview

Spotify's official recommender is great. But can *we*, with our own data, build an even more *personal* recommendation engine?

✅ Use entire listening history since 2016
✅ Enrich with complete Spotify catalog via API
✅ Engineer features that Spotify itself doesn't surface
✅ Build custom Machine Learning models to suggest what you'll actually like

> **Result:** 78%–95% accuracy in user testing, with Playlists tailored far beyond "Discover Weekly".

---

## 📈 Highlights

* 📦 **34,917** full streaming events since 2016
* 🎵 Enriched with **697,510** tracks from **77,413** albums by **5,003** artists
* 🗺️ Mapped **1,583** genres into **21** custom categories
* 💽 Designed a **relational Star Schema** in Postgres for analytics
* 📊 Interactive BI dashboards in Power BI
* 🧠 Custom ML model with up to **82% test accuracy**
* 🎯 User validation: 78–95% approval on suggested playlists

---

## 🧭 Goal

> "Given all the artists I've listened to, which other songs by them would I *love*?"

Spotify gives you Discover Weekly. I wanted *something better*: a recommender built from **my full history**, with transparent logic and control.

---

## 🛠️ Architecture

* **Data Sources:**

  * Spotify GDPR personal data export
  * Spotify Web API

* **Data Engineering:**

  * JSON to Postgres with Star Schema
  * Category normalization
  * Audio feature extraction

* **Analytics:**

  * Power BI with direct database connection
  * Automated relationship detection

* **ML Pipeline:**

  * Custom "Like Score" metric engineering
  * One-Hot encoding for genres
  * Artist name embeddings via Word2Vec
  * Decision Tree and Bagging Classifiers

---

## 📥 Data Collection

### 🎯 GDPR Export

* Full playback logs since June 2016
* Includes:

  * Timestamps
  * Track, artist, album names
  * Playback duration, device, IP
  * Spotify URIs

✅ 34,917 plays
✅ Unique, rich, user-authenticated data

---

### 🎯 Spotify API Enrichment

For every track:

* `Get Several Tracks`: metadata
* `Get Audio Features`: danceability, energy, loudness...
* `Get Multiple Artists`: genres, popularity
* `Get Artist’s Albums`: complete discography

✅ 697,510 tracks
✅ 5,003 artists
✅ 77,413 albums

> **All saved to JSON for reproducibility.**

---

## 🧹 Data Processing

✅ **Release Date Precision**

* Normalized day/month/year formats to consistent dates

✅ **Genre Normalization**

* 1,583 genres → 21 categories
* Example mapping:

  ```
  "pop rock" → Rock, Pop
  "nu jazz" → Jazz
  "modern indie rock" → Indie, Rock
  ```

✅ **Star Schema DB**

* Music, Artist, Album, Play, Genre, Favorites tables
* PostgreSQL with custom ingestion scripts

✅ **BI-Ready**

* Power BI autodetects relationships
* Fast querying for 35k+ user plays plus 700k+ track catalog

---

## 📊 Analytics Snapshots

✅ **Features over time**

* Did music choices get slower / quieter?
* Feature distributions by year

✅ **Top Played Artists / Genres**

* Discovered dominant listening patterns

✅ **Audio Feature Analysis**

* Danceability, Energy, Loudness histograms
* Radar charts for category vs. features

✅ **Genre Word Cloud**

* Visual distribution of listening taste

✅ **Immediate insights**

* Power BI dashboards detected **all joins automatically** thanks to schema design.

---

## 🧠 Feature Engineering: Like Score

To train the model, I defined **Like Score** — a weighted metric of genuine preference:

✅ Variables:

* Play count
* Month-level averages (recency-adjusted)
* Favorites
* Skips, replays
* % song completed

✅ Example weight scheme:

```python
pesos = {
  'repeat': 2,
  'month_avg': 2,
  'last': 5,
  'favorites': 5,
  'track_done': 7,
  'skipped': 4,
  'replayed': 10,
  'duration_avr_total': 3
}
```

✅ Normalized to 0–1 scale
✅ Median Like Score: **0.28**
✅ \~47% of tracks rated above average

---

## 🤖 Machine Learning

### Data

* \~7,841 unique user-played tracks with features
* One-hot genre categories
* Artist name embeddings (Word2Vec)

✅ Training/Test split: 70/30

---

### Models Tested

1️⃣ **DecisionTreeClassifier (default):**

* \~71% test accuracy

2️⃣ **DecisionTreeClassifier (custom hyperparams):**

* \~82% test accuracy

3️⃣ **BaggingClassifier:**

* Best result: **82% accuracy**

✅ Applied model to entire 700k+ track universe

---

### 📈 Model Improvements

* **Embedding Artist Names**

  * Word2Vec on artist names
  * Captured semantic relationships (e.g. "Sia" → "Diplo", "Illenium")
  * Improved classification of lesser-known artists

✅ Final playlist generation used both categorical and semantic features.

---

## 🎯 Results

✅ **User validation**:

* Top 15 recommendations: **78–95% approval**
* Category playlists: **High accuracy across genres**
* Negative playlists: **60%+ dislike rate (as designed!)**
* Spotify's own Discover Weekly compared at \~53% approval

✅ **Top Playlists Created:**

* Top 15 (overall best)
* Top 15 (with artist embeddings)
* Top 30 (compared with Discover Weekly)
* Top 15 Negative (what you won’t like)
* Genre-specific (Rock, Pop, Indie, EDM, Folk)

✅ **Machine Learning accuracy on test set: \~82%**

✅ **Data coverage:** over 697k tracks scored

---

## 🎵 Example Playlists

* [Top 15](https://open.spotify.com/playlist/5NEIQcJWFLmOFdu6hcubg5?si=99b0558f97ad45d0)
* [Top 15 Negatives](https://open.spotify.com/playlist/5aqy75889Ku3sMayCC0ryn?si=3d1441efda3646e4)
* [Rock](https://open.spotify.com/playlist/501wyVkxNQatCHOOWDS2GQ?si=c413325cd9304f67)
* [Pop](https://open.spotify.com/playlist/5Wu41xEU6AOwp42rdXE9Dd?si=5bc89d031dea4e15)
* [Indie](https://open.spotify.com/playlist/5imO7BLjC8LMR8XeWru6bO?si=70d3952471c64e17)
* [EDM](https://open.spotify.com/playlist/6GFflRxxRVdN6fU2ei0R1I?si=c0e7541a4b3d4482)
* [Folk](https://open.spotify.com/playlist/46Dd9AVfZouED8lgMo45xW?si=372e637feecf4123)

---

## 💻 Tech Stack

* **Python**: pandas, requests, scikit-learn, gensim
* **Spotify Web API** (+ Spotipy)
* **PostgreSQL**: custom Star Schema
* **Power BI**: analytics and visualization

---

## 🏁 Conclusion

✅ Personal recommendation engine outperforming Spotify’s own playlists
✅ Full ownership and transparency of data
✅ 35k+ plays analyzed, 700k+ tracks scored
✅ Ready-to-deploy BI dashboards and ML pipelines

> **Data-driven, user-centered, privacy-compliant recommendation system.**
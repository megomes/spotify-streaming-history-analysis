CREATE TABLE IF NOT EXISTS album (
    album_id SERIAL PRIMARY KEY,
    album_spotify_id VARCHAR(100),
    album_genius_id VARCHAR(100),
    title VARCHAR(250),
    release_date VARCHAR(100),
    total_tracks INTEGER
);

CREATE TABLE IF NOT EXISTS artist (
    artist_id SERIAL PRIMARY KEY,
    artist_spotify_id VARCHAR(100),
    artist_genius_id VARCHAR(100),
    title VARCHAR(250),
    instagram_name VARCHAR(100),
    twitter_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS music (
    music_id SERIAL PRIMARY KEY,
    album_id INTEGER,
    primary_artist_id INTEGER,
    writer_artist_id INTEGER,
    title VARCHAR(250),
    duration_ms FLOAT,
    popularity INTEGER,
    danceability FLOAT,
    energy FLOAT,
    music_key INTEGER,
    loudness FLOAT,
    mode INTEGER,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    time_signature FLOAT,
    genius_description VARCHAR(500),
    cover_count INTEGER,
    FOREIGN KEY (album_id) REFERENCES album (album_id),
    FOREIGN KEY (primary_artist_id) REFERENCES artist (artist_id),
    FOREIGN KEY (writer_artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE IF NOT EXISTS genre (
    genre_id SERIAL PRIMARY KEY,
    genre VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS music_artist (
    music_artist_id SERIAL PRIMARY KEY,
    music_id INTEGER,
    artist_id INTEGER,
    label VARCHAR(100),
    FOREIGN KEY (music_id) REFERENCES music (music_id),
    FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE IF NOT EXISTS album_artist (
    album_artist_id SERIAL PRIMARY KEY,
    album_id INTEGER,
    artist_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES album (album_id),
    FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE IF NOT EXISTS genre_artist (
    genre_artist_id SERIAL PRIMARY KEY,
    genre_id INTEGER,
    artist_id INTEGER,
    FOREIGN KEY (genre_id) REFERENCES genre (genre_id),
    FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE IF NOT EXISTS play (
    play_id SERIAL PRIMARY KEY,
    music_id INTEGER,
    end_time VARCHAR(100),
    ms_played FLOAT,
    FOREIGN KEY (music_id) REFERENCES music (music_id)
);

CREATE TABLE IF NOT EXISTS top_music (
    top_music_id SERIAL PRIMARY KEY,
    music_id INTEGER,
    top_year INTEGER,
    place INTEGER,
    FOREIGN KEY (music_id) REFERENCES music (music_id)
);

CREATE TABLE IF NOT EXISTS favorite (
    favorite_id SERIAL PRIMARY KEY,
    music_id INTEGER,
    favorite_year INTEGER,
    FOREIGN KEY (music_id) REFERENCES music (music_id)
);

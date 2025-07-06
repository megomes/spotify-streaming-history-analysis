CREATE TABLE IF NOT EXISTS album (
	album_id SERIAL PRIMARY KEY,
	album_spotify_uri VARCHAR(100),
	title VARCHAR(250),
	release_date DATE,
	total_tracks INTEGER,
	label TEXT,
	popularity INTEGER
);

CREATE TABLE IF NOT EXISTS artist (
	artist_id SERIAL PRIMARY KEY,
	artist_spotify_uri VARCHAR(100),
	name TEXT,
	followers INTEGER,
	popularity INTEGER
);

CREATE TABLE IF NOT EXISTS music (
	music_id SERIAL PRIMARY KEY,
	music_spotify_uri TEXT,
	name TEXT,
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
	time_signature FLOAT
);

CREATE TABLE IF NOT EXISTS genre (
	genre_id SERIAL PRIMARY KEY,
	genre VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS category (
	category_id SERIAL PRIMARY KEY,
	category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS genre_category (
	genre_category_id SERIAL PRIMARY KEY,
	genre_id INTEGER,
	category_id INTEGER,
	FOREIGN KEY (genre_id) REFERENCES genre (genre_id),
	FOREIGN KEY (category_id) REFERENCES category (category_id)
);

CREATE TABLE IF NOT EXISTS music_artist (
	music_artist_id SERIAL PRIMARY KEY,
	music_id INTEGER,
	artist_id INTEGER,
	FOREIGN KEY (music_id) REFERENCES music (music_id),
	FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE IF NOT EXISTS album_music (
	album_music_id SERIAL PRIMARY KEY,
	album_id INTEGER,
	music_id INTEGER,
	FOREIGN KEY (album_id) REFERENCES album (album_id),
	FOREIGN KEY (music_id) REFERENCES music (music_id)
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
	end_time TIMESTAMP,
	ms_played FLOAT,
	platform TEXT,
	ip_addr TEXT,
	reason_start TEXT,
	reason_end TEXT,
	shuffle TEXT,
	skipped TEXT,
	offline TEXT,
	FOREIGN KEY (music_id) REFERENCES music (music_id)
);

CREATE TABLE IF NOT EXISTS favorite (
	favorite_id SERIAL PRIMARY KEY,
	music_id INTEGER,
	year INTEGER,
	added_at TIMESTAMP,
	FOREIGN KEY (music_id) REFERENCES music (music_id)
);


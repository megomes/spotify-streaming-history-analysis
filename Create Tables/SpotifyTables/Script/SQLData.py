from Script.SQLConn import SQLConn
from Script.RAMData import RAMData

import sys

import uuid

class SQLData:
    __instance = None

    album = []
    artist = []
    music = []
    genre = []
    music_artist = []
    album_artist = []
    genre_artist = []
    play = []
    top_music = []
    favorite = []
    

    @staticmethod
    def instance():
        if not SQLData.__instance:
            SQLData.__instance = SQLData()
        return SQLData.__instance

    def checkMaxSize(self):
        if len(self.music) >= 1000:
            # time to save on db!
            self.save()
            return True
        return False

    def save(self):
        self.save_album()
        self.save_artist()
        self.save_music()
        self.save_genre()
        self.save_music_artist()
        self.save_album_artist()
        self.save_genre_artist()
        self.save_play()
        self.save_top_music()
        self.save_favorite()
        


    #############################
    # INSERT

    def insert_album(self, album):
        self.album.append(album)

    def insert_artist(self, artist):
        self.artist.append(artist)

    def insert_music(self, music):
        self.music.append(music)
        self.checkMaxSize()

    def insert_genre(self, genre):
        self.genre.append(genre)

    def insert_music_artist(self, music_artist):
        self.music_artist.append(music_artist)

    def insert_album_artist(self, album_artist):
        self.album_artist.append(album_artist)

    def insert_genre_artist(self, genre_artist):
        self.genre_artist.append(genre_artist)

    def insert_play(self, play):
        self.play.append(play)

    def insert_top_music(self, top_music):
        self.top_music.append(top_music)

    def insert_favorite(self, favorite):
        self.favorite.append(favorite)



    #############################
    # SAVE

    def save_album(self):
        valuesString = []
        for new_album in self.album:
            valuesString.append("""('%s','%s','%s','%s','%s',%s)""" % ( \
                                new_album.get('album_id', ''),
                                new_album.get('album_spotify_id', ''),
                                new_album.get('album_genius_id', ''),
                                new_album.get('title', ''),
                                new_album.get('release_date', ''),
                                new_album.get('total_tracks', 'null')
                            ))

        tabela = 'album'
        columns = """
            album_id,
            album_spotify_id,
            album_genius_id,
            title,
            release_date,
            total_tracks
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.album = []


    def update_album(self, album):
        keys_raw = list(album.keys())
        setValues = []
        for key in keys_raw:
            if key == 'album_id':
                continue
            if isinstance(album[key], float) or isinstance(album[key], int):
                setValues.append(key + ' = ' + str(album[key]))
            else:
                setValues.append(key + ' = \'' + str(album[key]) + '\'')

        if len(setValues) == 0:
            return

        updateString = f'UPDATE album SET %s WHERE album_id = %s' % (', '.join(setValues), album['album_id'])
        SQLConn.instance().cursor.execute(updateString)


    def save_artist(self):
        valuesString = []
        for new_artist in self.artist:
            valuesString.append("""('%s','%s','%s','%s','%s','%s')""" % ( \
                                new_artist.get('artist_id', ''),
                                new_artist.get('artist_spotify_id', ''),
                                new_artist.get('artist_genius_id', ''),
                                new_artist.get('title', ''),
                                new_artist.get('instagram_name', ''),
                                new_artist.get('twitter_name', '')
                            ))

        tabela = 'artist'
        columns = """
            artist_id,
            artist_spotify_id,
            artist_genius_id,
            title,
            instagram_name,
            twitter_name
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.artist = []


    def update_artist(self, artist):
        keys_raw = list(artist.keys())
        setValues = []
        for key in keys_raw:
            if key == 'artist_id':
                continue
            if isinstance(artist[key], float) or isinstance(artist[key], int):
                setValues.append(key + ' = ' + str(artist[key]))
            else:
                setValues.append(key + ' = \'' + str(artist[key]) + '\'')

        if len(setValues) == 0:
            return

        updateString = f'UPDATE artist SET %s WHERE artist_id = %s' % (', '.join(setValues), artist['artist_id'])
        SQLConn.instance().cursor.execute(updateString)


    def save_music(self):
        valuesString = []
        for new_music in self.music:
            valuesString.append("""('%s','%s','%s',%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s')""" % ( \
                                new_music.get('music_id', ''),
                                new_music.get('music_spotify_id', ''),
                                new_music.get('music_genius_id', ''),
                                new_music.get('album_id', 'null'),
                                new_music.get('title', ''),
                                new_music.get('duration_ms', 'null'),
                                new_music.get('popularity', 'null'),
                                new_music.get('danceability', 'null'),
                                new_music.get('energy', 'null'),
                                new_music.get('music_key', 'null'),
                                new_music.get('loudness', 'null'),
                                new_music.get('mode', 'null'),
                                new_music.get('speechiness', 'null'),
                                new_music.get('acousticness', 'null'),
                                new_music.get('instrumentalness', 'null'),
                                new_music.get('liveness', 'null'),
                                new_music.get('valence', 'null'),
                                new_music.get('tempo', 'null'),
                                new_music.get('time_signature', 'null'),
                                new_music.get('genius_description', ''),
                                new_music.get('lyrics', '')
                            ))

        tabela = 'music'
        columns = """
            music_id,
            music_spotify_id,
            music_genius_id,
            album_id,
            title,
            duration_ms,
            popularity,
            danceability,
            energy,
            music_key,
            loudness,
            mode,
            speechiness,
            acousticness,
            instrumentalness,
            liveness,
            valence,
            tempo,
            time_signature,
            genius_description,
            lyrics
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.music = []


    def update_music(self, music):
        keys_raw = list(music.keys())
        setValues = []
        for key in keys_raw:
            if key == 'music_id':
                continue
            if isinstance(music[key], float) or isinstance(music[key], int):
                setValues.append(key + ' = ' + str(music[key]))
            else:
                setValues.append(key + ' = \'' + str(music[key]) + '\'')

        if len(setValues) == 0:
            return

        updateString = f'UPDATE music SET %s WHERE music_id = %s' % (', '.join(setValues), music['music_id'])
        SQLConn.instance().cursor.execute(updateString)


    def save_genre(self):
        valuesString = []
        for new_genre in self.genre:
            valuesString.append("""('%s','%s')""" % ( \
                                new_genre.get('genre_id', ''),
                                new_genre.get('genre', '')
                            ))

        tabela = 'genre'
        columns = """
            genre_id,
            genre
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.genre = []


    def update_genre(self, genre):
        keys_raw = list(genre.keys())
        setValues = []
        for key in keys_raw:
            if key == 'genre_id':
                continue
            if isinstance(genre[key], float) or isinstance(genre[key], int):
                setValues.append(key + ' = ' + str(genre[key]))
            else:
                setValues.append(key + ' = \'' + str(genre[key]) + '\'')

        if len(setValues) == 0:
            return

        updateString = f'UPDATE genre SET %s WHERE genre_id = %s' % (', '.join(setValues), genre['genre_id'])
        SQLConn.instance().cursor.execute(updateString)


    def save_music_artist(self):
        valuesString = []
        for new_music_artist in self.music_artist:
            valuesString.append("""('%s',%s,%s,'%s')""" % ( \
                                new_music_artist.get('music_artist_id', ''),
                                new_music_artist.get('music_id', 'null'),
                                new_music_artist.get('artist_id', 'null'),
                                new_music_artist.get('label', '')
                            ))

        tabela = 'music_artist'
        columns = """
            music_artist_id,
            music_id,
            artist_id,
            label
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.music_artist = []


    def save_album_artist(self):
        valuesString = []
        for new_album_artist in self.album_artist:
            valuesString.append("""('%s',%s,%s)""" % ( \
                                new_album_artist.get('album_artist_id', ''),
                                new_album_artist.get('album_id', 'null'),
                                new_album_artist.get('artist_id', 'null')
                            ))

        tabela = 'album_artist'
        columns = """
            album_artist_id,
            album_id,
            artist_id
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.album_artist = []


    def save_genre_artist(self):
        valuesString = []
        for new_genre_artist in self.genre_artist:
            valuesString.append("""('%s',%s,%s)""" % ( \
                                new_genre_artist.get('genre_artist_id', ''),
                                new_genre_artist.get('genre_id', 'null'),
                                new_genre_artist.get('artist_id', 'null')
                            ))

        tabela = 'genre_artist'
        columns = """
            genre_artist_id,
            genre_id,
            artist_id
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.genre_artist = []


    def save_play(self):
        valuesString = []
        for new_play in self.play:
            valuesString.append("""('%s',%s,'%s',%s)""" % ( \
                                new_play.get('play_id', ''),
                                new_play.get('music_id', 'null'),
                                new_play.get('end_time', ''),
                                new_play.get('ms_played', 'null')
                            ))

        tabela = 'play'
        columns = """
            play_id,
            music_id,
            end_time,
            ms_played
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.play = []


    def save_top_music(self):
        valuesString = []
        for new_top_music in self.top_music:
            valuesString.append("""('%s',%s,%s,%s)""" % ( \
                                new_top_music.get('top_music_id', ''),
                                new_top_music.get('music_id', 'null'),
                                new_top_music.get('top_year', 'null'),
                                new_top_music.get('place', 'null')
                            ))

        tabela = 'top_music'
        columns = """
            top_music_id,
            music_id,
            top_year,
            place
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.top_music = []


    def save_favorite(self):
        valuesString = []
        for new_favorite in self.favorite:
            valuesString.append("""('%s',%s,%s)""" % ( \
                                new_favorite.get('favorite_id', ''),
                                new_favorite.get('music_id', 'null'),
                                new_favorite.get('favorite_year', 'null')
                            ))

        tabela = 'favorite'
        columns = """
            favorite_id,
            music_id,
            favorite_year
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.favorite = []



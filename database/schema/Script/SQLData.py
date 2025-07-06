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
    category = []
    genre_category = []
    music_artist = []
    album_music = []
    genre_artist = []
    play = []
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
        self.save_category()
        self.save_genre_category()
        self.save_music_artist()
        self.save_album_music()
        self.save_genre_artist()
        self.save_play()
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

    def insert_category(self, category):
        self.category.append(category)

    def insert_genre_category(self, genre_category):
        self.genre_category.append(genre_category)

    def insert_music_artist(self, music_artist):
        self.music_artist.append(music_artist)

    def insert_album_music(self, album_music):
        self.album_music.append(album_music)

    def insert_genre_artist(self, genre_artist):
        self.genre_artist.append(genre_artist)

    def insert_play(self, play):
        self.play.append(play)

    def insert_favorite(self, favorite):
        self.favorite.append(favorite)



    #############################
    # SAVE

    def save_album(self):
        valuesString = []
        for new_album in self.album:
            valuesString.append("""('%s','%s','%s','%s',%s,'%s',%s)""" % ( \
                                new_album.get('album_id', ''),
                                new_album.get('album_spotify_uri', ''),
                                new_album.get('title', ''),
                                new_album.get('release_date', ''),
                                new_album.get('total_tracks', 'null'),
                                new_album.get('label', ''),
                                new_album.get('popularity', 'null')
                            ))

        tabela = 'album'
        columns = """
            album_id,
            album_spotify_uri,
            title,
            release_date,
            total_tracks,
            label,
            popularity
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
            valuesString.append("""('%s','%s','%s',%s,%s)""" % ( \
                                new_artist.get('artist_id', ''),
                                new_artist.get('artist_spotify_uri', ''),
                                new_artist.get('name', ''),
                                new_artist.get('followers', 'null'),
                                new_artist.get('popularity', 'null')
                            ))

        tabela = 'artist'
        columns = """
            artist_id,
            artist_spotify_uri,
            name,
            followers,
            popularity
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
            valuesString.append("""('%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" % ( \
                                new_music.get('music_id', ''),
                                new_music.get('music_spotify_uri', ''),
                                new_music.get('name', ''),
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
                                new_music.get('time_signature', 'null')
                            ))

        tabela = 'music'
        columns = """
            music_id,
            music_spotify_uri,
            name,
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
            time_signature
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


    def save_category(self):
        valuesString = []
        for new_category in self.category:
            valuesString.append("""('%s','%s')""" % ( \
                                new_category.get('category_id', ''),
                                new_category.get('category', '')
                            ))

        tabela = 'category'
        columns = """
            category_id,
            category
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.category = []


    def update_category(self, category):
        keys_raw = list(category.keys())
        setValues = []
        for key in keys_raw:
            if key == 'category_id':
                continue
            if isinstance(category[key], float) or isinstance(category[key], int):
                setValues.append(key + ' = ' + str(category[key]))
            else:
                setValues.append(key + ' = \'' + str(category[key]) + '\'')

        if len(setValues) == 0:
            return

        updateString = f'UPDATE category SET %s WHERE category_id = %s' % (', '.join(setValues), category['category_id'])
        SQLConn.instance().cursor.execute(updateString)


    def save_genre_category(self):
        valuesString = []
        for new_genre_category in self.genre_category:
            valuesString.append("""('%s',%s,%s)""" % ( \
                                new_genre_category.get('genre_category_id', ''),
                                new_genre_category.get('genre_id', 'null'),
                                new_genre_category.get('category_id', 'null')
                            ))

        tabela = 'genre_category'
        columns = """
            genre_category_id,
            genre_id,
            category_id
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.genre_category = []


    def save_music_artist(self):
        valuesString = []
        for new_music_artist in self.music_artist:
            valuesString.append("""('%s',%s,%s)""" % ( \
                                new_music_artist.get('music_artist_id', ''),
                                new_music_artist.get('music_id', 'null'),
                                new_music_artist.get('artist_id', 'null')
                            ))

        tabela = 'music_artist'
        columns = """
            music_artist_id,
            music_id,
            artist_id
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.music_artist = []


    def save_album_music(self):
        valuesString = []
        for new_album_music in self.album_music:
            valuesString.append("""('%s',%s,%s)""" % ( \
                                new_album_music.get('album_music_id', ''),
                                new_album_music.get('album_id', 'null'),
                                new_album_music.get('music_id', 'null')
                            ))

        tabela = 'album_music'
        columns = """
            album_music_id,
            album_id,
            music_id
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.album_music = []


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
            valuesString.append("""('%s',%s,'%s',%s,'%s','%s','%s','%s','%s','%s','%s')""" % ( \
                                new_play.get('play_id', ''),
                                new_play.get('music_id', 'null'),
                                new_play.get('end_time', ''),
                                new_play.get('ms_played', 'null'),
                                new_play.get('platform', ''),
                                new_play.get('ip_addr', ''),
                                new_play.get('reason_start', ''),
                                new_play.get('reason_end', ''),
                                new_play.get('shuffle', ''),
                                new_play.get('skipped', ''),
                                new_play.get('offline', '')
                            ))

        tabela = 'play'
        columns = """
            play_id,
            music_id,
            end_time,
            ms_played,
            platform,
            ip_addr,
            reason_start,
            reason_end,
            shuffle,
            skipped,
            offline
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.play = []


    def save_favorite(self):
        valuesString = []
        for new_favorite in self.favorite:
            valuesString.append("""('%s',%s,%s,'%s')""" % ( \
                                new_favorite.get('favorite_id', ''),
                                new_favorite.get('music_id', 'null'),
                                new_favorite.get('year', 'null'),
                                new_favorite.get('added_at', '')
                            ))

        tabela = 'favorite'
        columns = """
            favorite_id,
            music_id,
            year,
            added_at
        """
        insertString = f'INSERT INTO %s (%s) VALUES %s' % (tabela, columns, (",".join(valuesString) ) )
        if len(valuesString) == 0:
            return
        insertString = insertString.replace('\'null\'', 'null')
        SQLConn.instance().cursor.execute(insertString)
        self.favorite = []



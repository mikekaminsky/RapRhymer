#get_songs.py
#Michael Kaminsky

#Import libraries
#https://github.com/rouxpz/pygenius
from pygenius import artists, songs, wordsearch
import sqlite3

#Set up sqlite connection
conn = sqlite3.connect('/Users/ccUser/sqlitedbs/rapgenerator.db')
conn.text_factory = str
c = conn.cursor()

#Set up database
c.execute('''
        DROP TABLE IF EXISTS songs;
''')
c.execute('''
        CREATE TABLE songs (id integer primary key, title text, artist text);
''')

AristList = [
       'kanye west',
       'migos',
       'drake',
       'big krit',
       'lupe fiasco',
       'joey badass',
       'meek mill',
       'logic',
       'danny brown',
       'rick ross',
       'lil wayne',
       'jay z',
       '2 chainz',
        ]

for artist in AristList:
    print(artist)
    Songs = songs.findAllSongs(artist, 'titles')
    used = list()
    for song in Songs:
        if song not in used:
            if ' by ' not in song and 'Album Art' not in song and 'Credits' not in song and 'Interview' not in song and 'Skit' not in song and 'Dates' not in song:
                print song
                used.append(song)
                c.execute('insert into songs(title, artist) values (?,?)', (song, artist))
    conn.commit()

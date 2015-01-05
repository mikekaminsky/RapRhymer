#!/usr/bin/python
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
        DROP TABLE IF EXISTS kanyesongs;
''')
c.execute('''
        CREATE TABLE kanyesongs (id integer primary key, title text);
''')

KanyeSongs = songs.findAllSongs('Kanye West', 'titles')

for song in KanyeSongs:
    if ' by ' not in song and 'Album Art' not in song and 'Credits' not in song and 'Interview' not in song and 'Skit' not in song and 'Dates' not in song:
        print song
        c.execute('insert into kanyesongs(title) values (?)', (song, ))

# Save (commit) the changes
conn.commit()


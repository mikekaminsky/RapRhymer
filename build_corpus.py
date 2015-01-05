#!/usr/bin/python
#build_corpus.py
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
        DROP TABLE IF EXISTS kanyelyrics;
''')
c.execute('''
        CREATE TABLE kanyelyrics (id integer primary key, title_id integer, lyrics text);
''')

#Get lyrics for all of the songs

c.execute("select * from kanyesongs where title not like '%dates%'")
for title in c.fetchall():
    #print(title[0])
    #print(title[1])
    try:
        lyrics = songs.searchSong('kanye west', title[1].lower(), 'lyrics')
        for lyric in lyrics:
            #print(lyric)
            c.execute('insert into kanyelyrics(title_id) values (?)', (title[0], ))
            c.execute('insert into kanyelyrics(lyrics) values (?)', (lyric, ))
    except:
        pass

# Save (commit) the changes
conn.commit()

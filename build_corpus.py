#!/usr/bin/python
#build_corpus.py
#Michael Kaminsky

#Import libraries
#https://github.com/rouxpz/pygenius
from pygenius import artists, songs, wordsearch
import sqlite3
execfile("poetry.py")

#Set up sqlite connection
conn = sqlite3.connect('/Users/ccUser/sqlitedbs/rapgenerator.db')
conn.text_factory = str
c = conn.cursor()

#Set up database
c.execute('''
        DROP TABLE IF EXISTS lyrics;
''')
c.execute('''
        CREATE TABLE lyrics (id integer primary key autoincrement, title_id integer, lyrics text, lastword text, rhymesyls text);
''')

#Get lyrics for all of the songs

c.execute("select * from songs where title not like '%dates%'")
for title in c.fetchall():
    try:
        lyrics = songs.searchSong(title[2].lower(), title[1].lower(), 'lyrics')
        for lyric in lyrics:
            for line in lyric.split('\n'):
                lastword = line.rsplit(None, 1)[-1]
                syls = str(rhymesyls(lastword))
                c.execute('insert into lyrics(title_id,lyrics,lastword,rhymesyls) values (?,?,?,?)', (title[0],line,lastword, syls))
                conn.commit()
    except:
        pass

# Save (commit) the changes

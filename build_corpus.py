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
        DROP TABLE IF EXISTS kanyelyrics;
''')
c.execute('''
        CREATE TABLE kanyelyrics (id integer primary key autoincrement, title_id integer, lyrics text, lastword text, rhymesyls text);
''')

#Get lyrics for all of the songs

c.execute("select * from kanyesongs where title not like '%dates%' limit 1000")
for title in c.fetchall():
    try:
        lyrics = songs.searchSong('kanye west', title[1].lower(), 'lyrics')
        for lyric in lyrics:
            lastword = lyric.rsplit(None, 1)[-1]
            syls = str(rhymesyls(lastword))
            #print(syls)
            c.execute('insert into kanyelyrics(title_id,lyrics,lastword,rhymesyls) values (?,?,?,?)', (title[0],lyric,lastword, syls))

    except:
        pass

# Save (commit) the changes
conn.commit()

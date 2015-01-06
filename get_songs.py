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


#dbupdate.py
#Michael Kaminsky

import sqlite3
import os.path
import re
from pygenius import artists, songs, wordsearch
execfile("rhymes.py")

class DBUpdate(object):

    """
    Class to serve as a container for updating the rapgenerator database
    """
    def __init__(self, dbloc = None):

        print "dbUpdate object created"
        defaultloc = "/usr/local/sqlite"

        if dbloc is None:
            if os.path.exists(defaultloc + '/rapgenerator.db'):
                conn=sqlite3.connect(defaultloc+'/rapgenerator.db')
                print("Database found")
            else:
                print("ERROR: Databse not found. Try using DBSetup()")
                raise
        else:
            if os.path.exists(dbloc + '/rapgenerator.db'):
                conn=sqlite3.connect(dbloc+'/rapgenerator.db')
                print("Database found")
            else:
                print("ERROR: Databse not found. Try using DBSetup()")
                raise

        self.conn = conn

    def AddSongs(self, ArtistList):
        """
        Method to find and add new songs to the songs table.
        """

        "Terms that identify songs that aren't really songs"
        conn = self.conn
        conn.text_factory = str
        c = conn.cursor()

        BadTerms = [
               ' by ', 
               'album art', 
               'credits', 
               'interview', 
               'skit', 
               'dates', 
               'interview'
                ]

        if ArtistList is None:
            return "You must provide a list of artists for whom to find songs."
        else:
            for artist in ArtistList:
                print("Finding songs for " + artist)
                Songs = songs.findAllSongs(artist)
                used = list()
                for song in Songs:
                    print(song[1])
                    c.execute("select count(*) from songs where title = (?) and artist = (?)", (song[1], artist))
                    checkindb = c.fetchall()
                    if checkindb[0][0] == 0:
                        if song[1] not in used:
                            if not [i for i, x in enumerate(BadTerms) if x in song[1]]:
                                used.append(song[1])
                                c.execute('insert into songs(title, artist, url) values (?,?,?)', (song[1], artist, song[0]))
                    conn.commit()

    def AddLyrics(self):
        """
        Method to add lyrics for any songs that don't have them
        """

        conn = self.conn
        conn.text_factory = str
        c = conn.cursor()

        c.execute("select songs.id, artist, title, url from songs left join lyrics on songs.id = lyrics.song_id where lyrics.song_id is null")
        obs = c.fetchall()
        for title in obs:
            print("Looking for lyrics for " + title[1] + title[2])
            try:
                lyrics = songs.searchURL(title[3], 'lyrics')
                for lyric in lyrics:
                    for line in lyric.split('\n'):
                        if line:
                            lastword = line.rsplit(None, 1)[-1]
                            lastword = re.sub('[^A-Za-z0-9\s]+', '', lastword)
                            syls = str(rhymesyls(lastword))
                            if syls != "NORHYME":
                                c.execute('insert into lyrics(song_id,lyrics,lastword,rhymesyls) values (?,?,?,?)', (title[0],line,lastword, syls))
                                conn.commit()
            except Exception as e:
                print(e)
                pass

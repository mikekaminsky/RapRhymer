#dbupdate.py
#Michael Kaminsky

import sqlite3
import os.path
from pygenius import artists, songs, wordsearch
execfile("poetry.py")

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
                Titles = songs.findAllSongs(artist, 'titles')
                used = list()
                for title in Titles:
                    print(title)
                    c.execute("select count(*) from songs where title = (?) and artist = (?)", (title, artist))
                    checkindb = c.fetchall()
                    if checkindb[0][0] == 0:
                        if title not in used:
                            if not [i for i, x in enumerate(BadTerms) if x in title]:
                                used.append(title)
                                c.execute('insert into songs(title, artist) values (?,?)', (title, artist))
                    conn.commit()

    def AddLyrics(self):
        """
        Method to add lyrics for any songs that don't have them
        """

        conn = self.conn
        conn.text_factory = str
        c = conn.cursor()

        c.execute("select songs.id, artist, title from songs left join lyrics on songs.id = lyrics.title_id where lyrics.title_id is null")
        obs = c.fetchall()
        for title in obs:
            print("Looking for lyrics for " + title[2])
            try:
                lyrics = songs.searchSong(title[1].lower(), title[2].lower(), 'lyrics')
                for lyric in lyrics:
                    for line in lyric.split('\n'):
                        lastword = line.rsplit(None, 1)[-1]
                        syls = str(rhymesyls(lastword))
                        c.execute('insert into lyrics(title_id,lyrics,lastword,rhymesyls) values (?,?,?,?)', (title[0],line,lastword, syls))
                        conn.commit()
                    print("Lyrics added for " + title)
            except:
                print("Lyrics not found.")
                pass

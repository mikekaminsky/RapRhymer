#rapgenerator.py
#Michael Kaminsky

#Import libraries
import sqlite3
import pyttsx
import random
import string
import os.path

class RapGenerator(object):
    """
    Class to serve as a container for the RapGenerator
    """

    def __init__(self, dbloc = None):
        print "RapGenerator object created"
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

    def CreateRap(self, SongLength = None):
        """
        Method for generating a rap
        """


        conn = self.conn
        conn.text_factory = str
        c = conn.cursor()

        #Problematic lyrics
        removelist = [
                '[Verse 1]',
                '[Verse 2]',
                '[Verse]',
                '[Hook]',
                '[Intro]',
                ]

        #Number of couplets
        if SongLength is None:
            SongLength = 5

        Song = list()

        #get number of lyrics
        c.execute("select count(*) from lyrics where lyrics is not null")
        numLyrics = c.fetchone()[0]

        #Grab random lyric
        def getrandom():
            rand = random.randrange(0, numLyrics)
            c.execute("select * from lyrics join songs on (lyrics.title_id = songs.id) where lyrics is not null and artist != 'migos' and lyrics.id = (?)", (rand,))
            data = c.fetchall()
            return data

        def cleanlyric(lyric):
            temp = lyric
            for removal in removelist:
                temp = string.replace(temp, removal, '')
            return temp

        i = 0
        while i < SongLength:
            obs = getrandom()
            lyric1 = obs[0][2]
            rhyme = obs[0][4]
            title1 = obs[0][1]
            c.execute("select * from lyrics where lyrics is not null and rhymesyls = (?) and lyrics != (?) and title_id != (?) limit 1", (rhyme, lyric1, title1))
            rhymeobs = c.fetchall()
            if rhymeobs:
                lyric1 = cleanlyric(lyric1)
                lyric2 = rhymeobs[0][2]
                lyric2 = cleanlyric(lyric2)
                Song.append(lyric1)
                Song.append(lyric2)
                Song.append("\n")
                i = i+1
        
        self.rap = Song
        return Song

    def ReadRap(self, Song = None):
        """
        Method for generating a rap
        """

        if Song is None:
            Song = self.rap

        engine = pyttsx.init()
        for lyric in Song:
            print(lyric)
            engine.say(lyric)
        return engine.runAndWait()

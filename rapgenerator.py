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

        #Number of couplets
        if SongLength is None:
            SongLength = 5

        Song = list()

        #get number of lyrics
        c.execute("select count(*) from lyrics where lyrics is not null")
        numLyrics = c.fetchone()[0]

        notsongwords = set(["interview", "rant"])
        notlyricwords = set(["[", "]", "(", ")", "produced by", "mixed by"])

        #Grab random lyric
        def getrandom():
            rand = random.randrange(0, numLyrics)
            c.execute("""select * 
                         from lyrics 
                         join songs 
                            on (lyrics.title_id = songs.id) 
                         where 
                            lyrics is not null 
                            and lyrics.id = (?)""", (rand,))
            data = c.fetchall()
            nwords = len(str.split(data[0][2]))
            if data is not None and not any(word in data[0][2] for word in notlyricwords)and nwords > 2 and nwords < 25 and not any(word in notsongwords for word in data[0][6].split()):
                return data
            else:
                return(getrandom())

        def pickrhyme(allrhymeobs):
            rhymeobs = random.choice(allrhymeobs)
            nwords = len(str.split(rhymeobs[2]))
            if rhymeobs is not None and not any(word in rhymeobs[2] for word in notlyricwords) and nwords > 2 and nwords < 25 and not any(word in notsongwords for word in rhymeobs[5].split()):
                return rhymeobs
            else:
                return(pickrhyme(allrhymeobs))

        i = 0
        while i < SongLength:
            obs = getrandom()
            lyric1 = obs[0][2]
            lastword1 = obs[0][3]
            rhyme = obs[0][4]
            title1 = obs[0][1]
            c.execute("""select 
                            lyrics.*,
                            songs.title
                         from lyrics 
                         join songs
                            on (lyrics.title_id = songs.id) 
                         where 
                            lyrics is not null 
                            and rhymesyls = (?) 
                            and lower(lastword) != (?) 
                            and title_id != (?) """, (rhyme, lastword1.lower(), title1))
            allrhymeobs = c.fetchall()
            rhymeobs = pickrhyme(allrhymeobs)
            if rhymeobs:
                lyric2 = rhymeobs[2]
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

        #engine = pyttsx.init()
        for lyric in Song:
            print(lyric)
            #engine.say(lyric)
        #return engine.runAndWait()

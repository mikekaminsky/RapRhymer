#rapgenerator.py
#Michael Kaminsky

#Import libraries
import sqlite3
import pyttsx
import nltk
import random
import poetry
import string

#Set up sqlite connection
conn = sqlite3.connect('/Users/ccUser/sqlitedbs/rapgenerator.db')
c = conn.cursor()

#http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
#get number of lyrics
c.execute("select count(*) from lyrics where lyrics is not null")
numLyrics = c.fetchone()[0]

#Grab random lyric
def getrandom():
    rand = random.randrange(0, numLyrics)
    c.execute("select * from lyrics join songs on (lyrics.title_id = songs.id) where lyrics is not null and artist != 'migos' and lyrics.id = (?)", (rand,))
    data = c.fetchall()
    return data

#Number of couplets
SongLength = 5
Song = list()

removelist = [
        '[Verse 1]',
        '[Verse 2]',
        '[Verse]',
        '[Hook]',
        '[Intro]',
        ]

def cleanlyric(lyric):
    temp = lyric
    for removal in removelist:
        temp = string.replace(temp, removal, '')
    return temp

i = 0
while i < SongLength:
#for i in range(0, SongLength):
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
#speak song

engine = pyttsx.init()
for lyric in Song:
    print(lyric)
    engine.say(lyric)

engine.runAndWait()

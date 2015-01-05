#!/usr/bin/python
#rapgenerator.py
#Michael Kaminsky

#Import libraries
import sqlite3
import pyttsx
import nltk
import random
import poetry

#Set up sqlite connection
conn = sqlite3.connect('/Users/ccUser/sqlitedbs/rapgenerator.db')
c = conn.cursor()

#http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
#get number of lyrics
c.execute("select count(*) from kanyelyrics where lyrics is not null")
numLyrics = c.fetchone()[0]

#Grab random lyric
def getrandom():
    rand = random.randrange(0, numLyrics)
    c.execute("select * from kanyelyrics where lyrics is not null and id = (?)", (rand,))
    data = c.fetchall()
    return data

#Number of couplets
SongLength = 5
Song = list()


i = 0
while i < SongLength:
#for i in range(0, SongLength):
    obs = getrandom()
    lyric1 = obs[0][2]
    rhyme = obs[0][4]
    c.execute("select * from kanyelyrics where lyrics is not null and rhymesyls = (?) and lyrics != (?) limit 1", (rhyme, lyric1))
    rhymeobs = c.fetchall()
    if rhymeobs:
        lyric1 = string.replace(lyric1,'[Verse 1]', '')
        lyric1 = string.replace(lyric1,'[Verse 2]', '')
        lyric1 = string.replace(lyric1,'[Verse]', '')
        lyric1 = string.replace(lyric1,'[Hook]', '')
        lyric1 = string.replace(lyric1,'[Intro]', '')
        lyric2 = rhymeobs[0][2]
        lyric2 = string.replace(lyric2,'[Verse 1]', '')
        lyric2 = string.replace(lyric2,'[Verse 2]', '')
        lyric2 = string.replace(lyric2,'[Verse]', '')
        lyric1 = string.replace(lyric1,'[Hook]', '')
        lyric1 = string.replace(lyric1,'[Intro]', '')
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

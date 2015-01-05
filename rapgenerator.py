#!/usr/bin/python
#rapgenerator.py
#Michael Kaminsky

#Import libraries
import sqlite3
import pyttsx
import nltk
import random

#Set up sqlite connection
conn = sqlite3.connect('/Users/ccUser/sqlitedbs/rapgenerator.db')
c = conn.cursor()

#http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

def doTheyRhyme ( word1, word2 ):
  # first, we don't want to report 'glue' and 'unglue' as rhyming words
  # those kind of rhymes are LAME
  if word1.find ( word2 ) == len(word1) - len ( word2 ):
      return False
  if word2.find ( word1 ) == len ( word2 ) - len ( word1 ): 
      return False
  return word1 in rhyme ( word2, 1 )


#get number of lyrics
c.execute("select count(*) from kanyelyrics where lyrics is not null")
numLyrics = c.fetchone()[0]


c.execute("select id, lyrics from kanyelyrics where lyrics is not null")
all_lyrics = c.fetchall()

#Grab random lyric
def getrandom():
    rand = random.randrange(0, numLyrics)
    data = all_lyrics[rand][1]
    return data

#Number of couplets
SongLength = 1
Song = list()

for i in range(0, SongLength):
    #Logic:
    # 1. Find a random lyric
    # 2. Find another random lyric
    # 3. If they rhyme, output the lyrics
    # 4. If not, repeat steps 2 and 3 10 times
    # 5. If after 10 times, then throw out the first random lyric and start over
    j = 0
    while j < 5:
        lyric1 = getrandom()
        lastword1 = lyric1.rsplit(None, 1)[-1]
        k = 0
        while k < 5:
            lyric2 = getrandom()
            lastword2 = lyric2.rsplit(None, 1)[-1]
            match = doTheyRhyme(lastword1, lastword2)
            k = k + 1
            if match:
                Song.append(lyric1)
                Song.append(lyric2)
                k = 5
                j = 5
        j = j + 1

#j = 0
#for i in range(0, SongLength):
    #while j < 10:
        #print(i)
        #match = False
        #lyric1 = getrandom()
        #lastword1 = lyric1.rsplit(None, 1)[-1]
        #print(lyric1)
        #print(lastword1)
        #k = 0 
        #while match == False and k < 10:
            #lyric2 = getrandom()
            #lastword2 = lyric2.rsplit(None, 1)[-1]
            #print(j)
            #print(lyric2)
            #print(lastword2)
            #match = doTheyRhyme(lastword1, lastword2)
            #print (doTheyRhyme(lastword1, lastword2))
            #k = k + 1 
        #j = j+1
    #Song.append(lyric1)
    #Song.append(lyric2)


#Speak song
print(Song)
engine = pyttsx.init()
for lyric in Song:
    engine.say(lyric)
engine.runAndWait()

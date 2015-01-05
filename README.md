#RapGenerator

A proof-of-concept for a rap music generation app.

##Proof of Concept:
1. Build corpus of lyrics
  * Currently jsut doing Kanye Lyrics
2. Write script that creates couplets.
  * First choose a random lyric.
  * Then start at a random place in the corpus, and go until you find a rhyme.
3. Save the 'song' 
4. Have Python read the song line-by-line.

##TODO:
1. Compile database of song lyrics (the more the better)
  * Using sqlite for now. Should switch to postgresql for production work.
  * Need one row per line. Should have the following associated information:
    * Artist
    * Album
    * Song ID
2. Improve how python speaks?
3. Add potential song structure (verse, chorus, hook)?

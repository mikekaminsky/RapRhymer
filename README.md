#RapGenerator

A proof-of-concept for a rap music generation app.

##Proof of Concept:
1. Build corpus of lyrics
  * Currently just doing Kanye Lyrics
2. Write script that creates couplets.
  * First choose a random lyric.
  * Select all lyrics that have the same last sylable
  * Choose among potential matches randomly (needs work).
3. Save the 'song' 
4. Have Python read the song line-by-line.

##TODO:
1. Compile database of song lyrics (the more the better)
  * Using sqlite for now. Should switch to postgresql for production work.
  * Need to improve scraping. [This library](https://github.com/pconner03/rapgenius.py) looks like it might be better.
2. Improve rhyme engine.
  * I think we can get some big gains in rhyme skill just by being a bit smarter about how we determine what the right 'rhyme syllables' are. Need to do some research on how the syllable maps work.
3. Improve how python speaks (pitch, pauses, rhythm?)
4. Add potential song structure (verse, chorus, hook)?

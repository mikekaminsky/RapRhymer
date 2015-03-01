#RapRhymer

A Library for scraping rap lyrics and generating a rhyme index.

##Relied upon:
* [Nantucket](https://github.com/DanielleSucher/Nantucket)
* [Pygenius](https://github.com/rouxpz/pygenius)

##TODO:
1. [ ] Update documentation.
  * [ ] Add examples:
2. [ ] Improve DB setup and connection process. 
3. [ ] Improve rhyme engine.
  * [ ] Improve rhyme index for multi-syllabic rhymes Proposed rule:
    * [ ] Starting from the end of the word keep leters until you hit a syllable break (identified by a number in the dictionary), then take letters going backwards until you hit a vowel. 

#rhymes.py
#Based on code by Danielle Sucher
#https://github.com/DanielleSucher/Nantucket/blob/master/poetry.py
#Updated by Michael Kaminsky

from curses.ascii import isdigit
from nltk.corpus import cmudict
d = cmudict.dict()

def approx_nsyl(word):
    digraphs = {"ai", "au", "ay", "ea", "ee", "ei", "ey", "oa", "oe", "oi", "oo", "ou", "oy", "ua", "ue", "ui"}
    # Ambiguous, currently split: ie, io
    # Ambiguous, currently kept together: ui
    count = 0
    array = re.split("[^aeiouy]+", word.lower())
    for i, v in enumerate(array):
        if len(v) > 1 and v not in digraphs:
            count += 1
        if v == '':
            del array[i]
    count += len(array)
    if re.search("(?<=\w)(ion|ious|(?<!t)ed|es|[^lr]e)(?![a-z']+)", word.lower()):
        count -= 1
    if re.search("'ve|n't", word.lower()):
        count += 1
    return count

def nsyl(word):
    # return the min syllable count in the case of multiple pronunciations
    if not word.lower() in d:
        return approx_nsyl(word)
    return min([len([y for y in x if isdigit(str(y[-1]))]) for x in d[word.lower()]])

def rhymesyls(word):
    if word.lower() in d:
        list1 = min(d[word.lower()], key=len)
        outlist = str()
        i = -1
        while i >= 0 - len(list1):
            if isdigit(str(list1[i][-1])):
                outlist = list1[i][:-1]
                if i != -1:
                    outlist = outlist + ' ' + list1[i + 1:][0]
                return outlist
            i -= 1
        return outlist
    else:
        return "NORHYME"


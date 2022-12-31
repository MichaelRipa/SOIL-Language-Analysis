#! /usr/bin/env python3

import epitran
import re
import operator
from copy import deepcopy

class Lexicon:

    def __init__(self):
        '''Lexicon()
        Allows for retrival and simple phonetic analyis of a lexicon.
        '''
        self.epi = epitran.Epitran('eng-Latn',ligatures=True)
        self.lexicon = []

    def load_lexicon(self,func,*args):
        self.lexicon = func(*args)

    def lexicon_to_ipa(self):
        '''lexicon_to_ipa()
        Uses epitran to transcribe each word in existing lexicon to ipa, and stores the result in `lex_ipa`. 
        '''
        self.lex_ipa = deepcopy(self.lexicon)
        #This takes roughly 1 minute, English transliteration is extremely slow
        for entry in self.lex_ipa:
            entry[0] = self.epi.transliterate(entry[0])

    def partition(self):
        #TODO: Better design
        assert hasattr(self,'lexicon') and hasattr(self,'lex_ipa')
        
        # This is a little bit messy, probably a more clean way of doing this
        sentiment = ['pos' if float(entry[1]) > 0 else 'neg' for entry in self.lexicon]
        positive = []
        positive_ipa = []
        negative = []
        negative_ipa = []

        for i in range(len(self.lexicon)):
            if sentiment[i] == 'pos':
                positive.append(self.lexicon[i])
                positive_ipa.append(self.lex_ipa[i])
            else:
                negative.append(self.lexicon[i])
                negative_ipa.append(self.lex_ipa[i])

        lex_pos = Lexicon()
        lex_pos.lexicon = positive
        lex_pos.lex_ipa = positive_ipa
        lex_neg = Lexicon()
        lex_neg.lexicon = negative
        lex_neg.lex_ipa = negative_ipa
        
        return lex_pos , lex_neg

    def create_histogram(self,normalize=True):
        histogram = {}
        for entry in self.lex_ipa:
            word = entry[0]
            for char in word:
                if char in histogram.keys():
                    histogram[char] += 1
                else:
                    histogram[char] = 1
        return dict(
                sorted(
                    histogram.items(),key=operator.itemgetter(1),reverse=True
                    )
                )



#TODO: Document better
def vadar_loader(*args):
    '''Loads the vadar corpus provided a path'''
    path = args[0]
    f = open(path,'r')
    raw = f.read()
    f.close()

    rows = raw.split('\n')
    #This creates a list of triples containing word, sentiment and valence
    entries = [result.split('\t')[0:3] for result in rows]

    # Subset of vadar corpus containing full length words
    return entries[441:-17]

class VadarLoader:

    def __init__(self,kwargs):
        #Set up the function to load the lexicon
        assert 'path' in kwargs
        


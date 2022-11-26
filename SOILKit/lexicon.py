#! /usr/bin/env python3

import epitran

class Lexicon:

    def __init__(self):
        '''Lexicon()
        Allows for retrival and simple phonetic analyis of a lexicon.
        '''
        self.epi = epitran.Epitran('eng-Latn')
        self.lex = []

    def load_lexicon(self,path):
        pass

    def lexicon_to_ipa(self):
        '''lexicon_to_ipa()
        Uses epitran to transcribe each word in existing lexicon to ipa, and stores the result in `lex_ipa`. 
        '''
        self.lex_ipa = []
        for word in self.lex:
            ipa = self.epi.transliterate(word)
            self.lex_ipa.append(ipa)


    def create_histogram(self):
        pass



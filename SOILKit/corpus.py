#! /usr/bin/env python3

from SOILKit.header import *
import os 
import re
import csv
import sys
import pandas as pd
import epitran
import numpy as np
from nltk import word_tokenize 
from nltk import sent_tokenize
from nltk import FreqDist
from nltk.util import ngrams
from nltk.lm.preprocessing import pad_both_ends
from nltk.lm.preprocessing import padded_everygram_pipeline
from abc import ABC, abstractmethod

#Allow large csv files to be opened
csv.field_size_limit(sys.maxsize)

class Corpus_Generator:

    @staticmethod
    def __load_corpus(language=None):

        assert type(language) == str
        assert language in LANGUAGES

        #Check if corpus files created locally 
        os.chdir(TOKEN_PATH)
        #os.chdir(TEST_PATH)

        missing_words = not os.path.isfile(f'{language}_words.csv') 
        missing_sents= not os.path.isfile(f'{language}_sents.csv') 
        missing_raw = not os.path.isfile(f'{language}_raw.csv') 
        missing_words_ipa = not os.path.isfile(f'{language}_words_ipa.csv') 
        missing_sents_ipa = not os.path.isfile(f'{language}_sents_ipa.csv') 


        # Create corpus files if missing from TOKEN_PATH
        Corpus_Generator._Corpus_Generator__update_corpus(missing_words,missing_sents,missing_raw,missing_words_ipa,missing_sents_ipa,language)
        words = Corpus_Generator._Corpus_Generator__read_from_csv(f'{language}_words.csv')
        sents = Corpus_Generator._Corpus_Generator__read_from_csv(f'{language}_sents.csv')
        raw = Corpus_Generator._Corpus_Generator__read_from_csv(f'{language}_raw.csv')
        words_ipa = Corpus_Generator._Corpus_Generator__read_from_csv(f'{language}_words_ipa.csv')
        sents_ipa = Corpus_Generator._Corpus_Generator__read_from_csv(f'{language}_sents_ipa.csv')
        

        os.chdir(SCRIPT_PATH)

        return words,sents,raw,words_ipa,sents_ipa


    @staticmethod
    def __update_corpus(missing_words,missing_sents,missing_raw,missing_words_ipa,missing_sents_ipa,language):

        #Check whether anything needs to be updated
        if True not in [missing_words,missing_sents,missing_raw,missing_words_ipa,missing_sents_ipa]:
            return

        
        DOCUMENT_PATH = os.path.join(CORPUS_PATH, f'{language.capitalize()}')
        os.chdir(DOCUMENT_PATH)
        #os.chdir(TEST_PATH)
        l_index = LANGUAGES.index(language)
        epi = epitran.Epitran(LANGUAGE_CODES[l_index])
        
        document_names = os.listdir()
        raw = ''
        for book in document_names:
            if book.endswith('.txt'):
                f = open(book,'r',encoding='utf-8')
                raw += f.read().lower()
                f.close()



        # Create list of tokens and IPA conversions 

        tokens = word_tokenize(raw,language=language)
        tokens = [word for word in tokens if word.isalpha()]
        tokens = list(set(tokens))
        np.random.shuffle(tokens)
        ipa = [epi.transliterate(word) for word in tokens]
        Corpus_Generator._Corpus_Generator__strings_to_csv(tokens,f'{language}_words.csv')
        Corpus_Generator._Corpus_Generator__strings_to_csv(ipa,f'{language}_words_ipa.csv')
                
        if missing_sents or missing_sents_ipa:
            sents = Corpus_Generator._Corpus_Generator__tokenize_sents(raw,l=language)
            sents_ipa = []
            for s in sents:
                cur_sent = ''
                for word in s.split(' '):
                    if word in tokens:
                        cur_sent += ipa[tokens.index(word)] + ' '
                sents_ipa.append(cur_sent)

#            sents_ipa = [ ipa[tokens.index(word)] + ' ' for s in sents for word in s.split(' ') if word in tokens]
#            sents_ipa = [epi.transliterate(sent) for sent in sents]
            
            #Jan 12th : Proposed method of writing the new csv files
            Corpus_Generator._Corpus_Generator__strings_to_csv(sents,f'{language}_sents.csv')
            Corpus_Generator._Corpus_Generator__strings_to_csv(sents_ipa,f'{language}_sents_ipa.csv')
 
        if missing_raw:
            Corpus_Generator._Corpus_Generator__strings_to_csv([raw],f'{language}_raw.csv')
         
    
    @staticmethod
    def __strings_to_csv(strings,file_name):
        ''' Added January 12th : Creates a csv file for a list of strings (used when updating) '''
        with open(file_name, 'w',newline='',encoding='utf-8') as csvfile:
            token_writer = csv.writer(csvfile)

            for word in strings:
                try:
                    token_writer.writerow([word])
                except:
                    pass
    
    @staticmethod 
    def __read_from_csv(file_name):
        ''' Added January 13th : Creates a list of strings from a csv file (assumed in same directory, used when loading corpuses) '''
        #        sents = pd.read_csv(file_name).values.tolist()
#        sents = pd.read_csv(file_name,encoding='utf-8')
        with open(file_name,encoding='utf-8',newline='') as csvfile:
            corpusreader = csv.reader(csvfile)
            sents = [row[0] for row in corpusreader]
        return sents
#        return [sent[0] for sent in sents if type(sent[0]) == str]
 
    @staticmethod 
    def __tokenize_sents(raw,l='italian'):
        '''Jan 12th : Begun working on this helper function '''
        tokenized_sents = []
        raw_sents = sent_tokenize(raw,language=l)
    
        split_chars = r'[.,;:-?!]'
        for sent in raw_sents:

            sent = sent.lower().replace('\n',' ')
            chunks = re.split(split_chars,sent)
            for chunk in chunks:
                if ''.join(chunk.split(' ')).isalpha():
                    tokenized_sents.append(chunk)
        return tokenized_sents


class Corpus:

    def __init__(self,words,sents,raw,words_ipa,sents_ipa):
        
        self.words = words 
        self.sents = sents 
        self.raw = raw 
        self.words_ipa = words_ipa 
        self.sents_ipa = sents_ipa 

    def sample(self,n=1,ipa=False):
        ''' sample(n=1,ipa=False) 
            Returns n random tokens from the instantiated corpus
            n - number of tokens
            ipa - flag for returning IPA format of tokens
        '''
        if ipa:
            return list(np.random.choice(self.words_ipa,n))
        else: 
            return list(np.random.choice(self.words,n))

    def sample_sents(self,n=1,ipa=False):
            ''' sample_sents(n=1,ipa=False) 
                Returns n random sentances from the instantiated corpus
                n - number of sentances
                ipa - flag for returning IPA format of sentances
            '''
            if ipa:
                return list(np.random.choice(self.sents_ipa,n))
            else: 
                return list(np.random.choice(self.sents,n))


    def sample_pairs(self,n=1):
        '''sample_pairs(n)
            Returns n tuples containing randomly sampled tokens and their cooresponding ipa transcriptions
        '''
        indicies = np.random.choice(np.arange(0,len(self.words)),n)
        pairs = [(self.words[i],self.words_ipa[i]) for i in indicies]
        
        return pairs

    def sample_sent_pairs(self,n=1):
        '''sample_sent_pairs(n)
            Returns n tuples containing randomly sampled sentances and their cooresponding ipa transcriptions
        '''
        indicies = np.random.choice(np.arange(0,len(self.words)),n)
        pairs = [(self.sents[i],self.sents_ipa[i]) for i in indicies]

        return pairs

    def get_frequencies(self,ngram=1,everygram=False,ipa=True):
            '''Counts letter frequencies in the derived classes corpus''' 
            fdict = FreqDist() 
           # Jan 28th - This does not work yet 
            corp = self.words_ipa if ipa == True else self.words
            for i in range(1,ngram+1):
                if everygram or i == ngram:
                    ngram_counts = list(ngrams(pad_both_ends(corp,i),i))
                    print(ngram_counts)
                    for gram in ngram_counts:
                        fdict[gram] += 1

            return fdict

        
        
class English(Corpus):

    def __init__(self):

        words,sents,raw,words_ipa,sents_ipa = Corpus_Generator._Corpus_Generator__load_corpus(language='english')

        super().__init__(words,sents,raw,words_ipa,sents_ipa)
 

class German(Corpus):

    def __init__(self):

        words,sents,raw,words_ipa,sents_ipa = Corpus_Generator._Corpus_Generator__load_corpus(language='german')
        super().__init__(words,sents,raw,words_ipa,sents_ipa)


class Italian(Corpus):

    def __init__(self):

        words,sents,raw,words_ipa,sents_ipa = Corpus_Generator._Corpus_Generator__load_corpus(language='italian')
        super().__init__(words,sents,raw,words_ipa,sents_ipa)



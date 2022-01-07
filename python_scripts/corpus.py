#! /usr/bin/env python3

import os 
import csv
import pandas as pd
import epitran
import numpy as np
from nltk import word_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline

class Corpus:
    ''' 
    A class to represent a corpus of a given language

    Attributes:
    language : str
        Language of initialized corpus
            options: 'italian','german','english'

    '''


    _SCRIPT_PATH =  os.path.dirname(os.path.realpath(    __file__))
    _languages = ['italian','german','english']
    _language_codes = ['ita-Latn','deu-Latn','eng-Latn']
    
    def __init__(self,language='italian'):
        
        self._CORPUS_PATH =  os.path.join(os.path.dirname(os.path.realpath(    __file__)), '../Books/' + language)

        self.language = language
        self.__set_corpus()

    def sample(self,n,ipa=False):
        ''' sample(n,ipa=False) 
            Returns n random tokens from the instantiated corpus
            n - number of tokens
            ipa - flag for returning IPA format of tokens
        '''
        if ipa:
            return list(np.random.choice(self.ipa,n))
        else: 
            return list(np.random.choice(self.corpus,n))

    @staticmethod
    def sample_from_corpus(corpus,n):
        shuffled_corpus = corpus.copy()
        np.random.shuffle(shuffled_corpus)
        return shuffled_corpus[0:n]

    def sample_pairs(self,n):
        indicies = np.random.choice(np.arange(0,len(self.corpus)),n)
        pairs = [(self.corpus[i],self.ipa[i]) for i in indicies]
        
        return pairs
    def create_ngrams(self,n=1,corpus=None,for_model=True,vocab=False):
       
        if corpus == None:
            corpus = self.corpus

        train_data, train_vocab = padded_everygram_pipeline(n,corpus)

        if for_model == False:
            train_data = list(train_data)
            train_data = [list(trained_word) for trained_word in train_data]

        if vocab:
            if for_model == False:
                train_vocab = list(train_vocab)

            return train_data, train_vocab

        return train_data

        

    def ngram_frequencies(self,n=1,corpus=None,chars_to_ign=[]):
        
        assert type(chars_to_ign) == list

        if corpus == None:
            corpus = self.corpus

        e_grams = self.create_ngrams(n,corpus,for_model=False,vocab=False)
        
        ngram = []
        for trained_word in e_grams: #Merge tuples into big list
            ngram += trained_word

        ngram = [''.join(tup) for tup in ngram if len(tup) == n and '<s>' not in tup and '</s>' not in tup]
        if chars_to_ign != []:
            ngram = [tup for tup in ngram for char in chars_to_ign if char not in tup] 
        return ngram


    def __set_corpus(self):

        os.chdir(self._CORPUS_PATH)
        existing_token_file = os.path.isfile(f'{self.language}.csv') 
        existing_ipa_file = os.path.isfile(f'{self.language}_ipa.csv') 
        if existing_token_file == False or existing_ipa_file == False:
            self.__update_corpus()
        words = pd.read_csv(f'{self.language}.csv').values.tolist()
        ipa = pd.read_csv(f'{self.language}_ipa.csv').values.tolist()
        self.corpus = [word[0] for word in words if type(word[0]) == str] 
        self.ipa = [word[0] for word in ipa if type(word[0]) == str]

        if self.language == 'english':
            positive = pd.read_csv(f'positive_words.csv').values.tolist()
            positive_ipa = pd.read_csv(f'positive_ipa.csv').values.tolist()
            negative = pd.read_csv(f'negative_words.csv').values.tolist()
            negative_ipa = pd.read_csv(f'negative_ipa.csv').values.tolist()
            self.positive = [word[0] for word in positive if type(word[0]) == str]
            self.positive_ipa = [word[0] for word in positive_ipa if type(word[0]) == str]
            self.negative = [word[0] for word in negative if type(word[0]) == str]
            self.negative_ipa = [word[0] for word in negative_ipa if type(word[0]) == str]
         
        os.chdir(Corpus._SCRIPT_PATH)

    def __update_corpus(self):
        epi = epitran.Epitran(self._language_codes[self._languages.index(self.language)])

        
        books = os.listdir()
        raw = ''
        for book in books:
            if book.endswith('.txt'):
                f = open(book,'r',encoding='utf-8')
                raw += f.read().lower()
                f.close()

        tokens = word_tokenize(raw,language=self.language)
        tokens = [word for word in tokens if word.isalpha()]
        tokens = list(set(tokens))
        np.random.shuffle(tokens)
        ipa = [epi.transliterate(word) for word in tokens]

        #Write csv file of tokens
        with open(f'{self.language}.csv', 'w',newline='',encoding='utf-8') as csvfile:
            token_writer = csv.writer(csvfile,delimiter=' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)

            for word in tokens:
                try:
                    token_writer.writerow([word])
                except:
                    pass

        #Write csv file of transcriptions
        with open(f'{self.language}_ipa.csv', 'w',newline='',encoding='utf-8') as csvfile:
            token_writer = csv.writer(csvfile,delimiter=' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)

            for word in ipa:
                try:
                    token_writer.writerow([word])
                except:
                    pass

        
 
        
        self.__set_corpus()

    

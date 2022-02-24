#! /usr/bin/env python3

from SOILKit.header import *
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

    def __init__(self,language='italian'):
        
        assert language in LANGUAGES
        self.language = language
        self.__set_corpus()

    def sample(self,n=1,ipa=False):
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
    def sample_from_corpus(corpus,n=1):
        shuffled_corpus = corpus.copy()
        np.random.shuffle(shuffled_corpus)
        return shuffled_corpus[0:n]


    def sample_pairs(self,n=1):
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
                B
                train_vocab = list(train_vocab)

            return train_data, train_vocab

        return train_data

        

    def ngram_frequencies(self,n=1,corpus=None,chars_to_ign=[]):
        '''Jan 21st - This needs to be renamed to make more clear, its functionality seems to just be to list out all characters in a corpus (with duplicates)'''        
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

        os.chdir(TOKEN_PATH)
        existing_token_file = os.path.isfile(f'{self.language}.csv') 
        existing_ipa_file = os.path.isfile(f'{self.language}_ipa.csv') 
        if existing_token_file == False or existing_ipa_file == False:
            # Jan 14 - To Do: Update this to only update necessary corpuses
            self.__update_corpus()
        words = pd.read_csv(f'{self.language}.csv').values.tolist()
        ipa = pd.read_csv(f'{self.language}_ipa.csv').values.tolist()
        self.corpus = [word[0] for word in words if type(word[0]) == str] 
        self.ipa = [word[0] for word in ipa if type(word[0]) == str]

        #January 13th: Proposed update
        #        self.corpus = self._read_from_csv(f'{self.language}.csv')
        #        self.ipa = self._read_from_csv(f'{self.language}_ipa.csv')

        if self.language == 'english':
            positive = pd.read_csv(f'positive_words.csv').values.tolist()
            positive_ipa = pd.read_csv(f'positive_ipa.csv').values.tolist()
            negative = pd.read_csv(f'negative_words.csv').values.tolist()
            negative_ipa = pd.read_csv(f'negative_ipa.csv').values.tolist()
            self.positive = [word[0] for word in positive if type(word[0]) == str]
            self.positive_ipa = [word[0] for word in positive_ipa if type(word[0]) == str]
            self.negative = [word[0] for word in negative if type(word[0]) == str]
            self.negative_ipa = [word[0] for word in negative_ipa if type(word[0]) == str]

            #January 13th: Proposed Updates
        #        self.positive = self._read_from_csv('positive.csv')
        #        self.positive_ipa = self._read_from_csv('positive_ipa.csv')
        #        self.negative = self._read_from_csv('negative_words.csv')
        #        self.negative_ipa = self._read_from_csv('negative_ipa.csv')

         # January 12th: Started adding functionality for corpus sentances
#        os.chdir(os.path.join(CORPUS_PATH,self.language))
#        self.sentances = self._read_from_csv('sentances.csv')
#        self.ipa_sentances = self._read_from_csv('ipa_sentances.csv')
               
        os.chdir(SCRIPT_PATH)

    def __update_corpus(self):

        epi = epitran.Epitran(LANGUAGE_CODES[self.language])
        
        books = os.listdir()
        raw = ''
        for book in books:
            if book.endswith('.txt'):
                f = open(book,'r',encoding='utf-8')
                raw += f.read().lower()
                f.close()

        # Jan 12th : Starting to create the machinary for creating a corpus of sentances
        sents = __tokenize_sentances(raw)
        ipa_sents = [epi.translisterate(sent) for sent in sents]

        tokens = word_tokenize(raw,language=self.language)
        tokens = [word for word in tokens if word.isalpha()]
        tokens = list(set(tokens))
        np.random.shuffle(tokens)
        ipa = [epi.transliterate(word) for word in tokens]

        #Write csv file of tokens
        ''' with open(f'{self.language}.csv', 'w',newline='',encoding='utf-8') as csvfile:
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
        ''' 
        #Jan 12th : Proposed method of writing the new csv files
        self._strings_to_csv(tokens,f'{self.language}.csv')
        self._strings_to_csv(ipa,f'{self.language}_ipa.csv')
        self._strings_to_csv(sents,f'{self.language}_sents.csv')
        self._strings_to_csv(sents_ipa,f'{self.language}_sents_ipa.csv')
                
        
        self.__set_corpus()

    def _strings_to_csv(strings,file_name):
        ''' Added January 12th : Creates a csv file for a list of strings (used when updating) '''
        with open(file_name, 'w',newline='',encoding='utf-8') as csvfile:
            token_writer = csv.writer(csvfile,delimiter=' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)

            for word in strings:
                try:
                    token_writer.writerow([word])
                except:
                    pass
 
    def _read_from_csv(self,file_name):
        ''' Added January 13th : Creates a list of strings from a csv file (assumed in same directory, used when loading corpuses) '''
        sents = pd.read_csv(file_name).values.tolist()
        return [sent[0] for sent in sents if type(sent[0]) == str]
 
    
    def __tokenize_sents(raw,l='italian'):
        '''Jan 12th : Begun working on this helper function '''
        tokenized_sents = []
        raw_sents = nltk.sent_tokenize(raw,language=l)
        split_chars = r'[.,;:-]'
        for sent in raw_sents:

            sent = sent.lower().replace('\n',' ')
            chunks = re.split(split_chars,sent)
            for chunk in chunks:
                if ''.join(chunk.split(' ')).isalpha():
                    tokenized_sents.append(chunk)
        return tokenized_sents
'''            
    Jan 21st - Wanting to implement each of these subclasses, but will need to ensure that it does not distupt the current state of the Corpus class 

    class English(Corpus):

        def __init__(self):

            words,sents,raw,words_ipa,sents_ipa,raw_ipa = Corpus.__set_corpus(language='english')
            super().__init__(words,sents,raw,words_ipa,sents_ipa,raw_ipa)
     
    class German(Corpus):

        def __init__(self):

            words,sents,raw,words_ipa,sents_ipa,raw_ipa = Corpus.__set_corpus(language='german')
           super().__init__(words,sents,raw,words_ipa,sents_ipa,raw_ipa)

   
    class Italian(Corpus):

        def __init__(self):

            words,sents,raw,words_ipa,sents_ipa,raw_ipa = Corpus.__set_corpus(language='italian')
           super().__init__(words,sents,raw,words_ipa,sents_ipa,raw_ipa)


'''

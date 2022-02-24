#! /usr/bin/env python3

import nltk
import numpy as np
from nltk import word_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE 
from sklearn.linear_model import LogisticRegression


class Similarity:

    def __init__(self,corpus=None):
        '''Initializes corpus and allows for similarity metrics to be computed with respect to a corpus'''
        self.c = corpus

    def mean_edit_distance(self,word,corpus=None):
        ''' 
        For an inputted word, returns the mean edit distance with respect to the entire corpus '''
        assert type(word) == str

        if corpus == None:
            corpus = self.c.words
        
        total_distance = 0
        it = iter(corpus)
        for token in it:
            total_distance += nltk.edit_distance(word,token)

        return total_distance / len(corpus)

    def n_sim_edit_distance(self,word,n=10,corpus=None):
        ''' For an inputted word and integer n, returns n words with smallest edit distance ''' 

        if corpus == None:
            corpus = self.c.words
        
        edit_dist = nltk.FreqDist()
        it = iter(corpus)
        for token in it:
            edit_dist[token] += nltk.edit_distance(word,token)
        return edit_dist.most_common()[-1*n:][::-1]

    def n_sim_jaccard_distance(self,word,n=10,corpus=None):
        ''' For an inputted word and integer n, returns n words with smallest Jaccard distance ''' 

        if corpus == None:
                corpus = self.c.words
            
        
        edit_dist = nltk.FreqDist()
        it = iter(corpus)
        for token in it:
            edit_dist[token] += nltk.jaccard_distance(set(word),set(token))
        return edit_dist.most_common()[-1*n:][::-1]
    
   
    def mean_jaccard_distance(self,word,corpus=None):
        ''' 
        For an inputted word, returns the mean Jaccard distance with respect to the entire corpus '''
        assert type(word) == str
        
        if corpus == None:
            corpus = self.c.words

        total_distance = 0
        it = iter(corpus)
        for token in it:
            total_distance += nltk.jaccard_distance(set(word),set(token))

        return total_distance / len(corpus)

    def minimal_pairs(self,word,corpus=None):
        '''
            For an inputted word, returns all minimal pairs with respect to an inputted corpus
        '''
        assert type(word) == str
        
        if corpus == None:
            corpus = self.c.words

        min_pairs = []
        for token in corpus:
            if nltk.edit_distance(word,token) == 1:
                if len(word) == len(token) and word != token:
                    min_pairs.append(token)

        return min_pairs


    def make_everygrams(self,n,corpus=None):

        if corpus == None:
                    corpus = self.c.words_ipa

        train_data, padded_sents = padded_everygram_pipeline(n,corpus)
        train_data = [list(gram) for gram in list(train_data)]
        padded_sents = [list(token) for token in list(padded_sents)]

        return train_data,padded_sents
         


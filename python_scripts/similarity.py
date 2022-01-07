#! /usr/bin/env python3

from corpus import Corpus
import nltk
import logging
import numpy as np
from nltk import word_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE 
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
import subprocess

class Similarity:

    def __init__(self,language='italian'):
        ''' Initializes a corpus and allows for similarity metrics to be computed with respect to a corpus'''
        self.c = Corpus(language)
        if language == 'english':
            logging.getLogger().setLevel(logging.CRITICAL)
            self._set_embedding()

    def mean_edit_distance(self,word,corpus=None):
        ''' 
        For an inputted word, returns the mean edit distance with respect to the entire corpus '''
        assert type(word) == str

        if corpus == None:
            corpus = self.c.corpus
        
        total_distance = 0
        it = iter(corpus)
        for token in it:
            total_distance += nltk.edit_distance(word,token)

        return total_distance / len(corpus)

    def n_sim_edit_distance(self,word,n=10,corpus=None):
        ''' For an inputted word and integer n, returns n words with smallest edit distance ''' 

        if corpus == None:
            corpus = self.c.corpus
        
        edit_dist = nltk.FreqDist()
        it = iter(corpus)
        for token in it:
            edit_dist[token] += nltk.edit_distance(word,token)
        return edit_dist.most_common()[-1*n:][::-1]

    def n_sim_jaccard_distance(self,word,n=10,corpus=None):
        ''' For an inputted word and integer n, returns n words with smallest Jaccard distance ''' 

        if corpus == None:
            corpus = self.c.corpus
        
        
        edit_dist = nltk.FreqDist()
        it = iter(corpus)
        for token in it:
            edit_dist[token] += nltk.jaccard_distance(set(word),set(token))
        return edit_dist.most_common()[-1*n:][::-1]
    
    def n_sim_embeddings(self,word,n=10):

        return self.embedding.wv.most_similar(word,topn=n)
    
    def mean_jaccard_distance(self,word,corpus=None):
        ''' 
        For an inputted word, returns the mean Jaccard distance with respect to the entire corpus '''
        assert type(word) == str
        
        if corpus == None:
            corpus = self.c.corpus

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
            corpus = self.c.corpus

        min_pairs = []
        for token in corpus:
            if nltk.edit_distance(word,token) == 1:
                if len(word) == len(token) and word != token:
                    min_pairs.append(token)

        return min_pairs


    def make_everygrams(self,n,corpus=None):

        if corpus == None:
                    corpus = self.c.ipa

        train_data, padded_sents = padded_everygram_pipeline(n,corpus)
        train_data = [list(gram) for gram in list(train_data)]
        padded_sents = [list(token) for token in list(padded_sents)]

        return train_data,padded_sents
         
    def make_mle(self,n,corpus=None):

        if corpus == None:
            corpus = self.c.ipa

        train, vocab = padded_everygram_pipeline(n,corpus)
        lm = MLE(n)
        lm.fit(train,vocab)
        return lm 

    
    def generate_words(self,length=10,n=3,num_words=1,corpus=None,ipa=True):
        
        if corpus == None:
            if ipa:
                corpus = self.c.ipa
            else:
                corpus = self.c.corpus

        lm = self.make_mle(n,corpus)
        generated_words = []
        for i in range(num_words):
            word = '<s>'
            while '<s>' in word or '</s>' in word:
                word = ''.join(list(lm.generate(length)))
            generated_words.append(word)

        return generated_words

    def word_sentiment_test(self,length=10,n=3,num_words=5,corpus=None):
        assert self.c.language == 'english'
#        pos = list(np.random.choice(self.c.positive_ipa,m))
#        neg = list(np.random.choice(self.c.negative_ipa,m))
        pos = self.generate_words(length,n,num_words,self.c.positive_ipa)
        neg = self.generate_words(length,n,num_words,self.c.negative_ipa)
        
        mixed_words = pos + neg
        np.random.shuffle(mixed_words)
        label = [0 if word in neg else 1 for word in mixed_words]
        for i in range(len(mixed_words)):
            print(mixed_words[i])
            input()
            print(label[i])

    def _test_bash(self):
        BASH_PATH = 'C:\\Windows\\System32\\bash.exe'
#        subprocess.run([BASH_PATH])
        subprocess.run(['bash.exe','-c','ls'],stdout=subprocess.PIPE)

    def _set_embedding(self):
        self.embedding = Word2Vec(sentences=[self.c.positive,self.c.negative],vector_size=100,window=5,min_count=1,workers=4)

    class naive_sentiment_clf:
        ''' A very half baked idea of mine to have a class that embeds a corpus of sentimental words and uses the embeddings along with logistic regression to try and classify words'''
        def __init__(self,inputs,labels):
            self.emb = Word2Vec(sentences= [inputs] ,vector_size=100,window=5,min_count=1,workers=4)
            print(self.emb.wv.vectors.shape)
            self.clf = LogisticRegression().fit(self.emb.wv.vectors,labels)

        def classify(self,corpus):
            assert type(corpus) == list
            pred = []
            for word in corpus:
                self.emb.build_vocab([[word]])
                pred.append(self.clf.predict(self.emb.wv[word].reshape(1,-1)))
            return pred

    @classmethod
    def nsclf(cls,inputs,labels):
        return Similarity.naive_sentiment_clf(inputs,labels)

#! /usr/bin/env python3

'''Miscellaneous ideas and unfinished implementations '''

from gensim.models import Word2Vec
import subprocess
import logging

#Supresses console output when using gensim module
logging.getLogger().setLevel(logging.CRITICAL)

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

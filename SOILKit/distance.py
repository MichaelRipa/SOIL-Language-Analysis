#! /usr/bin/env pyton3

import numpy as np

from nltk import FreqDist


class Distance:

    #TO-DO: Catagorize the similarity metrics based on their 4 categories

    def __init__(self,d1,d2,normalize=True):


        try:
            dist_1 = FreqDist(d1)
            dist_2 = FreqDist(d2)

        except:
            print(f'Error: Type {type(d1)} or {type(d2)} not compatible with {type(FreqDist)}')

        self.labels,dist_1,dist_2 = self._set_missing_labels(list(dist_1.keys()),list(dist_2.keys()),dist_1,dist_2)

        self.P = np.array(list(dist_1.values()))
        self.Q = np.array(list(dist_2.values()))
        self.H1 = np.array(list(dist_1.values()))
        self.H2 = np.array(list(dist_2.values()))
        self.dist_1 = dist_1
        self.dist_2= dist_2

        if normalize:
            self._normalize()

        self._distance_functions = {self.manhatten: 'Manhatten (City block)',self.euclidean_dist: 'Euclidean',self.intersection: 'Intersection',self.kullback_liebler: 'Kullback-Liebler',self.bhattacharyya:'Bhattacharyya',self.matusita: 'Matusita'}
 
    def manhatten_normalized(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Manhatten/City block distance (L1 norm) is defined as:
        
        D(P,Q) = sum(| p_i - q_i |)

        '''

        return np.sum(np.abs(self.P - self.Q))

    def manhatten(self):
        ''' For two discrete histograms:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Manhatten/City block distance (L1 norm) is defined as:
        
        D(P,Q) = sum(| p_i - q_i |)

        '''

        return np.sum(np.abs(self.dist_1 - self.dist_2))

    def euclidean_dist(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Euclidean distance (L2 norm) is defined as:
        
        D(P,Q) = sqrt( sum( (p_i - q_i)^2 ) ) 

        '''

        return np.sqrt(np.sum(np.square(self.P - self.Q)))

    def intersection(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their intersection distance (or Non-Intersection) is defined
        
        D(P,Q) = n - sum(min(p_i,q_i))

        '''
        return len(self.P) - np.sum(np.min(np.array([self.P,self.Q]),axis=0))

    def kullback_liebler(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Kullback Liebler distance (or K-L distance) is defined
        
        D(P,Q) = sum(P(p_i) log( P(p_i) / P(q_i) )

        '''
 
        return np.sum(self.P * np.log( self.P / self.Q))

    def bhattacharyya(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their bhattacharyya distance is defined as:
        
        D(P,Q) = - log( sum ( sqrt( P(p_i)P(q_i) ) ) )

        '''

        return -1 * np.log( np.sum ( np.sqrt( self.P * self.Q ) ) )

    def matusita(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Matusita distance is defined as:
        
        D(P,Q) = sqrt( sum( ( sqrt(P(p_i)) - sqrt(P(q_i) ) ^2 ) )

        '''

        return np.sqrt( np.sum( np.square( np.sqrt(self.P) - np.sqrt(self.Q)) ) )



    def kolmogorov_smirnov(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their chebyshev distance is defined as:
        
        D(P,Q) = max(|p_i - q_i|) 

        '''

       
        max_index = np.argmax(np.abs(self.P - self.Q))
        return self.P_labels[max_index]

    def print_summary(self):
        ''' Jan 13th : Added the start of a function that prints all distances ''' 
        for dist in self._distance_functions.keys():
            print(f'Metric: {self._distance_functions[dist]} has distance: {dist()}')


    def _set_missing_labels(self,l_1,l_2,dist_1,dist_2,type=dict):
        ''' Jan 13th : Started this function which adds missing keys to both dictionaries '''

        shared_labels =  list(set(dist_1.keys()) | set(dist_2.keys()))

        new_dist_1 = FreqDist()
        new_dist_2 = FreqDist()
        for key in shared_labels:
            new_dist_1[key] = dist_1[key] if key in dist_1.keys() else 0
            new_dist_2[key] = dist_2[key] if key in dist_2.keys() else 0

        dist_1 = new_dist_1
        dist_2 = new_dist_2

        return shared_labels,dist_1,dist_2
        
    def _normalize(self):

        P_total = sum(self.P)
        Q_total = sum(self.Q)
        self.P = self.P / P_total
        self.Q = self.Q / Q_total

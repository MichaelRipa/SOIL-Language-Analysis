#! /usr/bin/env pyton3

import numpy as np


class Distance:

    #TO-DO: Catagorize the similarity metrics based on their 4 categories

    def __init__(self,d1,d2,normalize=True):

        assert type(d1) == dict and type(d2) == dict

        dist_1 = d1.copy()
        dist_2 = d2.copy()

        self.labels,dist_1,dist_2 = self._set_missing_labels(list(dist_1.keys()),list(dist_2.keys()),dist_1,dist_2)

        self.P = np.array(list(dist_1.values()))
        self.Q = np.array(list(dist_2.values()))

        if normalize:
            self._normalize()

        #Jan 14th - Reduced need for both pairs of labels
        #        self.P_labels = list(dist_1.keys())
        #        self.Q_labels = list(dist_2.keys())

        
        self._distance_functions = {self.hellinger: 'hellinger', self.manhatten: 'manhatten',self.euclidean_dist: 'euclidean',self.chebyshev: 'chebyshev'} #January 13th : Might use a dictionary of function pointers to print all distances

    def hellinger(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Hellinger distance is defined as:

        H(P,Q) = 1/sqrt(2) * sqrt( sum((sqrt(p_i) - sqrt(q_i))^2) )

        '''

        squares = np.square(np.sqrt(self.P) - np.sqrt(self.Q))
        return 1/ np.sqrt(2) * np.sqrt(np.sum(squares))

    def manhatten(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Manhatten distance (or City Block Distance) is defined as:
        
        D(P,Q) = sum(| p_i - q_i |)

        '''


        return np.sum(np.abs(self.P - self.Q))

    def euclidean_dist(self):

        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their Euclidean distance is defined as:
        
        D(P,Q) = sqrt( sum( (p_i - q_i)^2 ) ) 

        '''

        return np.sqrt(np.sum(np.square(self.P - self.Q)))

    def chebyshev(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their chebyshev distance is defined as:
        
        D(P,Q) = max(|p_i - q_i|) 

        '''

        return np.max(np.abs(self.P - self.Q))

    def minkowski(self,p=1):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their chebyshev distance is defined as:
        
        D(P,Q) = max(|p_i - q_i|) 

        '''


        norm_power = np.power(np.abs(self.P - self.Q),p)
        return np.power(np.sum(norm_power),1/p)


        
    def histogram_intersection(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their histogram intersection is defined as:
        
        D(P,Q) = 1 - sum( min(p_i,q_i) ) / min(|p_i|,|q_i|)

        '''

        # Jan 11 - This is returning a vector, I should check the paper to ensure the formula is correct

        component_min = np.min(np.array([self.P,self.Q]),axis=0)
        abs_component_min = np.min(np.array([np.abs(self.P),np.abs(self.Q)]),axis=0)

        return 1 - np.sum(component_min)/abs_component_min 
       

    def cosine(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their cosine distance is defined as:
        
        D(P,Q) = 1 - sum(p_i q_i)

        '''

        return 1 - np.sum(self.P * self.Q)    

    def canberra(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their chebyshev distance is defined as:
        
        D(P,Q) = max(|p_i - q_i|) 

        '''

        pass

    def chi_squared(self):
        ''' For two discrete probability distributions:

        P = (p_1,...,p_k) 
        Q = (q_1,...,q_k)

        their chebyshev distance is defined as:
        
        D(P,Q) = max(|p_i - q_i|) 

        '''

        pass

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


    def _set_missing_labels(self,l_1,l_2,dist_1,dist_2):
        ''' Jan 13th : Started this function which adds missing keys to both dictionaries '''

        shared_labels =  list(set(dist_1.keys()) | set(dist_2.keys()))

        new_dist_1 = {}
        new_dist_2 = {}
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

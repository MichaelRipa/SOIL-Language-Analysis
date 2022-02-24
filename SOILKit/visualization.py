#! /usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network
import networkx as nx
import nltk

class Visualization:
    
    def __init__(self):
        self.similarity_metrics = {'jaccard': lambda x,y: nltk.jaccard_distance(set(x),set(y)),'edit_distance': lambda x,y: nltk.edit_distance(x,y)}
    
    def test_graph(self,word,neighbours,n=10,metric='jaccard',label=True,cmap='viridis'):
        ''' Testing the graphing of words based on their similarities'''
        assert metric in self.similarity_metrics.keys()

        #Find similar neighbours
        similarity_dict = {neigh: self.similarity_metrics[metric](word,neigh) for neigh in neighbours}
        if word in similarity_dict.keys():
            similarity_dict.pop(word)
        similarity_dict = dict(sorted(similarity_dict.items(), key=lambda item: item[1]))
        n_neighbours =  list(similarity_dict.keys())[0:n]

        G = nx.Graph()
        rgba_map = plt.cm.get_cmap(cmap,10)
        for i in range(n):
            sim_word = n_neighbours[i]
            word_weight = similarity_dict[sim_word]
       #     print(sim_word,similarity_dict[sim_word])
            G.add_edge(word, sim_word , weight=word_weight) # Adds vertices

        pos = nx.spring_layout(G)  

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=[(u,v) for (u,v,d) in G.edges(data=True)], width=6)

        if label:
            nx.draw_networkx_edge_labels(G,pos,edge_labels={(word,sim_word): str(round(similarity_dict[sim_word],2)) for sim_word in n_neighbours})
        # vertice labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()


    def shared_letters(self,corpus,n=10,notebook=False,node_size = 15):
        ''' Experimental graph that connects letter nodes to word nodes '''

        assert type(corpus) == list

        subcorpus = list(np.random.choice(corpus,min(n,len(corpus))))

        G = nx.Graph()
        for word in subcorpus:
            G.add_edges_from((word,letter) for letter in list(word))
            G.nodes[word]['color'] = 'green'
            G.nodes[word]['size'] = node_size

        nt = Network(notebook=notebook)
        nt.from_nx(G)

        nt.show('graph.html')
        
    def similarity_graph(self,word,neighbours,n=10,metric='jaccard',weights=False,notebook=False):

        assert metric in self.similarity_metrics.keys()

        similarity_dict = {neigh: self.similarity_metrics[metric](word,neigh) for neigh in neighbours}
        if word in similarity_dict.keys():
            similarity_dict.pop(word)
        similarity_dict = dict(sorted(similarity_dict.items(), key=lambda item: item[1]))
        G = nx.Graph()
        G.add_nodes_from(list(similarity_dict.keys())[0:n],color='purple')
        G.add_node(word,color='blue',size=20)
        key_list = list(similarity_dict.keys())
        for i in range(n):
            G.add_edge(key_list[i],word,label=round(similarity_dict[key_list[i]],2))
#        G.add_edges_from((list(similarity_dict.keys())[i] , word) for i in range(n))
        nt = Network(notebook=notebook)
        nt.from_nx(G)

       #Currently the only way to plot in a notebook is to make the nt.show() call directly 
        if notebook:
            return nt

        nt.show('graph.html')


    def letter_frequency(self,corpus,title=None,block = False,normalize=False,colour = 'blue',alpha=1):
        '''Plots frequencies of letters for a given input.

        TO-DO: 
            - Find way to do layered plots
            - Passing in parameters for legends
            - Maybe having option to plot the n most frequent characters

        '''
        frequencies = self._get_frequencies(corpus,normalize)
            
        if hasattr(self,'ax') == False:
            self.fig,self.ax = plt.subplots()
        self.ax.bar(frequencies.keys(), frequencies.values(),color=colour,alpha=alpha)
        ylabel = 'Frequency' if normalize else 'Frequency Tally'
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel('Characters')

        if title != None:
            self.ax.set_title(title)

        plt.show(block=block)


    def plot_n_most_common(self,corpus,n=10,title=None,block = False,normalize=False,colour = 'blue',alpha=1):

        frequencies = self._get_frequencies(corpus,normalize,chars=False)
        frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1],reverse=True))
        n_most_comm = list(frequencies.keys())[0:n]
        most_comm_freqs = [frequencies[token] for token in n_most_comm]

        print(n_most_comm,most_comm_freqs,type(n_most_comm[0]))
        if hasattr(self,'ax') == False:
            self.fig,self.ax = plt.subplots()
        self.ax.bar(n_most_comm,most_comm_freqs,color=colour,alpha=alpha)
        ylabel = 'Frequency' if normalize else 'Frequency Tally'
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel('Characters')

        if title != None:
            self.ax.set_title(title)

        plt.show(block=block)




        

    
    def plot_from_dictionary(self,word_dict,html=False,notebook=False):

        G = nx.Graph()
        
        
        for cluster in word_dict.items():
            for neighbour in cluster[1]: 
                G.add_edge(cluster[0],neighbour)


#        nt = Network(notebook=notebook)
#        nt.from_nx(G)
        pos = nx.spring_layout(G, seed=63)

        colors = [i for i in range(5)]
        print(colors)
        options = {
            "node_color": "#A0CBE2",
            "edge_color": colors,
            "width": 4,
            "edge_cmap": plt.cm.Blues,
            "with_labels": True,
        }

       #Currently the only way to plot in a notebook is to make the nt.show() call directly 
        if html:
            if notebook:
                return nt

            nt.show('graph.html')

        else:
            nx.draw(G,pos,**options)


    @classmethod
    def frequency_difference(cls,corpus_1,corpus_2,title=None,normalize=False):
        ''' Plots difference in frequencies between two corpuses '''
        corpus_1_freq = cls._get_frequencies(corpus_1,normalize=normalize)
        corpus_2_freq = cls._get_frequencies(corpus_2, normalize=normalize)

        all_chars = set(corpus_1_freq.keys()) | set(corpus_2_freq.keys())
        frequency_difference = {}
        for char in all_chars:

            if char not in corpus_1_freq.keys():
                corpus_1_freq[char] = 0

            if char not in corpus_2_freq.keys():
                corpus_2_freq[char] = 0

            frequency_difference[char] = corpus_1_freq[char] - corpus_2_freq[char]  

        fig,ax = plt.subplots()
        ax.bar(corpus_1_freq.keys(), corpus_1_freq.values(),label='Actual frequency')
        ax.bar(frequency_difference.keys(), frequency_difference.values(),label='Remaining frequency')

        ax.set_ylabel('Frequency Difference')
        ax.set_xlabel('Characters')

        if title != None:
            ax.set_title(title)

        plt.legend()
        plt.show()

    @staticmethod 
    def _get_frequencies(corpus,normalize=False,chars=True):

        frequencies = {} 

        if chars: #Counting letters
            for token in corpus:
                for char in token:
                    if char in frequencies.keys():
                        frequencies[char] += 1
                    else:
                        frequencies[char] = 1

            if normalize:
                total = sum(list(frequencies.values()))
                for char in list(frequencies.keys()):
                    frequencies[char] /= total

        else: #Counting words
            for token in corpus:
                if token in frequencies.keys():
                    frequencies[token] += 1
                else:
                    frequencies[token] = 1
            if normalize:
                total = sum(list(frequencies.values()))
                for token in list(frequencies.keys()):
                    frequencies[token] /= total



        return frequencies        

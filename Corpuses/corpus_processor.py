#! /usr/bin/env python3

import os
import operator

def load_corpus(*path):
    """load_corpus(*path)
    Reads raw text from all files in a directory and returns as one concatenated string.

    Args:
    path (str): One or more paths to directories containing corpus files. Defaults to current directory

    Returns:
    raw (str): All of the file contents concatenated together
    """
    raw = ''
    path = ('./') if len(path) == 0 else path
    for current_path in path:
        for fil in os.listdir(current_path):
            f = open(os.path.join(current_path,fil),'r',encoding='utf-8')
            raw += f.read()
            f.close()
        
    return raw

def get_ngram_freqs(raw,n=1,as_percents=False):
    """get_ngram_freqs(raw,n=1,as_percents=False)
    Generates a dictionary of ngram frequencies for a provided string of text

    Args:
    raw (str): String to count ngram frequencies from
    n (int): Width of ngram segment
    as_percents (bool): If True, returns the frequencies as percents (instead of raw counts)

    Returns:
    sorted_freqs (dict): Sorted dictionary of ngram frequencies
    """
    N = len(raw)
    freqs = {}
    #Iterate through each ngram
    for i in range(0,N-n+1):
        ngram = raw[i:i+n]
        #Increment ngram tally if and only if it contains valid characters
        if ngram.isalpha():
            freqs[ngram] = 1 if ngram not in freqs.keys() else freqs[ngram] + 1

    sorted_freqs = sorted(freqs.items(), key=operator.itemgetter(1),reverse=True)
    #Convert to probability distribution (if specified)
    if as_percents:
        for ngram in sorted_freqs.keys():
            sorted_freqs[ngram] /= N

    return sorted_freqs





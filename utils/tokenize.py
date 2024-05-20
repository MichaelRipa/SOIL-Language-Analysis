#! /usr/bin/python3

from nltk import sent_tokenize

def sentence_tokenize(data : str, lang : str):
    """Simple wrapper function for NLTK `sent_tokenize()` function"""
    return sent_tokenize(data, lang)

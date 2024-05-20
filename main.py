#! /usr/bin/python3

from enum import Enum
import operator

from config.config import *
from utils.clean import clean_german, clean_italian, filter_sentences
from utils.load import load_text_files

class Language(Enum):
    GERMAN = 0
    ITALIAN = 1

def load_corpus(language : int, as_sentences=False, ipa=False, raw=False):
    """
    Load and optionally process a language corpus.

    Parameters:
    ----------
    language : int
        The language to load. Use `Language.GERMAN.value` (0) for German and `Language.ITALIAN.value` (1) for Italian.
    as_sentences : bool, optional
        If True, return the corpus as a list of sentences (default is False).
    ipa : bool, optional
        If True, transliterate the sentences to IPA (International Phonetic Alphabet). Only effective if `as_sentences` is True (default is False).
    raw : bool, optional
        If True, return the raw corpus data without cleaning (default is False).

    Returns:
    -------
    list of str
        The loaded corpus data, either as raw text, a list of cleaned sentences, or a list of IPA-transliterated sentences, depending on the parameters.

    Notes:
    -----
    - Ensure that `GERMAN_CORPUS_DIRECTORIES` and `ITALIAN_CORPUS_DIRECTORIES` are defined globally and point to the correct corpus directories.
    """

    data = None
    if language == Language.GERMAN.value:
        data = load_text_files(*GERMAN_CORPUS_DIRECTORIES, remove_newlines=False)
        if not raw:
            data = clean_german(data)
    elif language == Language.ITALIAN.value:
        data = load_text_files(*ITALIAN_CORPUS_DIRECTORIES, remove_newlines=False)
        if not raw:
            data = clean_italian(data)
    else:
        raise ValueError(f'Error: Wrong language index passed: {language}\nValid options are:\n0 - German\n1 - Italian')

    sents = None
    if not as_sentences:
        return data
    else: 
        from utils.tokenizer import sentence_tokenize # Avoid NLTK dependency
        if language == Language.GERMAN.value:
            clean = clean_german(data)
            sents = sentence_tokenize(clean, 'german')
            sents = filter_sentences(sents)
            if ipa:
                from utils.ipa import transliterate # Avoid epitran dependency
                return transliterate(sents, 'deu-Latn')
        elif language == Language.ITALIAN.value:
            clean = clean_italian(data)
            sents = sentence_tokenize(clean, 'italian')
            sents = filter_sentences(sents)
            if ipa:
                from utils.ipa import transliterate # Avoid epitran dependency
                return transliterate(sents, 'ita-Latn')
    return sents

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

if __name__ == '__main__':
    data = load_corpus(1)
    ngrams = get_ngram_freqs(data,n=1,as_percents=True)

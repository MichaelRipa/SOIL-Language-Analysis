#! /usr/bin/python3

from enum import Enum

from config.config import *
from utils.load import load_text_files
from utils.clean import clean_german, clean_italian, sentence_tokenize, filter_sentences

class Language(Enum):
    GERMAN = 0
    ITALIAN = 1

def load_corpus(language : int, as_sentences=False, ipa=False, raw=False):
    data = None
    if language == Language.GERMAN.value:
        data = load_text_files(*GERMAN_CORPUS_DIRECTORIES, remove_newlines=False)
        if raw:
            return data
        if as_sentences: 
            clean = clean_german(data)
            sents = sentence_tokenize(clean, 'german')
            sents = filter_sentences(sents)
            if ipa:
                return transliterate(sents, 'deu-Latn')
            return sents
    elif language == Language.ITALIAN.value:
        data = load_text_files(*ITALIAN_CORPUS_DIRECTORIES, remove_newlines=False)
        if raw:
            return data
        if as_sentences: 
            clean = clean_italian(data)
            sents = sentence_tokenize(clean, 'italian')
            sents = filter_sentences(sents)
            if ipa:
                return transliterate(sents, 'ita-Latn')
            return sents

    else:
        raise ValueError(f'Error: Wrong language index passed: {language}\nValid options are:\n0 - German\n1 - Italian')


if __name__ == '__main__':
    data = load_corpus(1)
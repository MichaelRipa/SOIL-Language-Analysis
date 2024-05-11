# /usr/bin/env python3

import os
import re
import epitran
from nltk import sent_tokenize

epi = epitran.Epitran('deu-Latn')

def clean_german(raw):
    """Takes raw text scraped from german newspaper pdf's and removes specific metadata"""
    clean = raw.lower()
    patterns = ['-?\n','\(cid:[0-9]*\)',' {2,10}'] # Whitespace and specific identifiers
    subs = [' ','',' ']
    for i in range(len(patterns)):
        clean = re.sub(patterns[i],subs[i],clean)
    return clean

def filter_sentences_german(sentences):
    """Filters out sentences from the german corpus which do not contain a specific amount of content desired for phonetic analysis"""
    clean_sents = []
    for sent in sentences:
        # Condition 1: The proportion of numeric characters must be lower than a pre-defined threshold
        condition_1 = len(re.findall('[0-9]',sent))/len(sent) < 0.09
        # Condition 2: The sentence must contain at least 5 words
        condition_2 = len(sents[i].split(' ')) > 4

        # Condition 3: Removes space delimited characters
        re.findall('([a-zA-Z] ){3,}',sents[i]) == []:

        # Condition 4: Removes sudoku puzzle
        condition_4 = re.findall('([0-9] ){3,}',sents[i]) == []

        # Add sentence if it passes the previous 4 conditionsf
        if condition_1 and condition_2 and condition_3 and condition_4:
            clean_sents.append(sent)

    return clean_sents

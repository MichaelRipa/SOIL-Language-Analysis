#! /usr/bin/env python3

''' header.py - Stores global variables used throughout the various language classes'''

import os


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
LANGUAGES = ['italian','german','english']
LANGUAGE_CODES = ['ita-Latn','deu-Latn','eng-Latn']
TOKEN_PATH = os.path.join(SCRIPT_PATH, 'data/tokens')
CORPUS_PATH = os.path.join(SCRIPT_PATH, 'data')

#TEST_PATH = os.path.join(SCRIPT_PATH, 'data/testing')



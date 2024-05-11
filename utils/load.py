#! /usr/bin/python3

import glob
import re

def load_text_files(*directories, remove_newlines=True):
    """Helper function which loads in raw text from all files found under a passed in iterator of directories"""
    raw_text = ''
    for directory in directories:
        for file_path in glob.glob(f'{directory}/*.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_text += re.sub('\n',' ',file.read()) if remove_newlines else file.read()
    return raw_text 

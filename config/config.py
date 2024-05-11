#! /usr/bin/python3
import os
from pathlib import Path

_file_dir = Path(os.path.realpath(__file__))
repo_dir = _file_dir.parent.parent.absolute()

GERMAN_CORPUS_DIRECTORIES = [
    os.path.join(
        repo_dir,
        'corpus',
        'german',
        year,
        'raw'
    ) 
    for year in os.listdir(
        os.path.join(
            repo_dir
            ,'corpus',
            'german'
        )
    )
]

ITALIAN_CORPUS_DIRECTORIES = [
    os.path.join(
        repo_dir,
        'corpus',
        'italian',
        year,
        'raw'
    ) 
    for year in os.listdir(
        os.path.join(
            repo_dir
            ,'corpus',
            'italian'
        )
    )
]

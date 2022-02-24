#! /usr/bin/env python3

from corpus import Corpus
import random
from ipa import ipa

class Generate(Corpus):

    def __init__(self):
        pass

    def generate_suffix(self,nucleus=None,onset=None,coda=None):

        if nucleus == None:
            nucleus = random.choice(ipa.vowels)

        if onset == None:
            onset = random_onset_length(nucleus)


        if coda == None:
            coda = random_coda_length(nucleus)


        suffix = nucleus

        generated_coda = ''
        generated_onset = ''

        While True:
            generated_coda = generate_word(n=coda,start=nucleus)
            if _no_vowels(generated_coda):
                break

        While True:
            generated_onset = generate_word(n=onset,end=nucleus)
            if _no_vowels(generated_onset):
                break

        return generated_onset + nucleus + generated_coda

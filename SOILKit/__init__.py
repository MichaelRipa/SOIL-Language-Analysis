#! /usr/bin/env python3

class _load_globals:

    def __init__(self):
        self.vowels = ['ɪ','i','æ','e','ə','ê','ü','é','ë','î','á','ö','ʊ','a','u','o','ɔ','ʌ','ɑ','ɛ']
        self.fricatives = ['v', 'z', 'ð', 'f', 'θ', 'ʃ', 's', 'ʒ', 'h', 'j']
        self.nasels = ['n', 'm', 'ŋ', 'w', 'ɹ', 'l']
        self.stops = ['d', 'ɡ', 'k', 'p', 't', 'b']
        self.misc = ['͡', '̩']



ipa = _load_globals()

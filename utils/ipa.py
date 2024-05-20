#! /usr/bin/python3

import epitran


def transliterate(sents: str, lang_code: str):
    """Simple wrapper around the `epitran.Epitran()` class for converting alpha numberic text to IPA."""
    epi = epitran.Epitran(lang_code)
    return [epi.transliterate(s) for s in sents]

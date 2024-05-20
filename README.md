# SOIL-Language-Analysis

This repository contains German and Italian corpora collected from newspaper data. The corpora are intended for linguistic analysis, particularly phoneme frequency analysis. The codebase provides functionality for loading and processing the corpora with optional preprocessing steps.

## Getting Started

### Prerequisites
- Python 3.x

### Installation

Clone the repository:

`git clone https://github.com/yourusername/SOIL-Language-Analysis.git && cd SOIL-Language-Analysis`

### Usage

The main functionality is provided in main.py. You can load and process the corpora using the load_corpus function and analyze n-gram frequencies using the get_ngram_freqs function.

#### Loading a Corpus

```
from main import load_corpus, Language

# Load German corpus
german_data = load_corpus(Language.GERMAN.value)

# Load Italian corpus
italian_data = load_corpus(Language.ITALIAN.value)
```

### Analyzing N-gram Frequencies
```
from main import get_ngram_freqs

# Get unigram frequencies for Italian corpus
italian_data = load_corpus(Language.ITALIAN.value, raw=True)
italian_ngrams = get_ngram_freqs(italian_data, n=1, as_percents=True)
```

### Optional Preprocessing

- `as_sentences`: If `True`, return the corpus as a list of sentences.
- `ipa`: If `True`, transliterate the sentences to IPA (International Phonetic Alphabet). Only effective if `as_sentences` is `True`.
`raw`: If `True`, return the raw corpus data without cleaning.

Example:

```
# Load German corpus as sentences and transliterate to IPA
german_sentences_ipa = load_corpus(Language.GERMAN.value, as_sentences=True, ipa=True)
```

## Avoiding Dependencies
The corpus can be loaded without any dependencies if not doing sentence tokenization or IPA conversion.

## Contributing
Contributions are welcome. Please open an issue or submit a pull request for any changes.

## License
This project is licensed under the MIT License.



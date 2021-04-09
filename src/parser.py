import os
import string
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk import pos_tag
from inverted_index import *

# Parse all files in the given directory

directory = '../dataset/ShortStories/'
stop_words_filename = "../dataset/Stopword-List.txt"

parsed_docs = []
removal_words = set()

index = InvertedIndex()
pos_index = PositionalInvertedIndex()


def parse():

    # The parse function runs through all the documents in the corpus
    # and parse it by cleaning, replacing, removing stop-words, and
    # tokenizing them.

    global directory

    # porter = PorterStemmer()
    porter = SnowballStemmer("english")
    for docId in range(1, 51):
        doc_name = directory + "{}.txt".format(docId)
        doc = open(doc_name, 'r')
        doc_stream = doc.read()
        doc_stream = re.sub(r'\b-\b', '', doc_stream.lower())
        doc_stream = re.sub(r'[^a-z1-9]+', ' ', doc_stream.lower())

        tokens = tokenize(doc_stream)
        terms = process(tokens)

        for (term, pos) in terms:

            term = porter.stem(term)

            # building a simple and a positional index

            index.add_term(term, docId)
            pos_index.add_term(term, docId, pos)

        doc.close()

    index.write_index_to_disk()
    pos_index.write_index_to_disk()


def process(tokens):
    # Removes the removal words such as stop words, and
    # assigning positions to tokens.

    global removal_words

    if len(removal_words) == 0:
        load_removal_words()

    revised_tokens = []

    pos = 0
    i = 0
    while pos < len(tokens):
        is_possessive = 0

        # This section does pos tagging to know if "'s" shows possession
        # or it shows contraction, as I am assigning positions to stop words even
        # to stop words which appear as contraction.

        if pos > 0 and tokens[pos] == 's' and 'NN' not in nltk.pos_tag([tokens[pos - 1]])[0][1]:
            tokens[pos] = 'is'

        if pos > 0 and tokens[pos] == 's' and 'NN' in nltk.pos_tag([tokens[pos - 1]])[0][1]:
            is_possessive = 1
            i -= 1

        i += 1

        if is_possessive == 0 and tokens[pos] not in removal_words:
            revised_tokens.append((tokens[pos], i))

        pos += 1

    # returns processed tokens
    return revised_tokens


def tokenize(stream):
    tokens = nltk.word_tokenize(stream)
    return tokens


def load_removal_words():
    # loads the stopwords from disk

    global removal_words

    with open(stop_words_filename, 'r') as stop_file:
        stop_file_content = stop_file.readlines()

        for word in stop_file_content:
            word = word[:-1].rstrip()
            if word != "":
                removal_words.add(word)


def test():

    # *** Test code ***

    parse()
    print(index.dictionary)

    word = "beard"

    ps = PorterStemmer()
    w = ps.stem(word)
    print(w)


if __name__ == "__main__":
    test()

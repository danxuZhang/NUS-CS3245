#!/usr/bin/python3
import os
import pickle
import re
import nltk
import sys
import getopt


from sortedlist import SortedList
from dictionary import Token

sys.setrecursionlimit(2000)
dictionary = []  # list of tokens
postings = []  # list of postings (sorted list)
STEMMER = nltk.stem.porter.PorterStemmer()
TEST_SIZE = 500


def generate_word_tokens(file_name: str) -> set:
    with open(file_name) as file:
        content = file.read()
        sent_tokens = nltk.sent_tokenize(content)
        word_tokens = set()
        for sent in sent_tokens:
            words = nltk.word_tokenize(sent)
            for word in words:
                word_tokens.add(word.lower())
        return word_tokens


def stem(tokens: set) -> set:
    stemmed_tokens = set()
    for token in tokens:
        stemmed_tokens.add(STEMMER.stem(token))
    return stemmed_tokens


def indexing(doc_id: int, word_tokens: set, dictionary, postings):
    for word_token in word_tokens:
        token = None
        for dict_token in dictionary:
            if dict_token.get_term() == word_token:
                token = dict_token
                break
        if token is None:
            token = Token(word_token, len(postings))
            posting = SortedList()
            posting.add_val(doc_id)
            postings.append(posting)
            dictionary.append(token)
        else:
            id = token.get_posting_id()
            posting = postings[id]
            posting.add_val(doc_id)


def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")


def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below
    dir_list = os.listdir(in_dir)
    cnt = 0
    for file_name in dir_list:
        if cnt == TEST_SIZE:
            break
        cnt += 1
        doc_id = file_name
        tokens = stem(generate_word_tokens(in_dir + "/" + file_name))
        indexing(int(doc_id), tokens, dictionary, postings)

    with open(out_dict, "wb") as f:
        print("Written to dictionary: ", len(dictionary))
        pickle.dump(dictionary, f)
    with open(out_postings, "wb") as f:
        print("Written to postings: ", len(postings))
        pickle.dump(postings, f)

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        input_directory = a
    elif o == '-d':  # dictionary file
        output_file_dictionary = a
    elif o == '-p':  # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)

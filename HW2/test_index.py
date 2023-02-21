import os
import nltk
import pickle

import sortedlist

STEMMER = nltk.stem.PorterStemmer()
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


def load_index_data() -> (list, list):
    with open("dictionary.txt", "rb") as f:
        dictionary = pickle.load(f)
    with open("postings.txt", "rb") as f:
        postings = pickle.load(f)
    return dictionary, postings


def prepare_correct_data(file_path) -> (dict):
    term_doc = {}
    dir_list = os.listdir(file_path)
    cnt = 0
    for file_name in dir_list:
        if cnt == TEST_SIZE:
            break
        cnt += 1
        tokens = generate_word_tokens(file_path + "/" + file_name)
        tokens = stem(tokens)
        for token in tokens:
            if token not in term_doc.keys():
                term_doc[token] = set()
            term_doc[token].add(int(file_name))
    return term_doc


def test(dictionary: list, postings: list, term_doc: dict) -> float:
    cnt_correct = 0
    cnt_all = 0
    for token in dictionary:
        assert token.get_term() in term_doc.keys()
        ans_set = term_doc[token.get_term()]
        posting = postings[token.get_posting_id()]
        for node in posting:
            cnt_all += 1
            if node.val in ans_set:
                cnt_correct += 1
            else:
                print(f"Test failed for term {token.get_term}")
    return cnt_correct / cnt_all




if __name__ == "__main__":
    dictionary, postings = load_index_data()
    term_doc = prepare_correct_data("/Users/tim/nltk_data/corpora/reuters/training")

    print("Precision: ", str(test(dictionary, postings, term_doc)))

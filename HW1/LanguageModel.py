import re
import math
import string
import statistics
from collections import defaultdict


class LanguageModel:
    """A class containing language models for different languages and can be trained to perform language matching.

    Attributes:
        _vocab: a set containing all tokens appeared in the model.
        _langs: a dictionary with language label as key and a dictionary storing the frequency of tokens as value.
        _n: n-gram model used in the language model, by default n = 4.
    """
    def __init__(self, n: int = 4) -> None:
        """Constructor for the Language Model.

        Args:
            n: n-gram model.
        """
        self._vocab = set()
        self._langs = {}
        self._n = n

    def _tokenize(self, text: string) -> list:
        # remove punctuations and numbers
        new_text = text.translate(str.maketrans('', '', string.punctuation + string.digits))
        # remove redundant spaces
        new_text = re.sub(' +', ' ', new_text)

        # create token list
        tokens = []
        for i in range(0, len(new_text) - self._n + 1):
            sub_str = new_text.lower()[i:i + self._n]
            tokens.append(sub_str)
        return tokens

    def _smoothing(self, label: string, tokens: list, n: int = 1) -> defaultdict:
        smoothed = self._langs[label].copy()
        for token in set(self._langs[label].values()).union(tokens):
            smoothed[token] += n
        return smoothed

    def _cal_log_prob(self, label: string, tokens: list) -> float:
        # perform smoothing
        smoothed_dict = self._smoothing(label, tokens)

        # normalize dictionary by calculating the probabilities
        n = sum(smoothed_dict.values())  # total number
        probabilities = defaultdict(float)
        for token in smoothed_dict:
            probabilities[token] += smoothed_dict[token] / n

        # calculate probabilities in log-10
        prob = 0.0
        for token in tokens:
            prob += math.log10(probabilities[token])
        return prob

    def getVocab(self) -> set:
        return self._vocab

    def getN(self) -> int:
        return self._n

    def train(self, label: string, text: string) -> None:
        """Training the language model from the input text.

        Args:
            label: the language that the text belong to.
            text: content of the training data.
        """
        # if the language is not in the dictionary
        if label not in self._langs.keys():
            self._langs[label] = defaultdict(int)

        # convert text to tokens and add to the corresponding language dictionary,
        # also add to the vocabulary
        tokens = self._tokenize(text)
        for token in tokens:
            self._vocab.add(token)
            self._langs[label][token] += 1

    def predict(self, text: string) -> string:
        """Predicts the language that a string belong to.

        Args:
            text: input text to perform language matching.

        Returns: label of the predicted language, or "other" if the input string doesn't belong to any language.
        """
        # tokenize the input string
        tokens = self._tokenize(text)

        # count the number of tokens that are not in the vocabulary
        cnt = 0
        size = len(tokens)

        # ignore token that has never appeared in the vocabulary
        for token in tokens:
            if token not in self._vocab:
                tokens.remove(token)
                cnt += 1

        # categorize text as "other" if there are too many tokens not in the vocabulary
        # print("Never appeared token percentage: {:2.2%}".format(cnt/size))
        if cnt/size > 0.4:
            return "other"

        # calculate probabilities for the input text in each language
        probs = {}

        for language in self._langs.keys():
            probs[language] = self._cal_log_prob(language, tokens)

        # categorize the text to "other" if the std is less than 1
        # print("Standard deviation: {:.4}".format(np.std(list(probs.values()))))
        if statistics.stdev(list(probs.values())) < 1:
            return "other"

        # find the language that has the highest probability
        return max(probs, key=probs.get)
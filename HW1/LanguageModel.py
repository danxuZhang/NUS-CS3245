import re
import string
from math import log10
from collections import defaultdict


class LanguageModel:
    """ Langauge Model for processing Language Detection

    Attributes:
        _name: name of the model.
        _occurs: a default dictionary counting the occurrences of each token.
        _n: n-grams, default is 4.
    """

    def __init__(self, name: str, n: int = 4) -> None:
        """Constructor of the language model and initialize its name.
        Args:
            name: name of the language model (e.g. English, Malay)
            n: n-gram model, by default it's a 4-gram character model
        """
        self._name = name
        self._occurs = defaultdict(int)
        self._n = n

    def get_name(self) -> str:
        return self._name

    def train(self, text: string) -> None:
        """Convert text to tokens and then add tokens to the model
        Args:
            text: text to be converted and added to the model
        """
        tokens = self._tokenize(text)
        self._add_tokens(tokens)

    def cal_log_prob(self, text: str) -> float:
        """Calculate probability for a given text in a language model in log 10
        First perform smoothing, default add 1 smoothing, then normalize the frequency distribution with probabilities.
        Calculation of probabilities is done in log form, otherwise the number will be too small.
        Args:
            text: a string to be calculated
        Returns:
            calculated probabilities in log 10
        """
        # convert the text to tokens
        tokens = self._tokenize(text)

        # perform smoothing
        smoothed_dict = self._smoothing(tokens)

        # normalize dictionary by calculating the probabilities
        n = sum(smoothed_dict.values())  # total number
        probabilities = defaultdict(float)
        for token in smoothed_dict:
            probabilities[token] += smoothed_dict[token] / n

        # calculate probabilities in log-10
        prob = 0.0
        for token in tokens:
            prob += log10(probabilities[token])
        return prob

    def _tokenize(self, text: str) -> list:
        """Convert an input string to a list of tokens.

        Token is a string of n characters including spaces, by default it's 4 characters(4-gram)

        Args:
            text: input string to be tokenized
        Returns:
            A list containing tokens split from the input string
        """
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

    def _add_tokens(self, tokens: list) -> None:
        """Add tokens to the dictionary
        Args:
            tokens: a list of tokens to be added.
        """
        for token in tokens:
            self._occurs[token] += 1

    def _smoothing(self, tokens: list = None, n: int = 1) -> defaultdict:
        """Smoothing, default add one smoothing"""
        smoothed = self._occurs.copy()
        for token in set(self._occurs.values()).union(tokens):
            smoothed[token] += n
        return smoothed


def test():
    lm1 = LanguageModel("Test1")
    lm1.train("Hello world! 123 hello yes Yes yes.")
    lm2 = LanguageModel("Test2")
    lm2.train("Bye bye! No no no.")
    print(lm1._occurs)
    print(lm1.cal_log_prob("hello world yes yes"))
    print(lm2.cal_log_prob("hello world yes yes"))
    print(lm1.cal_log_prob("bye bye world no no no"))
    print(lm2.cal_log_prob("bye bye world no no no"))


test()

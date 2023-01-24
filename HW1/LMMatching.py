#!/usr/bin/python3

import numpy as np
from LanguageModel import LanguageModel


class LMMatching:
    def __init__(self) -> None:
        # a dictionary storing all the language models
        # key: label e.g. English, value: an instance of Language Model
        self._lms = {}

    def train(self, label=str, text=str) -> None:
        """ Add a training text with its label

        Args:
            label: label of the language (e.g. English, Malay)
            text: actual content of the training data
        """
        if label not in self._lms.keys():
            self._lms[label] = LanguageModel(str(label))
        self._lms[label].train(text)

    def predict(self, input_text=str) -> str:
        """ Find a language model that the input text most likely belong to.

        Args:
            input_text: input text to predict.

        Returns:
            label of the language model that the input text mostly likely belong to,
                return 'other' if all the models give similar results.

        """
        # probs is a dictionary containing calculated probability from each language model
        # key: label of the language model, value: log-10 of the probability
        probs = {}
        for lm in self._lms.values():
            probs[lm.get_name()] = lm.cal_log_prob(input_text)

        print(probs, np.std(list(probs.values())))
        # if there is no model have a stand-out answer, i.e. stand deviation of the output probability is less than 1
        # return other
        if np.std(list(probs.values())) < 1:
            return "other"

        return max(probs, key=probs.get)

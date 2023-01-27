#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import getopt

from LanguageModel import LanguageModel


def build_LM(in_file: str) -> LanguageModel:
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")

    # Pls implement your code below

    lm = LanguageModel()

    line_cnt = 0
    with open(in_file) as f:
        for line in f:
            # exact label and actual content from the input line
            (lang, text) = line.strip("\n").split(" ", 1)
            # train the language model
            lm.train(lang, text)
            line_cnt += 1

    print("langauge model built from {:} lines of training data.".format(line_cnt))
    return lm


def test_LM(in_file: str, out_file: str, LM: LanguageModel) -> None:
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")

    # Pls implement your code below

    with open(in_file) as in_f, open(out_file, "w") as out_f:
        for line in in_f:
            res = LM.predict(line)
            # write result to the output file
            out_f.write(res + " " + line)

    print("langauge models test finished, result has been written to " + out_file + ".")


def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b is None or input_file_t is None or output_file is None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)

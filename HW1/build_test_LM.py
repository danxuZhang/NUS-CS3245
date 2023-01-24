#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import getopt

from LMMatching import LMMatching


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")
    # This is an empty method
    # Pls implement your code below

    lm_matching = LMMatching()

    with open(in_file) as f:
        for line in f:
            # exact label and actual content from the input line
            (lang, text) = line.strip("\n").split(" ", 1)
            lm_matching.train(lang, text)

    print("langauge model built!")
    return lm_matching


def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code below

    with open(in_file) as in_f, open(out_file, "w") as out_f:
        for line in in_f:
            res = LM.predict(line)
            # write result to the output file
            out_f.write(res + " " + line)

    print("langauge models test finished!")
    # run evaluation module
    os.system("python3 eval.py input.predict.txt input.correct.txt")


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
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)

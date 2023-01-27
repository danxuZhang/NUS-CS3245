This is the README file for A0268977Y's submission
Email: e1107334@u.nus.edu

== Python Version ==

I'm using Python Version 3.8.15 for this assignment.

== General Notes about this assignment ==

This is a program that performs language matching with character-based 4-gram language model.

To build the language model, the program constructs a dictionary for each language to record the frequency of tokens
from the training text, and creates a set to record the vocabulary, i.e. all tokens that appeared in the model.

To perform classification, the program first ignores tokens that have never appeared in the vocabulary. Then it performs
add one smoothing and normalizes the dictionary by dividing the frequency of a token by the total frequency. After these
it calculates the probability of the input text for each language. To avoid getting very small numbers, the program
calculates by adding log-10 of the probabilities. The language that has the highest probabilities are selected.

To classify input text that does not belong to any language in the language model, the program first calculate the
percentage of tokens that have never appeared in the vocabulary. If there are too many never-appeared tokens, the text
will be classified as "others". Also, after calculating the probabilities of the text given each language, if the
probabilities are too similar (i.e. the standard deviation of the probabilities is too small), the input text will be
classified as "other" as well.

== Files included with this submission ==

* README.txt: This file, describes the content of the project.
* LanguageModel.py: Defines and implements the LanguageModel class used for training and predicting language matching.
* build_test_LM.py: Builds and tests the language model using the LanguageModel class.
* eval.py: Skeleton file, evaluates the prediction with correct result.
* test.sh: a shell script for testing the model
* input.train.txt: Skeleton file, the input file for you to build LMs.
* input.test.txt: Skeleton file, the input file for testing the LMs.
* input.predict.txt: Generated results from input in input.test.txt.
* input.correct.txt: Skeleton file, contains the correct labels for the input in input.test.txt.
* CS3245-hw-1-check.sh: Skeleton file.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0268977Y, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

* Textbook Introduction to Information Retrieval and Week 1 Slides.

* Python documentation for default dictionary.
https://docs.python.org/3/library/collections.html#defaultdict-objects

* Question @27 on the forum for classifying 'other' by using percentage of words appeared in the vocabulary.
(classify 'other' by using standard deviation of the probabilities is my original idea)
https://piazza.com/class/la0p9ydharl54v/post/27

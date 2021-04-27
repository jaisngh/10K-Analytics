from nltk import SyllableTokenizer, sent_tokenize
import pandas as pd
import string
import re
import os
import warnings
warnings.filterwarnings("ignore")

class Section:
    def __init__(self, raw_text, master, stop_words):
        self.master_dictionary = master
        self.stop_words = stop_words
        text = Section.tokenize(raw_text)
        self.variables = {}
        self.sentimentAnalysis(text)
        self.complexCount(text)
        self.readabilityAnalysis(raw_text)

    def sentimentAnalysis(self, text):
        self.cleaned_text = self.clean(text)
        self.positive, self.negative, self.polarity = 0, 0, 0
        self.wordCount = 0
        self.positive_dictionary, self.negative_dictionary = {}, {}
        for w in self.cleaned_text:
            if w not in string.punctuation:
                self.wordCount += 1
            if w.upper() in self.master_dictionary.index:
                if self.master_dictionary.at[w.upper(), 'Positive'] != 0:
                    self.positive_dictionary.update({w: 1})
                    self.positive += 1
                elif self.master_dictionary.at[w.upper(), "Negative"] != 0:
                    self.negative_dictionary.update({w: 1})
                    self.negative += 1

        self.polarity = (self.positive - self.negative) / ((self.positive + self.negative) + 0.000001)
        self.variables.update({"Word Count": self.wordCount, "Negative Score": self.negative, "Positive Score": self.positive, "Polarity Score": self.polarity})

    @staticmethod
    def tokenize(txt):
        tokens = re.split(r'\W+', txt)
        return tokens

    def clean(self, text):
        cleaned_tokens = []
        for w in text:
            if w.upper() not in self.stop_words:
                cleaned_tokens.append(w)
        return cleaned_tokens

    def readabilityAnalysis(self, text):
        sentences = len(sent_tokenize(text))
        self.avgSentenceLength = self.wordCount / sentences
        self.complexPercent = self.complexWordCount / self.wordCount
        self.fogIndex = 0.4 * (self.avgSentenceLength + self.complexPercent)
        
        self.variables.update({"Average Sentence Length": self.avgSentenceLength, "Percent of Complex Words": self.complexPercent, "Fog Index": self.fogIndex})

    def complexCount(self, text):
        tk = SyllableTokenizer()
        self.complexWordCount = 0
        totalWords, totalCharacters = 0, 0
        for i in text:
            totalWords += 1
            totalCharacters += len(i)
            if len(tk.tokenize(i)) > 2:
                self.complexWordCount += 1
        self.variables.update({"Complex Word Count": self.complexWordCount})

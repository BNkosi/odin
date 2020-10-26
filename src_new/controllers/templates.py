"""
Authors: Bulelani Nkosi, Caryn Pialat
Created: 23/10/2020
Classes that control chatbot message templates
"""

# Imports

import requests
import json
import re
from time import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from nltk import ngrams
import pandas as pd
from sklearn.neighbors import NearestNeighbors

class QuestionAnswering:
    """
    Guides new users through EDSA website
    Answers the users questions and stores FAQs
    """
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel, question):
        self.channel = channel
        self.question = question
        self.username = "Hera"
        self.icon_emoji = ":page_facing_up:"
        self.timestamp = ""
        # Add disambiguation stuffies here
        self.faq = set([
            "What are the fundamental values at explore?",
             "What are the payment plans",
             "Which course is best for me?",
             "Which course should I take?",
             "When is the next Advanced Python course?", 
             "When is the next coding challenge?",
             "How much does the Data Science course cost?",
             "How much is the Advanced Python course?",
             "How much is the Data Analysis course?"
            ])
        self.training_questions = pd.Series(list(self.faq))
        self.correct_question = self._spell_check(self.question)
        self.vectorizer = TfidfVectorizer(min_df=1, analyzer='char', ngram_range=(1,5), lowercase=True)
        self.tfidf = self.vectorizer.fit_transform(self.training_questions)
        self.nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(self.tfidf)
        self.n_sim_questions: int = 3

    DIVIDER_BLOCK = {"type": "divider"}

    def get_answer_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                *self._get_answer_block(), 
                self.DIVIDER_BLOCK,
                *self._get_sim_questions()
            ],
        }

    def _get_sim_questions(self):
        _, indices = self.GetNearestN(query=[self.question], n=self.n_sim_questions)
        results = self.training_questions[indices[0]].tolist()
        text = (
            "Did you mean:\n"
            f"{results[0]}\n"                                   # Turn this block (text = (XXXXX)) into slack radio buttons
            f"{results[1]}\n"
            f"{results[2]}\n"
            "None of the above"
        )
        information = ("None")
        return self._get_task_block(text, information)

    # @staticmethod
    def _get_answer_block(self):
        # Answers
        response = self.request_answer(self.question)
        try:
            answer = response['results'][0]['answers'][0]['answer']
            title = response['results'][0]['answers'][0]['meta']['name']
            conf = response['results'][0]['answers'][0]['probability']
            context = response['results'][0]['answers'][0]['context']
            # print(response)
            text = (
                f"*Question:*\n\n{self.correct_question}\n\n"
                f"*Answer:*\n\n{answer}.\n\n"
                f"*Confidence*:\t{int(conf*100)}%\n\n"
                # f"Title: {title}\n"
                f"*Extract*:\n\n{context}"
            )
            information = (
                ":information_source: *<https://explore-datascience.net|"
                f"{title}>*"
            )
            return self._get_task_block(text, information)
        except:
            return self._get_no_answer_block()
        
    # @staticmethod    
    def GetNearestN(self, query, n):
        queryTFIDF_ = self.vectorizer.transform(query)
        distances, indices = self.nbrs.kneighbors(queryTFIDF_, n_neighbors=n)
        return distances, indices
   
    @staticmethod
    def request_answer(question):
        url = 'http://127.0.0.1:8000/models/1/doc-qa'
        pay = {"questions": [re.sub("'", "",question)], "top_k_retriever": 1, "top_k_reader": 1}
        # data = '{"questions": ["What are the fundamental values at explore?"]}'
        # data = str({"questions": [question]})
        # print(url+ " " +data)
        response = requests.post(url, json.dumps(pay)).json()
        print(response)
        return response

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]

    @staticmethod
    def _get_no_answer_block():
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": "I don't have an answer for that. Click yes if you would like to be notified when an answer is available."}},
        ]

    @staticmethod
    def _spell_check(question):
        return TextBlob(question).correct()

# # Replace contractions with full form of the words
# contractions = {
# "ain't": "am not / are not",
# "aren't": "are not",
# "can't": "cannot",
# "can't've": "cannot have",
# "'cause": "because",
# "could've": "could have",
# "couldn't": "could not",
# "couldn't've": "could not have",
# "didn't": "did not",
# "doesn't": "does not",
# "don't": "do not",
# "hadn't": "had not",
# "hadn't've": "had not have",
# "hasn't": "has not",
# "haven't": "have not",
# "he'd": "he had / he would",
# "he'd've": "he would have",
# "he'll": "he will",
# "he'll've": "he will have",
# "he's": "he has / he is",
# "how'd": "how did",
# "how'd'y": "how do you",
# "how'll": "how will",
# "how's": "how has / how is",
# "i'd": "I had / I would",
# "i'd've": "I would have",
# "i'll": "I will",
# "i'll've": "I will have",
# "i'm": "I am",
# "i've": "I have",
# "isn't": "is not",
# "it'd": "it had / it would",
# "it'd've": "it would have",
# "it'll": "it will",
# "it'll've": "it will have",
# "it's": "it has / it is",
# "let's": "let us",
# "ma'am": "madam",
# "mayn't": "may not",
# "might've": "might have",
# "mightn't": "might not",
# "mightn't've": "might not have",
# "must've": "must have",
# "mustn't": "must not",
# "mustn't've": "must not have",
# "needn't": "need not",
# "needn't've": "need not have",
# "o'clock": "of the clock",
# "oughtn't": "ought not",
# "oughtn't've": "ought not have",
# "shan't": "shall not",
# "sha'n't": "shall not",
# "shan't've": "shall not have",
# "she'd": "she had / she would",
# "she'd've": "she would have",
# "she'll": "she will",
# "she'll've": "she will have",
# "she's": "she has / she is",
# "should've": "should have",
# "shouldn't": "should not",
# "shouldn't've": "should not have",
# "so've": "so have",
# "so's": "so has",
# "that'd": "that would / that had",
# "that'd've": "that would have",
# "that's": "that has / that is",
# "there'd": "there had / there would",
# "there'd've": "there would have",
# "there's": "there has / there is",
# "they'd": "they had / they would",
# "they'd've": "they would have",
# "they'll": "they will",
# "they'll've": "they will have",
# "they're": "they are",
# "they've": "they have",
# "to've": "to have",
# "wasn't": "was not",
# "we'd": "we had / we would",
# "we'd've": "we would have",
# "we'll": "we will",
# "we'll've": "we will have",
# "we're": "we are",
# "we've": "we have",
# "weren't": "were not",
# "what'll": "what will",
# "what'll've": "what will have",
# "what're": "what are",
# "what's": "what has / what is",
# "what've": "what have",
# "when's": "when has / when is",
# "when've": "when have",
# "where'd": "where did",
# "where's": "where has / where is",
# "where've": "where have",
# "who'll": "who will",
# "who'll've": "who will have",
# "who's": "who has / who is",
# "who've": "who have",
# "why's": "why has / why is",
# "why've": "why have",
# "will've": "will have",
# "won't": "will not",
# "won't've": "will not have",
# "would've": "would have",
# "wouldn't": "would not",
# "wouldn't've": "would not have",
# "y'all": "you all",
# "y'all'd": "you all would",
# "y'all'd've": "you all would have",
# "y'all're": "you all are",
# "y'all've": "you all have",
# "you'd": "you had / you would",
# "you'd've": "you would have",
# "you'll": "you will",
# "you'll've": "you will have",
# "you're": "you are",
# "you've": "you have"
# }

# # Replace contractions with full length words
# df['msg_clean'] = df['msg_clean'].apply(lambda x: [word.replace(word, contractions[word.lower()]) if word.lower() in contractions else word for word in x])


### TEST: Radio button
def _get_sim_questions(self):
        distances, indices = self.GetNearestN(query=[self.question], n=self.n_sim_questions)
        results = self.training_questions[indices[0]].tolist()
        text = (
            "Did you mean:\n"
            f"{results[0]}\n"
            f"{results[1]}\n"
            f"{results[2]}\n"
            "None of the above"
        )
        information = ("None")
        return self._get_task_block(text, information)
"""
Authors: Bulelani Nkosi, Cary Pialat
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
from nltk import ngrams
import pandas as pd
from sklearn.neighbors import NearestNeighbors

class QuestionAnswering:
    """
    Guides new users through EDSA website
    """
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel, question):
        self.channel = channel
        self.question = question
        self.username = "Zeus"
        self.icon_emoji = ":zap:"
        self.timestamp = ""
        # Add disambiguation stuffies here
        self.faq = set(
            [
                "What are the fundamental values at explore?"
            ]
        )

    def get_answer_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                *self._get_answer_block(),
                self.DIVIDER_BLOCK,
                # *self._get_sim_questions()
            ],
        }

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
            # f"*Question:*\n\n{self.question}\n\n"
            f"*Answer:*\n\n{answer}.\n\n"
            f"*Confidence*:\t{int(conf*100)}%\n\n"
            # f"Title: {title}\n"
            # f"*Extract*:\n\n{context}"
            )
            information = (
                ":information_source: *<https://explore-datascience.net|"
                f"{title}>*"
                )
            return self._get_task_block(text, information)
        except:
            text = (
                "I don't have an answer to that."
                "Would you like to be notified when an answer becomes available?"
                )
            information = (
                "Notify me|"
                f"yes/no"
                )
            return self._get_no_answer_block(text, information)
        
   
    @staticmethod
    def request_answer(question):
        url = 'http://127.0.0.1:8000/models/1/doc-qa'
        pay = {"questions": [re.sub("'", "",question)], "top_k_retriever": 3, "top_k_reader": 1}
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
    def _get_no_answer_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]
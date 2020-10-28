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
        with open('data/questions.txt') as faq:
            self.faq = faq.read().split('\n')
            faq.close()
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
        return self._get_options_block(results)

        ###########################
    
    @staticmethod
    def _get_options_block(results):
        return [{
            "type": "section",	"text": {"type": "plain_text", "text": "Did you mean:"},
            "accessory": {
                "type": "radio_buttons",
                "action_id": "this_is_an_action_id",
                "initial_option": {
                    "value": "A1",
                    "text": {
                        "type": "plain_text",
                        "text": f"{results[0]}"
                        }
                    },
				"options": [
					{
						"value": "A1",
						"text": {
							"type": "plain_text",
							"text": f"{results[0]}"
						}
					},
					{
						"value": "A2",
						"text": {
							"type": "plain_text",
							"text": f"{results[1]}"
						}
					},
                    {
                        "value": "A3",
						"text": {
							"type": "plain_text",
							"text": f"{results[2]}"
						}
                    }
				]
			}
		}
        ]

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

# Replace contractions with full form of the words
    @staticmethod
    def _replace_contractions(text):
        contractions = json.load(open('../data/preprocessing/contractions.json',))
        for key in contractions.keys():
            text = re.sub(key, contractions[key], text)
        return text

# # Replace contractions with full length words
# df['msg_clean'] = df['msg_clean'].apply(lambda x: [word.replace(word, contractions[word.lower()]) if word.lower() in contractions else word for word in x])


### TEST: Radio button
#def _get_sim_questions(self):
#        distances, indices = self.GetNearestN(query=[self.question], n=self.n_sim_questions)
#        results = self.training_questions[indices[0]].tolist()
#        text = (
#            "Did you mean:\n"
#            f"{results[0]}\n"
#            f"{results[1]}\n"
#            f"{results[2]}\n"
#            "None of the above"
#       )
#        information = ("None")
#       return self._get_task_block(text, information)

#def get_answer_payload(self):
#        return {
#            "ts": self.timestamp,
#            "channel": self.channel,
#            "username": self.username,
#            "icon_emoji": self.icon_emoji,
#            "blocks": [
#               *self._get_answer_block(), 
#               self.DIVIDER_BLOCK,
#               *self._get_sim_questions()
#           ],
#       }
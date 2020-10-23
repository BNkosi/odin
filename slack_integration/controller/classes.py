import requests
import json
import re
from time import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import ngrams
import pandas as pd
from sklearn.neighbors import NearestNeighbors

class WebsiteOnboarding:
    """
    Constructs the Website onboarding chatbot and guides the user through website
    """

    HELLO_NEW_USER_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome to Explore, Mortal! I am Zeus :zap:\n\n"
                "My vast power has been harnessed by Explorers past to make your journey a little easier.\n"
                "My daughter - Athena- is here to teach you :pencil:\n"
                "And I am here to answer all your questions :question:\n\n"
                "*Choose an option below or just type your question*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "Odin"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.guide_task_completed = False
        self.register_task_completed = False
        self.application_task_complete = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.HELLO_NEW_USER_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_guide_block(),
                self.DIVIDER_BLOCK,
                *self._get_register_block(),
                self.DIVIDER_BLOCK,
                *self._get_application_block(),
            ],
        }

    def _get_guide_block(self):
        task_checkmark = self._get_checkmark(self.guide_task_completed)
        
        GUIDE_BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "Welcome to Explore, Mortal! I am Zeus :zap:\n\n"
                    "My vast power has been harnessed by Explorers past to make your journey a little easier.\n"
                    "My daughter - Athena- is here to teach you :pencil:\n"
                    "And I am here to answer all your questions :question:\n\n"
                    "*Choose an option below or just type your question*"
                ),
            },
        }
        self.DIVIDER_BLOCK
        OPTIONS_BLOCK = {
            "text": "What would you like to know about?",
            "attachments": [
                {
                    "text": "Choose a topic",
                    "fallback": "You are unable to choose a topic",
                    "callback_id": "new_user_guide",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "topic",
                            "text": f"{task_checkmark} Long Courses",
                            "type": "button",
                            "value": "long courses"
                        },
                        # {
                        #     "name": "topic",
                        #     "text": "Short Courses",
                        #     "type": "button",
                        #     "value": "short courses"
                        # },
                        # {
                        #     "name": "topic",
                        #     "text": "About Us",
                        #     "style": "danger",
                        #     "type": "button",
                        #     "value": "about us",
                            # "confirm": {
                            #     "title": "Are you sure?",
                            #     "text": "Wouldn't you prefer a good game of chess?",
                            #     "ok_text": "Yes",
                            #     "dismiss_text": "No"
                            # }
                        # }
                    ]
                }
            ]
        }

    def _get_register_block(self):
        pass

    def _get_application_block(self):
        pass

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

class QuestionAnswering:
    """Answers the users questions and stores FAQs"""

    def __init__(self, channel, question):
        self.channel = channel
        self.question = question
        self.username = "Odin"
        self.icon_emoji = ":page_facing_up:"
        self.timestamp = ""
        self.faq = set(["What are the fundamental values at explore?",
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
        self.vectorizer = TfidfVectorizer(min_df=1, analyzer='char', ngram_range=(1,5), lowercase=True)
        self.tfidf = self.vectorizer.fit_transform(self.training_questions)
        self.nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(self.tfidf)
        self.n_sim_questions = 3

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

    # @staticmethod    
    def GetNearestN(self, query, n):
        queryTFIDF_ = self.vectorizer.transform(query)
        distances, indices = self.nbrs.kneighbors(queryTFIDF_, n_neighbors=n)
        return distances, indices

    # @staticmethod
    def _get_answer_block(self):
        # Answers
        response = self.request_answer(self.question)
        answer = response['results'][0]['answers'][0]['answer']
        title = response['results'][0]['answers'][0]['meta']['name']
        conf = response['results'][0]['answers'][0]['probability']
        context = response['results'][0]['answers'][0]['context']
        # print(response)
        text = (
            f"*Question:*\n\n{self.question}\n\n"
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

class OnboardingTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome! I'm Zeus :robot_face: We're so glad you're here. :blush:\n\n"
                "We can't wait to get you on board.\n\n"
                "*The students even built me to show you around :robot_face:*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "Odin"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_reaction_block(),
                self.DIVIDER_BLOCK,
                *self._get_pin_block(),
            ],
        }

    def _get_reaction_block(self):
        task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f"{task_checkmark} *Add an emoji reaction to this message* :thinking_face:\n"
            "You can quickly respond to any message on Slack with an emoji reaction."
            "Reactions can be used for any purpose: voting, checking off to-do items, showing excitement."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
            "Learn How to Use Emoji Reactions>*"
        )
        return self._get_task_block(text, information)

    def _get_pin_block(self):
        task_checkmark = self._get_checkmark(self.pin_task_completed)
        text = (
            f"{task_checkmark} *Pin this message* :round_pushpin:\n"
            "Important messages and files can be pinned to the details pane in any channel or"
            " direct message, including group messages, for easy reference."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/205239997-Pinning-messages-and-files"
            "|Learn How to Pin a Message>*"
        )
        return self._get_task_block(text, information)

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]
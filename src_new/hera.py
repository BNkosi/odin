"""
Authors: Bulelani Nkosi, Caryn Pialat
Main api to run chatbot
"""

# Imports

import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from controllers.templates import QuestionAnswering

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], "/slack/events", app)
# slack_events_adapter.on()
# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
# Keep track of past messages
messages_received = {}

def answer_question(user_id: str, channel: str, question: str):
    """
    Function to answer questions
    """
    # Search for the answer
    question_answer = QuestionAnswering(channel, question)
    # Build answer payload
    answer = question_answer.get_answer_payload()

    # Post answer in slack
    response = slack_web_client.chat_postMessage(**answer)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed a task.
    question_answer.timestamp = response["ts"]


@slack_events_adapter.on('message')
def message(payload):
    """
    Responds to messages written to the bot
    """
    # Gather event data
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    print(text)
    event_id = payload.get("event_id")

    if event_id in messages_received.keys() and user_id == 'U01AZRT0S30':
        pass
    else:
        messages_received[event_id] = {
            "user": user_id,
            "text": text,
            "channel": channel_id
        }
        return answer_question(user_id, channel_id, text)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
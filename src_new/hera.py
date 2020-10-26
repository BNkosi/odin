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

@slack_events_adapter.on("message")
def handle_message(payload):
    event = payload.get("event", {})
    text = event.get("text")
    print("++++++++++++++++++++++")
    print(event)
    # If the incoming message contains "hi", then respond with a "Hello" message
    if event.get("subtype") is None and "hi" == text:
        channel = event.get("channel")
        message = "Hello <@%s>! :tada:" % event.get("user")
        slack_web_client.chat_postMessage(channel=channel, text=message)
    
    elif event.get("subtype") is None and text.endswith("?"):
        event = payload.get("event", {})
        channel = event.get("channel")
        user = event.get("user")
        return answer_question(user, channel, text)
    
if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
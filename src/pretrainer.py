import requests
import json
import os
import re
from haystack.utils import export_answers_to_csv
import logging
import subprocess
import time
import pprint
import pandas as pd
from typing import Dict, Any, List
from haystack.document_store.sql import DocumentORM
from collections import defaultdict

## Paths to raw questions and models
question_path = "/home/bulelani/Desktop/odin/odin/src_new/data/raw_questions"
url = 'http://127.0.0.1:8000/models/1/doc-qa' # use more accurate model in config.py

## initialize finders ands stuffies
from haystack import Finder
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.retriever.sparse import ElasticsearchRetriever

logger = logging.getLogger(__name__)

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
retriever = ElasticsearchRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False, no_ans_boost=0.6)
finder = Finder(reader, retriever)

## Lists
filtered_questions = list()
## Getting questions
for filename in os.listdir(question_path):
    with open(f"{question_path}/{filename}") as file:
        data = json.load(file)
        file.close()

    questions = list(data["question"])
    filtered_questions = [q for q in questions if "this course" in q]
    filtered_questions = list(set(filtered_questions))

## Answering questions
answers = list()
equad = {"data": [{"paragraphs": []}]}

{
    'question': 'What does this course help professionals who need to quickly upskill and enhance their SQL?',
    'no_ans_gap': 4.704477691650391,
    'answers': [
        {
            'answer': 'demonstrable and  practical skills', 
            'score': 10.06596565246582, 
            'probability': 0.7787239681151941, 
            'context': 'eed to rapidly upskill and enhance their SQL toolkit with demonstrable and  practical skills. This course is technical in nature. It is therefore reco', 
            'offset_start': 58, 
            'offset_end': 92, 
            'offset_start_in_doc': 3290, 
            'offset_end_in_doc': 3324, 
            'document_id': '23bc88fa-f41e-4bd3-97e9-268fd6f0ac92', 
            'meta': {
                'name': 'SQL_Prospectus_2020.txt'
                }
            }
        ]
    }
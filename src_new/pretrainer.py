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
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
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
total = len(filtered_questions)
print(filtered_questions)
times = list()
for i in range(total):

    try:
        _answers = finder.get_answers(question=filtered_questions[i], top_k_retriever=1, top_k_reader=1)

        _filtered_answers = list()
        for ans in range(len(_answers['answers'])):
            if _answers['answers'][ans]['probability'] >= 0.8:
                _filtered_answers.append(_answers['answers'][ans])
                print(f"accepted: {round(_answers['answers'][ans]['probability'],2)}\n")
            else:
                print(f"rejected: {round(_answers['answers'][ans]['probability'],2)}")

        _answers['answers'] = _filtered_answers

        answers.append(_answers)

        print(f"{round(i+1/total*100, 2)}% complete\n")
    except:
        pass

print(answers)
def convert_labels_to_squad(labels=answers):
    """
    Convert the export from the labeling UI to SQuAD format for training.

    :param labels_file: path for export file from the labeling tool
    :return:
    """

    labels_grouped_by_documents = defaultdict(list)
    for label in labels:
        labels_grouped_by_documents[label["document_id"]].append(label)

    labels_in_squad_format = {"data": []}  # type: Dict[str, Any]
    for document_id, labels in labels_grouped_by_documents.items():
        qas = []
        for label in labels:
            doc = DocumentORM.query.get(label["document_id"])

            assert (
                doc.text[label["start_offset"] : label["end_offset"]]
                == label["selected_text"]
            )

            qas.append(
                {
                    "question": label["question"],
                    "id": label["id"],
                    "question_id": label["question_id"],
                    "answers": [
                        {
                            "text": label["selected_text"],
                            "answer_start": label["start_offset"],
                            "labeller_id": label["labeler_id"],
                        }
                    ],
                    "is_impossible": False,
                }
            )

        squad_format_label = {
            "paragraphs": [
                {"qas": qas, "context": doc.text, "document_id": document_id}
            ]
        }

        labels_in_squad_format["data"].append(squad_format_label)

    with open("labels_in_squad_format.json", "w+") as outfile:
        json.dump(labels_in_squad_format, outfile)


# if __name__ == "__main__":
    # convert_labels_to_squad(labels=answers)
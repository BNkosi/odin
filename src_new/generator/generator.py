import os
import re
import json
from transformers import AutoModelWithLMHead, AutoTokenizer
from utils.utils import clean_website_text


class QuestionGenerator:
    def __init__(self, clean_func, doc_dir: str = '../data/documents/', question_dir: str = '../data/training/questions.json', max_length: int=64):
        self.doc_dir = doc_dir
        self.qu_dir = question_dir
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
        self.model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
        self.cleaning = clean_func

    def generate_qs(self):
        # Fetch documents
        self.docs=list()
        self.questions={
            "question": list,
            "title": list,
            "url": list,
            "context": list,
        }
        for filename in os.listdir(self.doc_dir):
            if filename.endswith(".txt"): 
                with open(str(self.doc_dir+filename), mode = 'r', encoding='utf-8') as doc:
                    text = doc.read()
                    text = clean_website_text(text)
                    self.docs.append({"title": filename, "text": text})
                    doc.close()
            else:
                continue
        
        # Generate list of training questions
        # for each document
        for doc in range(len(self.docs)):
            # get data
            title = self.docs[doc]["title"]
            text = self.docs[doc]["text"]
            link = [line for line in text.split("\n") if line.startswith("https:")]
            sentences = [line +"." for line in text.split("\n") if line.startswith("https:") == False or line != "" or line!= " "]
            
            for i in range(len(sentences[:6])):
                for word in sentences[i].split():
                    question = self.get_question(word, sentences[i])
                    question = re.sub('question: ', '', question)
                    self.questions["question"].append(question)
                    self.questions["title"].append(title)
                    self.questions["link"].append(link)
                    self.questions["context"].append(text)
        
        # Save questions to json
        with open(self.qu_dir, 'w') as fp:
            json.dump(self.questions, fp)
            fp.close()
            


    def get_question(self, answer, context, max_length=64):
        input_text = "answer: %s  context: %s </s>" % (answer, context)
        features = self.tokenizer([input_text], return_tensors='pt')

        output = self.model.generate(
            input_ids=features['input_ids'],
            attention_mask=features['attention_mask'],
            max_length=max_length
        )
        return self.tokenizer.decode(output[0])
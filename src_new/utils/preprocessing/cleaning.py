"""
    Description:    Data Preprocessing Functions
    Author :        BNkosi
"""

import re
import os
import numpy as np
import pandas as pd
import json

def clean_website_text(text: str()):
    # removing lines starting with "<", ">", "="
    exclude = []
    for i in range(len(text.split("\n"))):
        if text.split("\n")[i].startswith("<"):
            exclude.append(text.split("\n")[i])
        elif text.split("\n")[i].startswith("="):
            exclude.append(text.split("\n")[i])
        elif text.split("\n")[i].startswith(">"):
            exclude.append(text.split("\n")[i])
        elif text.split("\n")[i] == "":
            exclude.append(text.split("\n")[i])
        elif text.split("\n")[i] == " ":
            exclude.append(text.split("\n")[i])
    text_clean = []
    for i in text.split("\n"):
        if i not in exclude:
            text_clean.append(i)
    
    text = "\n".join(text_clean)
    
    # Text cleaning
    text = re.sub("Jan ", "January ", text)
    text = re.sub("Feb ", "February ", text)
    text = re.sub("Mar ", "March ", text)
    text = re.sub("Apr ", "April ", text)
    text = re.sub("May ", "May ", text)
    text = re.sub("Jun ", "June ", text)
    text = re.sub("Jul ", "July ", text)
    text = re.sub("Aug ", "August ", text)
    text = re.sub("Sep ", "September ", text)
    text = re.sub("Oct ", "October ", text)
    text = re.sub("Nov ", "November ", text)
    text = re.sub("Dec ", "December ", text)
    text = re.sub("&", "and", text)
    text = re.sub("T�s", "terms", text)
    text = re.sub("C�s", "conditions", text)
    text = re.sub("sure�", "sure?", text)
    text = re.sub("�Find your tribe�", "Find your tribe", text)
    text = re.sub("NQF", "National Qualifications Framework (NQF)", text)
    text = re.sub("team�s", "team's", text)
    text = re.sub("We're", "We are", text)
    text = re.sub("we're", "we are", text)
    text = re.sub("AWS", "Amazon Web Services", text)
    text = re.sub("Amazon's", "Amazon", text)
    text = re.sub("EC2", "Elastic Cloud Compute", text)
    text = re.sub("EBS", "Elastic Block Store", text)
    text = re.sub("EFS", "Elastic File Store", text)
    text = re.sub("S3", "Simple Storage, Service", text)
    text = re.sub("RDS", "Relational Database Service", text)
    text = re.sub("VPC", "Virtual Private Cloud", text)
    text = re.sub("Services", "", text)
    text = re.sub("IAM", "Identity and Access Management", text)
    text = re.sub("CSIR", "Council for Scientific and Industrial Research", text)
    text = re.sub("2/3", "2 to 3", text)
    text = re.sub("NLP", "Natural Language Processing", text)
    text = re.sub("JanuarydeWet", "January de Wet", text)
    text = re.sub("UK", "United Kingdom", text)
    text = re.sub("fin-tech", "financial services technology", text)
    text = re.sub("�ll", " will", text)
    text = re.sub("n�t", " not", text)
    text = re.sub("1:1", "one-on-one", text)
    text = re.sub("we�ve", "we have", text)
    text = re.sub("We�ve", "we have", text)
    text = re.sub("We�re", "We are", text)
    text = re.sub("we�re", "we are", text)
    text = re.sub("/", " or ", text)
    text = re.sub("API�s", "application programming interfaces", text)
    text = re.sub("ANN�s", "Artificial Neural Networks", text)
    text = re.sub("CNN�s", "Convolutional Neural Networks", text)
    text = re.sub("RNN�s", "Recurrent Neural Networks", text)
    text = re.sub("it�s", "it is", text)
    text = re.sub("\t", " ", text)
    text = re.sub("CAs", "Chartered Accountants", text)
    text = re.sub("CA's", "Chartered Accountant's", text)
    text = re.sub("An innovate", "An innovative", text)
    text = re.sub("it's", "it is", text)
    text = re.sub("It's", "It is", text)
    text = re.sub("don't", "do not", text)
    text = re.sub("There's", "There is", text)
    text = re.sub("you'll", "you will", text)
    text = re.sub("you're", "you are", text)
    text = re.sub("We've", "We have", text)
    text = re.sub("we've", "we have", text)
    text = re.sub("you�re", "you are", text)
    text = re.sub("�CTC�", "(CTC)", text)
    text = re.sub("�Qualifying Position�", '"Qualifying Position"', text)
    text = re.sub(".Explore", "Explore", text)
    text = re.sub("Explore�s", "Explore's", text)
    text = re.sub("you�ve", "you have", text)
    text = re.sub("�TWOE�", "(TWOE)", text)
    text = re.sub("coaches�", "coaches'", text)
    text = re.sub("IRP5�s", "IRP5's", text)
    text = re.sub("sill", "will", text)
    text = re.sub("we'll", "we will", text)
    text = re.sub("�ve", " have", text)
    text = re.sub("It�s been", "It has been", text)
    text = re.sub("It�s a", "It is a", text)
    text = re.sub("It�s open", "It is open", text)
    text = re.sub("It�s used", "It is used", text)
    text = re.sub("It�s free", "It is free", text)
    text = re.sub("It�s very", "It is very", text)
    text = re.sub("SVM�s", "Support Vector Machines", text)
    text = re.sub("I�m", " I am", text)
    text = re.sub("country�s", "country's", text)
    text = re.sub("projects�helping", "projects - helping", text)
    text = re.sub("EXPLORE�s", "EXPLORE's", text)
    text = re.sub("That�s", "That is", text)
    text = re.sub("month�s", "month's", text)
    text = re.sub("South African�s", "South Africans", text)
    text = re.sub("Data Scientist�s", "Data Scientist's", text)
    text = re.sub("�Data Scientist�", '"Data Scientist"', text)
    text = re.sub("�sexiest profession of the 21st Century�", '"sexiest profession of the 21st Century"', text)
    text = re.sub("email�protected", "email protected", text)
    text = re.sub("python�s", "Python's", text)
    text = re.sub("he�s", "he is", text)
    text = re.sub("�Reading�s", "Reading's", text)
    text = re.sub("1,000�s", "thousands", text)
    text = re.sub("They�re", "They are", text)
    text = re.sub("they�re", "they are", text)
    text = re.sub("customer�s", "customer's", text)
    text = re.sub('\\"', "", text)
    text = re.sub(" � ", " - ", text)
    text = re.sub("�", "", text)    
    # Join text into one line
    text = " ".join(text.split('\n'))
    return text

def clean_text_files(doc_dir: str()):
    """
    Function to fix utf-8 errors
    Parameters
    ----------
        doc_dir (path):
            path to document folder
    """
    for filename in os.listdir(path=doc_dir):
        with open(os.path.join(doc_dir, filename), 'r', encoding='utf-8', errors='replace') as file:
            text = file.read()
            file.close()
        with open(os.path.join(doc_dir, filename), 'w', encoding='utf-8', errors='replace') as file:
            file.write(text)
            file.close()

def clean_wiki_text(text: str) -> str:
    # get rid of multiple new lines
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")

    # remove extremely short lines
    lines = text.split("\n")
    cleaned = []
    for l in lines:
        if len(l) > 30:
            cleaned.append(l)
        elif l[:2] == "==" and l[-2:] == "==":
            cleaned.append(l)
    text = "\n".join(cleaned)

    # add paragraphs (identified by wiki section title which is always in format "==Some Title==")
    text = text.replace("\n==", "\n\n\n==")

    # remove empty paragrahps
    text = re.sub(r"(==.*==\n\n\n)", "", text)

    return text

# Importing libraries which will assist in removing the html tags
from io import StringIO
from html.parser import HTMLParser

"""Remove html tags from messages"""

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

directory = 'data/documents'
faq_dict = {}
counter = 0

for filename in os.listdir(directory):
    if (filename.endswith(".txt") and 'blog_' not in filename):
        f = open('utils/data/documents/{}'.format(filename), 'r+', encoding='utf-8')
        string_list = f.readlines()
        
        if len(string_list) > 0:
            
            # Cleans blank lines and random sub-headings from the text (Part 1 of 2)
            new_lines = [line for line in string_list if line != '\n' and line != ' \n']
            new_lines = [strip_tags(line) for line in new_lines]
            new_lines = [re.sub(' +', ' ', line) for line in new_lines]
            new_lines = [re.sub('\xa0', '', line) for line in new_lines]
            for i in range(len(new_lines) - 1):
                if new_lines[i] == new_lines[i+1]:
                    new_lines[i] = ' '
            for i in range(len(new_lines)):
                if new_lines[i].startswith(' '):
                    new_lines[i] = ' '
            new_lines = [line for line in new_lines if line != ' ']

            try:
                # Look for questions that aren't in headings
                for i in range(len(new_lines)):
                    if '?' in new_lines[i]:
                        if new_lines[i] in faq_dict.keys():
                            a = faq_dict[new_lines[i]]
                            if new_lines[i + 1] not in a:
                                a.append(new_lines[i + 1])
                                faq_dict[new_lines[i]] = a
                        else:
                            faq_dict[new_lines[i]] = [new_lines[i + 1]]

                # Look for questions in H2 headings
                    if ('?' in new_lines[i] and 'H2' in new_lines[i]):
                        key = new_lines[i]
                        vals = []
                        j = i + 1
                        while 'H2' not in new_lines[j]:
                            vals.append(new_lines[j])
                            j += 1
                        if key in faq_dict.keys():
                            a = faq_dict[key]
                            for k in range(len(vals)):
                                if vals[k] not in a:
                                    a.append(vals[k])
                                    faq_dict[key] = a
                        else:
                            faq_dict[key] = vals

                # Look for questions in H3 headings
                    if ('?' in new_lines[i] and 'H3' in new_lines[i]):
                        key = new_lines[i]
                        vals = []
                        j = i + 1
                        while 'H2' not in new_lines[j]:
                            vals.append(new_lines[j])
                            j += 1
                        if key in faq_dict.keys():
                            a = faq_dict[key]
                            for k in range(len(vals)):
                                if vals[k] not in a:
                                    a.append(vals[k])
                                    faq_dict[key] = a
                        else:
                            faq_dict[key] = vals
            except:
                print('Skipped file: {}'.format(filename))
            
            # Cleans blank lines and random sub-headings from the text (Part 2 of 2)
            new_lines = [line for line in new_lines if line not in faq_dict.keys() and line not in faq_dict.values() and 'FAQ' not in line]
            new_lines = [re.sub('H\d: ', '', line) for line in new_lines]
            new_lines = [re.sub('Paragraph: ', '', line) for line in new_lines]
            new_lines = [line for line in new_lines if line != '\n' and line != ' \n']
            final_lines = []
            final_lines = [line for line in new_lines if line not in final_lines]
            final_lines = list(dict.fromkeys(final_lines))

            # Write cleaned text data to new text file
            if len(final_lines) > 0:
                f_cl = open('utils/data/documents/cleaned_{}'.format(filename), 'w+', encoding='utf-8')
                for i in range(len(final_lines)):
                    f_cl.write(final_lines[i])
                f_cl.close()
        f.close()
    counter += 1
    print('Complete {0} {1}'.format(counter, filename))
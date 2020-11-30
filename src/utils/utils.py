import os
import io
import re
import time
import logging
import requests
import pdfplumber
import subprocess
import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from io import BytesIO, StringIO
from html.parser import HTMLParser
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore

class Pipeline():
    """
    Class to scrape, create and clean text files, load documuents to elasticsearch
    Parameters
    ----------
        URL (str): website url
        path_to_data (str): file save path
    """
    def __init__(self, URL:str = 'https://explore-datascience.net', path_to_data:str = "../src/data/documents/"):
        """
        Initialize by: accessing website, getting urls and pdfs
        """
        self.URL = URL
        self.data_path = path_to_data
        self.page = requests.get(self.URL)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.urls_list = self.get_urls(self.soup)
        self.urls, self.new_urls, self.pdfs = self.website_links(self.urls_list, self.get_urls)
        if self.new_urls > 0:
            self.urls, self.new_urls, self.pdfs = self.website_links(self.urls_list, self.get_urls)

    def scrape_website(self):
        """
        Function to scrape website text
        """
        for i in range(len(self.urls)):
            _url = self.urls[i]
            _page = requests.get(_url)
            _soup = BeautifulSoup(_page.content, 'html.parser')
            _name = str(_url).replace(self.URL, 'explore').replace('/', '_')
            if os.path.exists(f"{self.data_path}{_name}.txt"):
                os.remove(f"{self.data_path}{_name}.txt")
            with open((f"{self.data_path}{_name}.txt"), "w", encoding="utf-8") as f:
                f.write('{}\n'.format(str(_url)))
                for items in _soup.find_all():
                    all_text = [item.text for item in items.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'p'])]
                    for j in all_text:
                        f.write('{}\n'.format(j))
                f.close()
        
        for i in self.pdfs:
            try:
                _rq = requests.get(i)
                _pdf = pdfplumber.open(BytesIO(_rq.content))
                _name = "".join(re.findall(r'pdf/(.*?).pdf', str(i)))
                _name = _name.replace('careers/', '').replace(" ", "_").replace("_(1)", "")
                _myfile = io.open(f"{self.data_path}{_name}.txt", "w", encoding="utf-8")
                _myfile.write(str(i)+"\n")
                for j in range(len(_pdf.pages)):
                    _p = _pdf.pages[j]
                    _text = _p.extract_text()
                    _myfile.write(str(_text)+"\n ")
                _myfile.close()
            except:
                raise("Unable to scrape")
            finally:
                pass

    def web_cleaning(self):
        for filename in os.listdir(self.data_path):
            if (filename.endswith(".txt") and 'blog_' not in filename):
                f = open(f'{self.data_path}{filename}', 'r+', encoding='utf-8')
                string_list = f.readlines()

                if len(string_list) > 0:

                    new_lines = [line for line in string_list if line != '\n' and line != ' \n']
                    new_lines = [self.strip_tags(line) for line in new_lines]
                    new_lines = [re.sub(' +', ' ', line) for line in new_lines]
                    new_lines = [re.sub('\xa0', '', line) for line in new_lines]
                    for i in range(len(new_lines) - 1):
                        if new_lines[i] == new_lines[i+1]:
                            new_lines[i] = ' '
                    for i in range(len(new_lines)):
                        if new_lines[i].startswith(' '):
                            new_lines[i] = ' '
                    new_lines = [line for line in new_lines if line != ' ']

                    # new_lines = [line for line in new_lines if line not in faq_dict.keys() and line not in faq_dict.values() and 'FAQ' not in line]
                    # new_lines = [re.sub(r'H\d: ', '', line) for line in new_lines]
                    # new_lines = [re.sub('Paragraph: ', '', line) for line in new_lines]
                    new_lines = [line for line in new_lines if line != '\n' and line != ' \n']
                    final_lines = []
                    final_lines = [line for line in new_lines if line not in final_lines]
                    final_lines = list(dict.fromkeys(final_lines))

                    # Write cleaned text data to new text file
                    if len(final_lines) > 0:
                        with open(f'{self.data_path}{filename}', 'w+', encoding='utf-8') as f_cl:
                            for i in range(len(final_lines)):
                                f_cl.write(final_lines[i])
                            f_cl.close()
                f.close()

    def launch_elasticsearch(self, launch: bool = False, name:str = "hera"):
        if launch:
            logging.info("Starting Elasticsearch ...")
            status = subprocess.run(
                [f'docker run -d -p 9200:9200 --name "hera" -e "discovery.type=single-node" elasticsearch:7.6.2'], shell=True
                )
            time.sleep(30)
        else:
            logging.info("Starting Elasticsearch ...")
            try:
                status = subprocess.run(
                ['docker stop hera'], shell=True
                )
            except:
                raise("No running containers")
            
            finally:
                status = subprocess.run(
                    ['docker start hera'], shell=True
                    )
                time.sleep(30)

        index = "document"
        document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index=index)

        dicts = convert_files_to_dicts(dir_path=self.data_path, clean_func=self.clean_website_text, split_paragraphs=True)
        try:
            document_store.delete_all_documents(index=index)
        except:
            pass
        finally:
            document_store.write_documents(dicts)
        return status

    @staticmethod
    def get_urls(soup):
        """
        Function returns a list of all url links from a BeautifulSoup object.
        """
        _urls = []
        for link in soup.find_all('a'):
            if link.get('href') != None:
                _urls.append(link.get('href'))
        _urls = [x for x in _urls if 'https' in x]
        _urls = list(set(_urls))
        return _urls

    @staticmethod
    def website_links(urls_list, url_scraper):
        """
        Function splits up the urls_list into urls and pdfs. It then accesses each
        url in the list and scrapes additional urls and pdfs that may have been missed.
        ----------
        Returns:
        lists of urls and pdfs, integer value of the number of urls
        """
        _urls = [x for x in urls_list if '.pdf' not in x and 'facebook' not in x and 'twitter' not in x and 'linkedin' not in x]
        _pdfs = [x for x in urls_list if '.pdf' in x]
        _new_urls = []
        for i in range(len(_urls)):
            _page = requests.get(_urls[i])
            _soup = BeautifulSoup(_page.content, 'html.parser')
            _pg_urls = url_scraper(_soup)
            if len(_pg_urls) > 0:
                _pdfs.extend([x for x in _pg_urls if '.pdf' in x and x not in _pdfs])
                _new_urls.extend([x for x in _pg_urls if x not in _urls 
                                and x not in _new_urls 
                                and x not in _pdfs 
                                and 'https://explore-datascience.net' in x])
        _urls.extend(_new_urls)
        return _urls, len(_new_urls), _pdfs

    @staticmethod
    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    @staticmethod
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
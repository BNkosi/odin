# Import libraries
#pip install pdfplumber
import io
import re
import time
import requests
import pdfplumber
import numpy as np
import pandas as pd
import urllib.request
from io import BytesIO
from bs4 import BeautifulSoup

# Functions to extract all urls from the website page
def get_urls(soup):
    """
    Function returns a list of all url links from a BeautifulSoup object.
    """
    urls = []
    for link in soup.find_all('a'):
        if link.get('href') != None:
            urls.append(link.get('href'))
    urls = [x for x in urls if 'https' in x]
    urls = list(set(urls))
    return urls

def website_links(urls_list):
    """
    Function splits up the urls_list into urls and pdfs. It then accesses each
    url in the list and scrapes additional urls and pdfs that may have been missed.
    ----------
    Returns:
    lists of urls and pdfs, integer value of the number of urls
    """
    urls = [x for x in urls_list if '.pdf' not in x and 'facebook' not in x and 'twitter' not in x and 'linkedin' not in x]
    pdfs = [x for x in urls_list if '.pdf' in x]
    new_urls = []
    for i in range(len(urls)):
        page = requests.get(urls[i])
        soup = BeautifulSoup(page.content, 'html.parser')
        pg_urls = get_urls(soup)
        if len(pg_urls) > 0:
            pdfs.extend([x for x in pg_urls if '.pdf' in x and x not in pdfs])
            new_urls.extend([x for x in pg_urls if x not in urls 
                             and x not in new_urls 
                             and x not in pdfs 
                             and 'https://explore-datascience.net' in x])
    urls.extend(new_urls)
    return urls, len(new_urls), pdfs

# Open website home page
URL = 'https://explore-datascience.net/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# Extract urls and pdfs from website
urls_list = get_urls(soup)
urls, new_urls, pdfs = website_links(urls_list)
if new_urls > 0:
    urls, new_urls, pdfs = website_links(urls_list)

# Scrape text data from the website (this excludes the pdfs)
a = 0
for i in range(len(urls)):
    page = requests.get(urls[i])
    soup = BeautifulSoup(page.content, 'html.parser')
    name = str(urls[i]).replace('https://explore-datascience.net', 'explore').replace('/', '_')
    f = open("data/documents/{}.txt".format(name), "a+", encoding="utf-8")
    f.write('{}\n'.format(str(urls[i])))
    for items in soup.find_all():
        all_text = [item.text for item in items.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'p'])]
        for j in all_text:
            f.write('{}\n'.format(j))
    f.close()
    a += 1
print('Completed: {1} of {2}'.format(a, len(urls)))

pdfs = ['https://explore-datascience.net/pdf/EDSA_Course_Outline.pdf?12.4',
 'https://explore-datascience.net/pdf/Data_Analytics.pdf',
 'https://explore-datascience.net/pdf/EDSA_Course_Outline.pdf',
 'https://explore-datascience.net/pdf/Data_Science.pdf',
 'https://explore-datascience.net/pdf/Full_Syllbus_DS_for_Executives_Mar_2020.pdf',
 'https://explore-datascience.net/pdf/Machine_Learning_Analysts_Short.pdf',
 'https://explore-datascience.net/pdf/careers/Senior_Data_Scientist.pdf',
 'https://explore-datascience.net/pdf/careers/Senior_Data_Engineer.pdf',
 'https://explore-datascience.net/pdf/Machine_Learning_for_Analysts.pdf',
 'https://explore-datascience.net/pdf/Data_Engineering.pdf',
 'https://explore-datascience.net/pdf/Full_Syllbus_DS_for_Managers_Mar_2020.pdf',
 'https://explore-datascience.net/pdf/Data_Science_Managers_Short.pdf',
 'https://explore-datascience.net/pdf/Advanced_Python_Short.pdf',
 'https://explore-datascience.net/pdf/Explore_Course_Catalogue.pdf',
 'https://explore-datascience.net/pdf/Advanced_Visualisation_Short.pdf',
 'https://explore-datascience.net/pdf/Data_Science_High_School_Short.pdf',
 #'https://explore-datascience.net/pdf/aws_cloud_practitioner_short.pdf',
 'https://explore-datascience.net/pdf/Deep_Learning_AI.pdf',
 'https://explore-datascience.net/pdf/Insights_Led_Organisation.pdf',
 'https://explore-datascience.net/pdf/How to Structure Your Data Science Capability.pdf',
 'https://explore-datascience.net/pdf/Investing_in_LandD.pdf',
 'https://explore-datascience.net/pdf/A Data Science Team.pdf',
 'https://explore-datascience.net/pdf/Ogranization_Data_Maturity.pdf',
 'https://explore-datascience.net/pdf/Machine_Learning_for_Analysts_Short.pdf']

# Scrape text data from the PDFs
a = 0
for i in pdfs:
    rq = requests.get(i)
    pdf = pdfplumber.open(BytesIO(rq.content))
    name = "".join(re.findall(r'pdf/(.*?).pdf', str(i)))
    name = name.replace('careers/', '')
    myfile = io.open('data/documents/' + name + ".txt", "w", encoding="utf-8")
    for i in range(len(pdf.pages)):
        p = pdf.pages[i]
        text = p.extract_text()
        myfile.write(str(text)+"\n ")
    myfile.close()
    a += 1

print('Completed: {1} of {2}'.format(a, len(pdfs)))
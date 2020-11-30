"""
Data pipeline for webscraping, cleaning and loading elasticsearch
"""
from utils.utils import Pipeline
import subprocess
import os
import time

# SCRAPE = True


if __name__ == "__main__":
    pipe = Pipeline()
    # print('Scraping')
    # pipe.scrape_website()
    print('cleaning')
    pipe.web_cleaning()
    print('Launching')
    try:
        pipe.launch_elasticsearch()
    except:
        print("No available containers, launching new one")
        pipe.launch_elasticsearch(True)
    

"""
Data pipeline for webscraping, cleaning and loading elasticsearch
"""
from utils.utils import Pipeline
import subprocess
import os

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
    else:    
        pipe.launch_elasticsearch(True)
    
    ## Dont forget `export SLACK_SIGNING_SECRET="xxxxx"` `export SLACK_BOT_TOKEN='xoxb-xxxx'
    os.system('gunicorn rest_api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300 --daemon')
    os.system('FLASK_ENV=development python3 hera.py')
    

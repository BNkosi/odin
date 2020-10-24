"""
Data pipeline for webscraping, cleaning and loading elasticsearch
"""
import logging
import subprocess
import time

# Scrape data

def scrape():
    logging.info("Scraping explore-datascience.net...")
    status = subprocess.run(
        ['python3 web_scraper/webscraper.py'], shell=True
    )
    return status
scrape()
"""
	Script to download documents, initiate document store, clean and index documents

	Author: BNkosi
"""
import logging
import subprocess
import time

from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from utils.cleaning import clean_text_files, clean_website_text
from haystack.preprocessor.utils import convert_files_to_dicts, fetch_archive_from_http

logger = logging.getLogger(__name__)

LAUNCH_ELASTICSEARCH = False # Set to False to add documents

if LAUNCH_ELASTICSEARCH:
    logging.info("Starting Elasticsearch ...")
    status = subprocess.run(
        ['docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.6.2'], shell=True
    )
    if status.returncode:
        raise Exception("Failed to launch Elasticsearch. If you want to connect to an existing Elasticsearch instance"
                        "then set LAUNCH_ELASTICSEARCH in the script to False.")
    time.sleep(15)

# Connect to Elasticsearch
index = "document"
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

# Download data
doc_dir = "data/explore-datascience.net"
data_url = "https://github.com/Thabo-5/Chatbot-scraper/raw/master/txt_files/Cleaned/Cleaned.zip"
fetch_archive_from_http(url=data_url, output_dir=doc_dir)

# Document Preprocessing
# ## Fix Encoding errors
clean_text_files(doc_dir=doc_dir)

# ## Convert files to dicts containing documents that can be indexed  to our datastore
dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_website_text, split_paragraphs=True)
# ## The cleaning function "clean_website_text" has been applied twice in clean_text_files and in conversion.

# Wrting docs to DB.
if LAUNCH_ELASTICSEARCH:
	document_store.write_documents(dicts)
else:
	try:
		document_store.delete_all_documents(index="documents")
	except:
		pass
	finally:
		document_store.write_documents(dicts)
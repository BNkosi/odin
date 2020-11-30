import logging
import subprocess
import time

from haystack import Finder
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.retriever.sparse import ElasticsearchRetriever

logger = logging.getLogger(__name__)

LAUNCH_ELASTICSEARCH = True

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
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

doc_dir = "/home/bulelani/Desktop/odin/odin/src_new/data/demo"

dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
# You can optionally supply a cleaning function that is applied to each doc (e.g. to remove footers)
# It must take a str as input, and return a str.

# Now, let's write the docs to our DB.
if LAUNCH_ELASTICSEARCH:
    document_store.write_documents(dicts)
else:
    logger.warning("Since we already have a running ES instance we should not index the same documents again. \n"
                   "If you still want to do this call: document_store.write_documents(dicts) manually ")
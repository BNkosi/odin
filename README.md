# Installation Instructions

1. Create a virtual environment:
`python3.6 -m venv odin_env`

2. Activate the virtual environment:
`source odin_env/bin.activate`

3. Clone the Odin repository:
`git clone https://github.com/BNkosi/odin.git`

4. Navigate to haystack
`cd haystack`

5. Install editable to keep haystack up to date with the main repo
`pip install --editable ~/Desktop/odin/odin/haystack`

6. pip install haystack to ensure packages have been installed
`pip install farm-haystack`

# First time use

Before we can make any predictions we must first load our documents into Elasticsearch, download and train a model.
1. To load documents, run `python odin/src/documents.py`. This will only be allowed to run once to prevent duplication of documents.

2. To download and train a model, run `python odin/src/fine-tune.py`. Use the [annotation tool](https://annotate.deepset.ai/) to generate training data.

# Continuous use - Coming soon

1. Adding new documents
2. Training on feedback data
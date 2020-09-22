# Odin
Odin is a closed domain question answering package for Explore Data Science Academy.
The package is required to assist in the onboarding of new  students and provide administrative guidance for the course.
This will benefit Explore by providing students with an alternative resource to Supervisors therby freeing up Supervisor time.

## 1. Installation Instructions
### 1.1 Odin

1. Create a virtual environment:
`python3.6 -m venv odin_env`

2. Activate the virtual environment:
`source odin_env/bin.activate`

3. Clone the Odin repository:
`git clone https://github.com/BNkosi/odin.git`

At this point you have the code for odin but you need haystack to make it work.

4. Change directory to odin
`cd path/to/odin`

### 1.2 Haystack

5. Delete the haystack folder - it is empty
`rm -R haystack`

6. For development installation (latest updates) -**Not recommended for instance**
`git clone https://github.com/deepset-ai/haystack.git`
`cd haystack`
`pip install --editable path/to/haystack` _eg: `pip install --editable ~/Desktop/explore/odin/haystack`_

7. Compute Instance installation
`git clone https://github.com/deepset-ai/haystack.git`
`cd haystack`
`python setup.py`

### 1.3 Docker

Our Elasticsearch server is going to be run with Docker. Follow the appropriate instructions below

a. [Linux installation instruction](https://docs.docker.com/engine/install/ubuntu/)
b. [Windows 10 build 18563+](https://docs.docker.com/docker-for-windows/install/)

## 2. Dataloading and model training - First use only

### 2.1 Initial setup

1. Navigate to `haystack/rest_api/config.py` and edit line 30 to read:
`READER_MODEL_PATH = os.getenv("READER_MODEL_PATH", "../../saved_models/distilbert-base-uncased-distilled-squad")` save and exit. _this step may be skipped if you are not ready to train a model_

### 2.2 Initialize Docker, clean and index documents

2. Change directory to `src`
`cd ../src`

3. Open documents.py and make the following adjustments:
	line 16: change `False` to `True` _first setup only_
	line 29: if adding new documents, specify and index name
	line 34: download a zip file from your s3 bucket

4. Run `python odin/src/documents.py`.
	notes: 
	a. When LAUNCH_ELASTICSEARCH is set to false, documents in an index will be deleted. Do avoid deletion change the index.
	b. The document cleaning function can be found in `src/utils/cleaning.py`. Function input/output must be a `str`

### 2.3 Model training and saving

1. Open fine-tune.py and edit the following lines:
	line 31: Choose a model from [Hugging Face's Model hub](https://huggingface.co/models) AND set gpu parameter
	line 32 and 34: adjust file path, file name, n_epochs and batch_size _if necessary_

2. Run
`python odin/src/fine-tune.py`.

3. Use the [annotation tool](https://annotate.deepset.ai/) to generate training data.

## Rest API

**If this is your first time running this, skip step 1**

1. Run a single Elasticsearch node using docker:
`docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.6.2`

2. To serve the API run:
`gunicorn rest_api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300`

3. You will find the Swagger API documentation at http://127.0.0.1:8000/docs.
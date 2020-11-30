<div align="center" id="top"> 
  [<img src="./img/H.e.r.a.png" alt="H.E.R.A">](https://youtu.be/gsDucStJIJw)

  &#xa0;

  <!-- <a href="https://odin.netlify.app">Demo</a> -->
</div>

<h1 align="center">H.E.R.A</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/BNkosi/odin?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/BNkosi/odin?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/BNkosi/odin?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/BNkosi/odin?color=56BEB8">

  <img alt="Github issues" src="https://img.shields.io/github/issues/BNkosi/odin?color=56BEB8" />

  <img alt="Github forks" src="https://img.shields.io/github/forks/BNkosi/odin?color=56BEB8" />

  <img alt="Github stars" src="https://img.shields.io/github/stars/BNkosi/odin?color=56BEB8" />
</p>

Status

<h4 align="center"> 
	🚧  Hera 🚀 Under construction...  🚧
</h4> 

<hr>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0;
  <a href="#sparkles-works">How It Works</a> &#xa0; | &#xa0;

  <a href="#rocket-technologies">Requirements</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Getting Started</a> &#xa0; | &#xa0;
  <a href="#hammer-features">Improvements</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/BNkosi" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

### :question::exclamation: Problem Statement ###

[![Watch the video]("./img/H.e.r.a.png)](https://youtu.be/gsDucStJIJw)

<a href="https://www.explore-datascience.net">Explore Data Science Academy</a> is an amazing company helping South Africas youth do amazing things. This repository is a testament to that. Explore is an educational institution in the information systems development field.

Student enquiries are an administrative burden on the company. For reasons which are little understood, users cannot find information on the website and require human assistance.

Hera aims to address this issue by creating an information retrieval assistant to act as the first trouble shooting step before contacting a member of staff.

## :sparkles: How It Works ##

##  :white_check_mark:  Requirements ##

The following tools were used in this project:

- [Docker](https://docs.docker.com)
- [Slack App](https://api.slack.com/apps)
- [Ngrok](https://ngrok.com/)
- [Haystack](https://github.com/deepset-ai/haystack)

## :checkered_flag: Getting Started ##

```bash
# Clone this project
$ git clone https://github.com/Bnkosi/odin.git

# Access
$ cd odin

# Install dependencies
$ pip install farm-haystack==0.4.9
```

### Setting up Slack Auth ###

Before starting :checkered_flag:, you need to have [a Slack App](https://api.slack.com/apps), Slack Signing Secret and Slack Bot Token. You cannot proceed without these. You will also need to install [Docker](https://docs.docker.com/engine/install/ubuntu/) to run the ElasticSearch container, and [Ngrok](https://ngrok.com/) to connect the bot to the internet.

```bash
# Install signing secret
$ export SLACK_SIGNING_SECRET="xxxxx" 

# Install token
$ export SLACK_BOT_TOKEN="xoxb-xxxx"
```

### :notebook: Run the pipeline ###

H.E.R.A works by scraping your website and loading this data into and ElasticSearch Document Store. It is possible to ask questions immediately but to improve accuracy, a model should be trained.

```bash
# A. Scrape Website
$ python3 pipeline.py


# B. If you have previously run the step above, start here
# 1. Start docker container
$ docker ps -a  # view available containers
$ docker start hera # start container

# 2. Write documents to ElasticSearch
# Change Document location and run
$ python3 add_doc.py

# 3. Start the Question Answering API
$ gunicorn rest_api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300

# 4. Start Hera
$ python3 hera.py
```

### :arrows_counterclockwise: Set up a tunnel ###

You will need to set up a HTTP tunneler to allow slack to communicate with your local server

```bash
# Navigate to ngrok installation folder and run the following.
$ ./ngrok http 3000
```

Copy the resultant https forwarding address and update the Slack App Event Subscriptions Request URL. 

eg: `https://6fdef00d53b6.ngrok.io/slack/events`

### :robot: Interacting with the bot ###

Open your Slack workspace, invite the bot to a channel and ask it a few questions. You can watch a demo of the bot [here](https://youtu.be/JZyE4Mu4ddo)

## Updating documents ##

From time to time you might need to ad documents that specifically address issues that are not covered by the website. In those cases, add your txt files to a folder and rund the script below. Remember to change the file paths.

```bash
# Change Document location and run
$ python3 add_doc.py
```

## Fine-Tuning ###

When you are ready to improve the models accuracy, you will need to train it on annotated data. Documents can be manually annotated using Deepset annotation tool.

### Coming Soon - Learning to answer by learning to ask ###

The process of document annotation is tedious and requires a substantial investment in time to generate and label documents. To solve this, we have built twon in-progress scripts.

1. Generator - The generator reads every all the text files and attempts to generate a question for every word (token). Noteably, most of the questions will be useless due to being to general or having been generated on invalid tokens.

2. Pretrainer - The pretrainer then attempts to answer every question from the generator. It is important that we set the `NO_ANS_BOOST` fairly high in order to filter out useless questions. After answering the questions, a dataset is generated and the model is ready to be trained.

### Training ###

Once the dataset has been downloaded from the annotation tool, run the following to train the model

```bash
# Train
$ python3 trainer.py
```

## :rocket: Improvements ##

:heavy_check_mark: Retrieval-Augmented Generation - Currently the model works by selecting the most appropriate span of text and presenting it as the answer (extractive QA). The next step is the generation of novel answers from the same documents. This makes the bot more human-like and thus more trust-worthy.;\

:heavy_check_mark: Generative Pretraining - The annotation tool is labour intesive and costly. Generative Pretraining aims to simulate a human asking and answerinig (annotating) documents. The code is present but still needs fine-tuning;\

:heavy_check_mark: Context Management - Users ask ambiguous questions, such as: "How much is this course?". Context management allows the bot to know which course the user is talking about or ask for clarity where there is uncertainty.;

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/BNkosi" target="_blank">Bulelani Nkosi</a> and <a href="https://github.com/carynpialat" target="_blank">Caryn Pialt</a>

Special Thanks :heart::heart: Pfano Phungo

&#xa0;

<a href="#top">Back to top</a>

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
  <a href="#hammer-features">Installation</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Getting Started</a> &#xa0; | &#xa0;
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

## :hammer: Installation ##

:heavy_check_mark: Feature 1;\
:heavy_check_mark: Feature 2;\
:heavy_check_mark: Feature 3;

## :rocket: Technologies ##

The following tools were used in this project:

- [Docker](https://docs.docker.com)
- [Slack App](https://api.slack.com/apps)
- [Ngrok](https://ngrok.com/)
- [Haystack](https://github.com/deepset-ai/haystack)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [a Slack App](https://api.slack.com/apps), Slack Signing Secret and Slack Bot Token. You cannot proceed without these. You will also need to install [Docker](https://docs.docker.com/engine/install/ubuntu/) to run the ElasticSearch container, and [Ngrok](https://ngrok.com/) to connect the bot to the internet.

```bash
# Install signing secret
$ export SLACK_SIGNING_SECRET="xxxxx" 

# Install token
$ export SLACK_BOT_TOKEN="xoxb-xxxx"
```

## :checkered_flag: Getting Started ##

```bash
# Clone this project
$ git clone https://github.com/Bnkosi/odin.git

# Access
$ cd odin

# Install dependencies
$ pip install farm-haystack==0.4.9
```

### :page_facing_up: Run the pipeline ###

H.E.R.A works by scraping your website and loading this data into and ElasticSearch Document Store. It is possible to ask questions immediately but to improve accuracy, a model should be trained.

```bash
# First time use/refreshing documents
$ python3 pipeline.py

# USE THIS IF YOU HAVE THIS IS NOT THE FIRST USE
# 1. Start docker container
$ docker run <container_name>

# 2. Start the app
$ $ gunicorn rest_api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300
```
## Running Ngrok ##
### :: Set up a tunnel###

You will need to set up a HTTP tunneler to allow slack to communicate with your local server

```bash
# Navigate to ngrok installation folder and run the following.
$ ./ngrok http 3000
```

Copy the resultant https forwarding address and update the Slack App Event Subscriptions Request URL. 

eg: `https://6fdef00d53b6.ngrok.io/slack/events`


# To add additional documents
# Change file location and run
$ python3 add_doc.py
```

### Model Training ###




```bash
# Run the project
$ yarn start

# The server will initialize in the <http://localhost:3000>
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">{{YOUR_NAME}}</a>

&#xa0;

<a href="#top">Back to top</a>

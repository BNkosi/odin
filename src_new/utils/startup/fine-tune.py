"""
	Script to download, train and save model on local machine
	Author: BNkosi
"""

from haystack.reader.farm import FARMReader

# ## Create Training Data
# 
# There are two ways to generate training data
# 
# 1. **Annotation**: You can use the annotation tool(https://github.com/deepset-ai/haystack#labeling-tool) to label
#                    your data, i.e. highlighting answers to your questions in a document. The tool supports structuring
#                   your workflow with organizations, projects, and users. The labels can be exported in SQuAD format
#                    that is compatible for training with Haystack.
# 
# 2. **Feedback**:   For production systems, you can collect training data from direct user feedback via Haystack's
#                    REST API interface. This includes a customizable user feedback API for providing feedback on the
#                    answer returned by the API. The API provides feedback export endpoint to obtain the feedback data
#                    for fine-tuning your model further.
# 
# 
# ## Fine-tune your model
# 
# Once you have collected training data, you can fine-tune your base models.
# We initialize a reader as a base model and fine-tune it on our own custom dataset (should be in SQuAD-like format).
# We recommend using a base model that was trained on SQuAD or a similar QA dataset before to benefit from Transfer
# Learning effects.
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
# train_data = "data"
# train_data = "PATH/TO_YOUR/TRAIN_DATA" 
reader.train(data_dir="/home/bulelani/Desktop/odin/odin/src_new/data/training", train_filename="answers.json", use_gpu=False, n_epochs=1, save_dir="/home/bulelani/Desktop/odin/saved_models")

# Saving the model happens automatically at the end of training into the `save_dir` you specified
# However, you could also save a reader manually again via:
reader.save(directory="/home/bulelani/Desktop/odin/saved_models")

# If you want to load it at a later point, just do:
# new_reader = FARMReader(model_name_or_path="my_model")
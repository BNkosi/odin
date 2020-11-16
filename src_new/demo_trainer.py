from haystack.reader.farm import FARMReader

reader = FARMReader(model_name_or_path="distilbert-base-uncased-distilled-squad", use_gpu=False)
train_data = "/home/bulelani/Desktop/odin/odin/src_new/data/training"
# train_data = "PATH/TO_YOUR/TRAIN_DATA" 
reader.train(data_dir=train_data, train_filename="demo.json", use_gpu=False, n_epochs=100, save_dir="/home/bulelani/Desktop/odin/my_model")

# Saving the model happens automatically at the end of training into the `save_dir` you specified
# However, you could also save a reader manually again via:
reader.save(directory="/home/bulelani/Desktop/odin/my_model")
"""
function to read and question and label every document
"""
import os

document_path = "/home/bulelani/Desktop/odin/odin/src_new/data/documents"

for filename in os.listdir(document_path):
    print(filename)
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials
from PIL import Image
import requests
import io
import os
import re

ENDPOINT = os.environ["INPUT_ENDPOINT"]

# Replace with a valid key
training_key = os.environ["INPUT_TRAININGKEY"]
prediction_key = os.environ["INPUT_PREDICTIONKEY"]
prediction_resource_id = os.environ["INPUT_PREDICTIONRESOURCEID"]

publish_iteration_name = "classifyModel"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# Create a new project
print ("Creating project...")
project = trainer.create_project("My New Project")

tags = os.environ["INPUT_TAGS"]

#List of tag variables
tag_list = [] 

#Make tags in the new project
for tag in tags:
    tag_list.append(trainer.create_tag(project.id, tag))

# Make two tags in the new project
#hemlock_tag = trainer.create_tag(project.id, "Hemlock")
#cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")

base_image_url = "https://github.com/" + os.environ["GITHUB_REPOSITORY"] +"/raw/master/"

print("Adding images...")

image_list = []
num_tags = len(tags)

for i in range (num_tags):
    for image_num in range(1, 11):
        file_name = r"^.*\/([^\/]+\.jpg).*$"
        #file_name = "hemlock_{}.jpg".format(image_num)
        response = requests.get(base_image_url + "images/"+tag[i]+"/" + file_name)
        image_file = io.BytesIO(response.content)
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_file.read(), tag_ids=[tag_list[i].id]))

'''for image_num in range(1, 11):
    file_name = "japanese_cherry_{}.jpg".format(image_num)
    response = requests.get(base_image_url + "images/Japanese Cherry/" + file_name)
    image_file = io.BytesIO(response.content)
    image_list.append(ImageFileCreateEntry(name=file_name, contents=image_file.read(), tag_ids=[cherry_tag.id]))
'''

upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)

import time

print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    time.sleep(1)

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

response = requests.get(base_image_url + "Test/test_image.jpg")
image_file = io.BytesIO(response.content)
results = predictor.classify_image(
    project.id, publish_iteration_name, image_file.read())

    # Display the results.
for prediction in results.predictions:
    print("\t" + prediction.tag_name +
            ": {0:.2f}%".format(prediction.probability * 100))
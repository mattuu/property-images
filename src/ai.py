from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
from pathlib import Path
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import json
import jsonpickle

class ImageDescriptor:
    tags = array
    description = ''
    confidence = 0


# Add your Computer Vision subscription key to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

# Add your Computer Vision endpoint to your environment variables.
endpoint = 'https://property-room-locator.cognitiveservices.azure.com/'

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
analyze_url = endpoint + "vision/v3.0/analyze"

root = os.getcwd()
files = os.listdir('downloads')

for file_name in files:
    image_path = Path('downloads') / file_name

    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Description'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()
    # print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    json_file_name = file_name[0:-3] + 'json'
    json_file_path = Path('downloads') / json_file_name

    image_data = ImageDescriptor()
    image_data.tags = analysis['description']['tags']
    image_data.description = image_caption
    image_data.confidence = analysis['description']["captions"][0]["confidence"]

    json_string = jsonpickle.encode(image_data)
    with open(json_file_path, 'w') as outfile:
        outfile.writelines(json_string)
# print(json_string)



# with open(json_file_path, 'w') as outfile:
#     json.dump(image_data, outfile)

# image = Image.open(BytesIO(image_data))
# plt.imshow(image)
# plt.axis("off")
# _ = plt.title(image_caption, size="x-large", y=-0.1)
# plt.show()
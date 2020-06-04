import requests
from urllib.parse import urlparse
from pathlib import Path
import os
import shutil

dirs = os.listdir()
if ('downloads' in dirs):
    shutil.rmtree('downloads')

os.makedirs("downloads")

i = 1

while True:
    index = str(i)
    if(i < 10):
        index = '0' + index
    url = 'https://media.rightmove.co.uk/167k/166781/93080897/166781_RS0969_IMG_' + index + '_0000.jpg'

    o = urlparse(url)
    print('Downloading image from url: ' + url)

    fileName = o.path.split('/')[-1:][0]
    print('Captured file name: ' + fileName)

    r = requests.get(url, allow_redirects=True)

    if(r.status_code == 404):  
        break  

    root = os.getcwd()
    output_folder = Path(root) / 'downloads'
    file_to_write = output_folder / fileName
    open(file_to_write, 'wb').write(r.content)

    i += 1
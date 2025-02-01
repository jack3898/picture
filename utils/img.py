from PIL import Image
from io import BytesIO
import requests
import os
import random

def get_unsplash_image():
    url = "https://picsum.photos/800/480"

    response = requests.get(url)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return Image.new("RGB", (800, 480), "white")

def get_dir_image(dir):
    # If dir does not exist
    if not os.path.exists(dir):
        return Image.new("RGB", (800, 480), "white")

    # Get all files in dir
    files = os.listdir(dir)

    # filter out non-image files
    files = [f for f in files if (f.endswith(".png") or f.endswith(".jpg")) and not f.startswith(".")]

    # Pick a random file
    file = random.choice(files)

    # Open the file
    return Image.open(f"{dir}/{file}")

def get_file_image(path):
    file = os.path.expanduser(path)

    if not os.path.exists(file):
        return Image.new("RGB", (800, 480), "white")

    return Image.open(file)

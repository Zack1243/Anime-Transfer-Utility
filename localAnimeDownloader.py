import requests
import json
import os
import re
import shutil
import subprocess
import sys
import time
import yt_dlp
import zipfile
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter import Listbox
import os
import json
import shutil

INFOFILE = 'information.json'
global root
global frm

root = Tk()
frm = ttk.Frame(root, padding=10)

def filter_details(file, url, episode_file):

  # Get correct format options
  with open(file, 'r') as f:
    data = json.load(f)

    # Get info for details.json file
    transformed_data = {
        "title": data.get("title", ""),
        "author": data.get("uploader", ""),
        "artist": data.get("uploader", "can't re-use uploader I guess..."),
        "description": data.get("description", ""),
        "genre": data.get("tags", []),
        # Trying 3 for the status value to see if artist/uploader works
        "status": "2",
        "url": url,
    }

    # Get details for episode.json file
    episode_data = [{
              "episode_number": 1,
              "name": data.get("title", ""),
              "date_upload": data.get("upload_date", "")
    }]

    url_pattern = r'https?://\S+|www\.\S+'

    # Replace URLs with an empty string
    transformed_data["description"] = re.sub(url_pattern, '', transformed_data["description"])

    # Rewrite .json files WITH PROPER SYNTAX!!!
    with open(file, 'w') as f:
      json.dump(transformed_data, f, indent=4)

    with open(episode_file, 'w') as f:
      json.dump(episode_data, f, indent=4)
  return

def getTitle(url):
  try:
    print(url)
    
    # Get the video title
    result = subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "--no-playlist",
        "--skip-download",
        "--get-title",
        url
    ], capture_output=True, text=True, check=True)
    
    # Extract the title from the result
    title = result.stdout.strip()
    print(title)
    return title
  except subprocess.CalledProcessError as e:
    return ""


def download(my_text):
    try:
        # gather all the text in the textbox
        content = my_text.get("1.0", "end-1c")  # from line 1, char 0 to end (minus the auto newline)
        urls = [line for line in content.split("\n") if line.strip()]
        for url in urls:
            # Get the video title
            title = getTitle(url)

            # Make path to new directory including video's title
            path = os.path.join(os.getcwd(), title)

            print(f"Path of stored title: {path}")
            print(f"Title: {title}")
            ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
            subprocess.run([
                sys.executable, "-m", "yt_dlp",
                '--ffmpeg-location', ffmpeg_dir,
                '--convert-thumbnails', 'jpg',
                '--progress',
                '--no-playlist',
                '--write-thumbnail',
                '--embed-thumbnail',
                '--add-metadata',
                '--write-info-json',
                '--remux-video', 'mkv',
                '-f', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
                '-o', f'{path}\\%(title)s.%(ext)s',
                url
            ])
        return ""
        
    except subprocess.CalledProcessError as e:
        print("………………………………………………………………………………………………………")
        print(f"An error occurred: {e}")
        print(f"Failed to download url: {url}")
        print("………………………………………………………………………………………………………")
        with open('failed_downloads.txt', 'a') as f:
          f.write(url + '\n')
        return False
        

def downloadPage():
    my_text = Text(root, width=60, height=20)
    my_text.grid(pady=20)
    
    transferButton = Button(root, text="Download", command=lambda: download(my_text))
    transferButton.grid(pady=20)

def main():
    frm.grid()
    app_width = 600
    app_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    
    downloadPage()
    root.mainloop()


main()
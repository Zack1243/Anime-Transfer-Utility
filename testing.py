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
from PIL import Image
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
import os
import re
import subprocess
import time
from seleniumwire import webdriver
#pip install blinker==1.4 #in case the import webdriver doesn't work
from selenium.webdriver.firefox.options import Options
from mutagen.mp4 import MP4, MP4FreeForm

INFOFILE = 'information.json'
global root
global frm
global retrieveFrm
global retrieveRoot
global downloadRoot
global storeRoot
global storeFrm
global progressRoot
global progressFrm
global downloadFrm
global data
global labels
global progressLabels
global retrieveAnimeMap
global storeAnimeMap
global showNumSize
showNumSize = {}
#root = Tk()
#frm = ttk.Frame(root, padding=10)
downloadRoot = Tk()
downloadFrm = ttk.Frame(downloadRoot, padding=10)


retrieveAnimeMap = {}
storeAnimeMap = {}
data = {
            "PC Directory": "testing",
            "PC Capacity": "testing",
            "PC storage usage": "testing",
            "Phone storage usage": "testing",
            "Phone Directory": "testing",
            "Phone Capacity": "testing",
        }
labels = {
        "PC Directory": StringVar(),
        "PC Storage Usage": StringVar(),
        "Phone Directory": StringVar(),
        "Phone Storage Usage": StringVar(),
    }
progressLabels = {
    "Summary": StringVar(), # Transfering NUM files to DIRECTORY
    "Percentage": StringVar(), # NUM% complete
    "numFiles": StringVar(), # Transfering file NUM/TOTAL
    "Name": StringVar(), # Name: NAME
    "sizeTransfered": StringVar(), # Transfered NUM / TOTAL SIZE
}



## DOWNLOAD PAGE
def filter_details(file, url, episode_file):
    if os.path.exists(file):
        
        # Get correct format options
        with open(file, 'r', encoding="utf-8") as f:
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
    else:
        print(f"ERROR! Not a valid directory: {file}")
    return

def getTitle(url):
  try:
    print(f"Getting title for url: {url}")
    
    # Get the video title
    result = subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "--no-playlist",
        "--skip-download",
        '--impersonate', 'firefox',
        "--get-title",
        url
    ], capture_output=True, text=True, check=True)
    
    # Extract the title from the result
    title = result.stdout.strip()
    title = re.sub(r'[<>:"/\\|?*]', '_', title)
    print(f"Found title: {title}")
    return title
  except subprocess.CalledProcessError as e:
    return ""

def instantiate_checkpoint_files(urls):
    with open('urls.txt', 'w') as f:
        for url in urls:
            f.write(url)
        pass
    with open('completed.txt', 'w') as f:
      pass
    with open('failed_downloads.txt', 'w') as f:
      pass
    with open('downloaded already.txt', 'w') as f:
      pass

def attach_cover(mkv_file, cover_image):
    if os.path.exists(mkv_file):
        if os.path.exists(cover_image):
            base, ext = os.path.splitext(mkv_file)
            output_file = f"{base}.withcover{ext}"
            ffmpeg = r"D:\Programming\ffmpegDIr\ffmpeg.exe"
            if os.path.exists(ffmpeg):
                cmd = [
                    ffmpeg,
                    "-i", mkv_file,
                    "-i", cover_image,
                    "-map", "1",  # map all streams from mkv
                    "-map", "0",  # map the cover image
                    "-c", "copy",  # copy video/audio/subtitles
                    "-disposition:v:0", "attached_pic",  # mark second video stream as attached picture
                    output_file
                ]
                try:
                    subprocess.run(cmd, check=True)
                    print(f"Created new MKV with cover: {output_file}")
                    if os.path.exists(mkv_file):
                        os.remove(mkv_file)
                        os.rename(output_file, mkv_file)
                    return True
                except subprocess.CalledProcessError as e:
                    print("………………………………………………………………………………………………………")
                    print(f"An error occurred: {e}")
                    print(f"Something went wrong in the process of converting the thumbnail!")
                    return False
            else:
                print("......................................")
                print("......................................")
                print("ERROR: Invalid ffmpeg directory")
                print("......................................")
                print("......................................")
                return False
        else:
            print("......................................")
            print("......................................")
            print("ERROR: Invalid cover image directory!")
            print("......................................")
            print("......................................")
            return False
    else:
        print("......................................")
        print("......................................")
        print("ERROR: Invalid mkv directory!")
        print("......................................")
        print("......................................")
        return False
        
def getVideo(url, title):
    
    if not title:
        print("No title detected!")
        try:
            print(f"Url: {url}")
            print(f"Attempting to download through cyberdrop")
            # Create Download Directory
            title = "fuckshitbitch"
            output_dir = os.path.join(os.getcwd(), title)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            result = subprocess.run([
                "cyberdrop-dl", "--download",
                "--ignore-history",
                # Change the output directory
                "--download-folder", output_dir,
                "--exclude-images",
                #"-j",
                "--log-level", "10",
                url
                ], capture_output=True, text=True)
            if result.returncode != 0:
                print("Download failed:", result.stderr)
                print(result.stdout)
                #return False

            # look in the downloaded folder
            video_exts = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"}

            folder = output_dir
            print("starting the search!")
            for file in os.listdir(folder):
                print(f"Searching within the folder: {folder}")
                print(f"Name of the file: {file}")
                filePath = os.path.join(folder, file)
                if os.path.isdir(filePath):
                    print(f"this is the file shown to be a directory: {file}")
                    folder = os.path.join(folder, file)
                    for video in os.listdir(folder):
                        print(f"found thing {video}")
                        if os.path.splitext(video)[1].lower() in video_exts:
                            title = os.path.splitext(video)[0]  # filename without extension
                            print("Found video:", video, "| Title:", title)
                            newDir = os.path.join(os.getcwd(), title)
                            folder = os.path.join(folder, video)
                            convVideo = MP4(folder)
                            convVideo["----:com.apple.iTunes:url"] = [MP4FreeForm(url.encode("utf-8"))]
                            convVideo.save()
                            os.mkdir(newDir)
                            shutil.move(folder, newDir)
                            return True

            if result.returncode == 0:
                print("Download succeeded... by cyberdrop!")
                return True
            else:
                print("Download failed:", result.stderr)
                return False
        except FileNotFoundError:
            print("Failed to download via cyberdrop!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to download: {e}")
            return False
    else:
        try:
            # Make path to new directory including video's title
            path = os.path.join(os.getcwd(), title)
            print(f"Path of stored title: {path}")
            print(f"Title: {title}")
            ffmpeg_dir = r"D:\Programming\ffmpegDIr"
            
            if os.path.exists(ffmpeg_dir):
                print("found the ffmpeg Directory!")
            else:
                print("404 ERROR ffmpeg not found!")
                
            #if url.contains("bunkr", "")
                
                
            subprocess.run([
                sys.executable, "-m", "yt_dlp",
                '--ffmpeg-location', ffmpeg_dir,
                '--progress',
                '--no-playlist',
                '--remux-video', 'mp4',
                '--convert-thumbnails', 'jpg',
                '--impersonate', 'firefox',
                '--write-thumbnail',
                '--embed-thumbnail',
                '--embed-metadata',
                '--write-info-json',
                '--embed-chapters',
                #'--embed subs',
                '-f', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
                '-o', f'{path}\\{title}.%(ext)s',
                '-o', f'thumbnail:{path}\\cover.%(ext)s',
                '-o', f'infojson:{path}\\details.%(ext)s',
                url
            ])
            if os.path.exists(path):
                # Create empty .nomedia file
                os.chdir(path)
                with open('.nomedia', 'w') as makefile:
                    pass
                os.chdir('..')
    
                # Change info.json file to be "details.json"
                if os.path.exists(f'{path}/details.info.json'):
                    os.rename(f'{path}/details.info.json', f'{path}/details.json')
                    filter_details(f'{path}/details.json', url, f'{path}/episode.json')
                else:
                    print("No info file found.")
                return True
            else:
                return False
            
        except subprocess.CalledProcessError as e:
            print("………………………………………………………………………………………………………")
            print(f"An error occurred: {e}")
            print(f"Failed to download url: {url}")
            print("………………………………………………………………………………………………………")
            with open('failed_downloads.txt', 'a') as f:
              f.write(url + '\n')
            return False

def download(urls):
    for url in urls:
        # Get the video title
        title = getTitle(url)
        if getVideo(url, title):
            print("Downloaded the video!")
        else:
            print(f"Failed to download the video: {title}")
            print('SKIPPED: ' + title + '.zip')

url = [

    ]
download(url)
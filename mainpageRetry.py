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
import subprocess
import sys
import math
import re
import requests
import time
import yt_dlp
import zipfile
from PIL import Image
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
root = Tk()
frm = ttk.Frame(root, padding=10)
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

## GENERAL FUNCTIONS
# Set the Phone Directory
def setPCDirectory():
    
    # Prompt user to select file location
    folder_path = filedialog.askdirectory()
    
    # Update JSON and data with file location
    data["PC Directory"] = folder_path

        
    labels["PC Directory"].set(f"{data['PC Directory']}")


    with open(INFOFILE, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Set the Phone Directory
def setPhoneDirectory():
    
    # Prompt user to select file location
    folder_path = filedialog.askdirectory()
    # Update JSON and data with file location
    data["Phone Directory"] = folder_path

    labels["Phone Directory"].set(f"{data['Phone Directory']}")

    with open(INFOFILE, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# get the size of a title directory
def getSize(titleDir):
    total_size = 0
    # Walk through each folder, subfolder, and files
    for dirpath, dirnames, filenames in os.walk(titleDir):
        for filename in filenames:
            # Get the full file path
            file_path = os.path.join(dirpath, filename)
            # Add the file size to the total size
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

# Stores the data of the titles
def storeData(title, src):
    global showNumSize
    size = getSize(src)
    showNumSize[title] = size

# Returns the total size of all items in listbox
def getTotalSize(my_listbox):
    global showNumSize
    totalSize = 0
    if my_listbox.curselection():
        for index in my_listbox.curselection():
            title = my_listbox.get(index)
            totalSize = totalSize + showNumSize[title]
    return totalSize

def convert(size):
    if size == 0:
        return f"0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)

    return f"{s} {size_name[i]}"

## STORE PAGE
def gridStoreListbox(storeFrm):
    my_scrollbar = Scrollbar(storeFrm, orient=VERTICAL)
    my_listbox = Listbox(storeFrm, width=50, yscrollcommand=my_scrollbar.set, selectmode=MULTIPLE)
    my_scrollbar.config(command=my_listbox.yview)
    my_listbox.grid(row=0, column=0, pady=15)
    my_scrollbar.grid(row=0, column=1, sticky='ns')
    for show in storeAnimeMap:
        my_listbox.insert(0, show)
    return my_listbox

def getStoreShowMap():
    global storeAnimeMap

    # Get PC Directory
    current_dir = data["Phone Directory"]
    # Get List of Directories in PC Directory
    directories = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    
    downloads = os.path.join(current_dir, "downloads")
    for title in directories:
        if title == "downloads":
            siteDirs = [d for d in os.listdir(downloads) if os.path.isdir(os.path.join(downloads, d))]
            for site in siteDirs:
                subDirs = [d for d in os.listdir(os.path.join(downloads, site)) if os.path.isdir(os.path.join(downloads, site))]
                if len(subDirs) > 0:
                    for title in subDirs:
                        storeAnimeMap[title] = str(f"{downloads}/{site}/{title}")
        elif title == "localanime":
            localAnimeDir = [d for d in os.listdir(os.path.join(current_dir, title)) if os.path.isdir(os.path.join(current_dir, title))]
            for title in localAnimeDir:
                storeAnimeMap[title] = str(f"{current_dir}/localanime/{title}")
        
def storeShows(my_listbox, progressBar):
    global storeAnimeMap
    numFilesTransfered = 0
    percentage = 0
    sizeTransfered = 0
    dst = data['PC Directory']
    dst = dst.replace("/", "\\")
    
    
    if my_listbox.curselection():
        for index in my_listbox.curselection():
            title = my_listbox.get(index)
            storeData(title, storeAnimeMap[title])
        totalSize = getTotalSize(my_listbox)
        totalFiles = len(my_listbox.curselection())
        
        
        progressLabels["Name"].set(f"Storing: ")
        progressLabels["Percentage"].set(f"{percentage}% Completed")
        progressLabels['numFiles'].set(f"Stored {numFilesTransfered} / {totalFiles} items")
        progressLabels["sizeTransfered"].set(f"Stored 0b / {convert(totalSize)}")
        
        for index in my_listbox.curselection():
            
            title = my_listbox.get(index)
            titleDir = storeAnimeMap[title]
            titleSize = showNumSize[title]
            progressLabels["Name"].set(f"Storing: {title}")
            
            print(f"Beginning to store title: {title}")
            print(f"Directory of title: {storeAnimeMap[title]}")
            
            # The title is in the localanime directory
            if titleDir.split('/')[-2] == "localanime":
                dst = os.path.join(dst, storeAnimeMap[title].split('/')[-1])
            # The title is in the downloads directory
            else:
                dst = os.path.join(dst, "downloads", storeAnimeMap[title].split('/')[-2], storeAnimeMap[title].split('/')[-1])
            
            shutil.move(titleDir, dst)
            
            sizeTransfered = sizeTransfered + titleSize
            percentage = (sizeTransfered / totalSize) * 100
            numFilesTransfered = numFilesTransfered + 1
            
            progressLabels["sizeTransfered"].set(f"Stored {convert(sizeTransfered)} / {convert(totalSize)}")
            progressLabels["Percentage"].set(f"{percentage}% Completed")
            progressLabels['numFiles'].set(f"Stored {numFilesTransfered} / {totalFiles} items")
            progressBar['value'] = percentage
        for index in reversed(my_listbox.curselection()):
            title = my_listbox.get(index)
            # Remove from the dictionary
            if title in storeAnimeMap:
                del storeAnimeMap[title]
            my_listbox.delete(index)
        my_listbox.delete(ANCHOR)

def populateStorePage(storeFrm, storeRoot):
    
    # Have to make a progress Bar
    myProgressBar = ttk.Progressbar(storeFrm, orient="horizontal", length=300, mode='determinate')
    
    # Get a Dictionary of shows
    getStoreShowMap()

    # Make a listbox of shows
    my_listbox = gridStoreListbox(storeFrm)
    
    
    
    # Button to retrieve shows
    storeButton = ttk.Button(storeFrm, text="Store", command=lambda: storeShows(my_listbox, myProgressBar))
    storeButton.grid(row=1, column=0)
    
    # Separator for the progress bar
    separator = ttk.Separator(storeFrm, orient="horizontal")
    separator.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
    
    sizeTransferedLabel = ttk.Label(storeFrm, textvariable=progressLabels["numFiles"])
    sizeTransferedLabel.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
    
    # []% Complete
    percentLabel = ttk.Label(storeFrm, textvariable=progressLabels["Percentage"])
    percentLabel.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
    
    
    # Name: [Filename]
    filenameLabel = ttk.Label(storeFrm, textvariable=progressLabels["Name"])
    filenameLabel.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
    
    # Stored 0b / 3.14 Gb
    storeSizeLabel = ttk.Label(storeFrm, textvariable=progressLabels["sizeTransfered"])
    storeSizeLabel.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
    
    #Progress Bar
    myProgressBar.grid(row=7, column=0)

def storePage():
    global progressLabels
    storeRoot = Toplevel(root)
    storeFrm = ttk.Frame(storeRoot, padding=10)
    storeFrm.grid()
    app_width = 600
    app_height = 500
    screen_width = storeRoot.winfo_screenwidth()
    screen_height = storeRoot.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    storeRoot.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    
    populateStorePage(storeFrm, storeRoot)
    storeRoot.mainloop()

## RETRIEVE PAGE 
# Retrieve Shows Button Function
def retrieveShows(my_listbox, progressBar):
    global retrieveAnimeMap
    numFilesTransfered = 0
    percentage = 0
    sizeTransfered = 0
    dst = data['Phone Directory']
    dst = dst.replace("/", "\\")
    
    
    if my_listbox.curselection():
        for index in my_listbox.curselection():
            title = my_listbox.get(index)
            storeData(title, retrieveAnimeMap[title])
        totalSize = getTotalSize(my_listbox)
        totalFiles = len(my_listbox.curselection())
        
        
        progressLabels["Name"].set(f"Retrieving: ")
        progressLabels["Percentage"].set(f"{percentage}% Completed")
        progressLabels['numFiles'].set(f"Retrieved {numFilesTransfered} / {totalFiles} items")
        progressLabels["sizeTransfered"].set(f"Retrieving 0b / {convert(totalSize)}")
        
        
        for index in my_listbox.curselection():
            title = my_listbox.get(index)
            titleDir = retrieveAnimeMap[title]
            titleSize = showNumSize[title]
            progressLabels["Name"].set(f"Storing: {title}")
            
            
            if titleDir.split('/')[-2] == data['PC Directory'].split('/')[-1]:
                dst = os.path.join(dst, "localanime", retrieveAnimeMap[title].split('/')[-1])
            # we will assume our title is in a source within the downloads folder
            else:
                dst = os.path.join(dst, "downloads", retrieveAnimeMap[title].split('/')[-2], retrieveAnimeMap[title].split('/')[-1])
            
            shutil.move(titleDir, dst)

            sizeTransfered = sizeTransfered + titleSize
            percentage = (sizeTransfered / totalSize) * 100
            numFilesTransfered = numFilesTransfered + 1
            
            progressLabels["sizeTransfered"].set(f"Retrieved {convert(sizeTransfered)} / {convert(totalSize)}")
            progressLabels["Percentage"].set(f"{percentage}% Completed")
            progressLabels['numFiles'].set(f"Retrieved {numFilesTransfered} / {totalFiles} items")
            progressBar['value'] = percentage
            
        for index in reversed(my_listbox.curselection()):
            title = my_listbox.get(index)
            # Remove from the dictionary
            if title in retrieveAnimeMap:
                del retrieveAnimeMap[title]
            my_listbox.delete(index)
        my_listbox.delete(ANCHOR)

# Get a Dictionaryh of [show: Directory]
def getRetrieveShowMap():
    global retrieveAnimeMap

    # Get PC Directory
    current_dir = data["PC Directory"]
    # Get List of Directories in PC Directory
    directories = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    
    for title in directories:
        
        # Add all the localanime
        if title != "downloads":
            retrieveAnimeMap[title] = str(f"{current_dir}/{title}")
        
        # Add all the anime from sites
        elif title == "downloads":
            siteDirectories = [d for d in os.listdir(str(f"{current_dir}/{title}")) if os.path.isdir(os.path.join(str(f"{current_dir}/{title}"), d))]
            for site in siteDirectories:
                titles = [d for d in os.listdir(str(f"{current_dir}/downloads/{site}")) if os.path.isdir(os.path.join(str(f"{current_dir}/downloads/{site}"), d))]
                for title in titles:
                    retrieveAnimeMap[title] = str(f"{current_dir}/downloads/{site}/{title}")

# Make a Listbox for the retrievePage
def gridListbox(retrieveFrm):
    global retrieveAnimeMap
    my_scrollbar = Scrollbar(retrieveFrm, orient=VERTICAL)
    my_listbox = Listbox(retrieveFrm, width=50, yscrollcommand=my_scrollbar.set, selectmode=MULTIPLE)
    my_scrollbar.config(command=my_listbox.yview)
    my_listbox.grid(row=0, column=0, pady=15)
    my_scrollbar.grid(row=0, column=1, sticky='ns')
    for show in retrieveAnimeMap:
        my_listbox.insert(0, show)
    return my_listbox

def populateRetrievePage(retrieveFrm, retrieveRoot):
    myProgressBar = ttk.Progressbar(retrieveFrm, orient="horizontal", length=300, mode='determinate')
    
    # Get a Dictionary of shows
    getRetrieveShowMap()

    # Make a listbox of shows
    my_listbox = gridListbox(retrieveFrm)
    
    # Button to retrieve shows
    retrieveButton = ttk.Button(retrieveFrm, text="Retrieve", command=lambda: retrieveShows(my_listbox))
    retrieveButton.grid(row=1, column=0)
    
        
    # Have to make a progress Bar
    myProgressBar = ttk.Progressbar(retrieveFrm, orient="horizontal", length=300, mode='determinate')
    
    
    # Button to retrieve shows
    storeButton = ttk.Button(retrieveFrm, text="Store", command=lambda: retrieveShows(my_listbox, myProgressBar))
    storeButton.grid(row=1, column=0)
    
    # Separator for the progress bar
    separator = ttk.Separator(retrieveFrm, orient="horizontal")
    separator.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
    
    sizeTransferedLabel = ttk.Label(retrieveFrm, textvariable=progressLabels["numFiles"])
    sizeTransferedLabel.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
    
    # []% Complete
    percentLabel = ttk.Label(retrieveFrm, textvariable=progressLabels["Percentage"])
    percentLabel.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
    
    
    # Name: [Filename]
    filenameLabel = ttk.Label(retrieveFrm, textvariable=progressLabels["Name"])
    filenameLabel.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
    
    # Stored 0b / 3.14 Gb
    storeSizeLabel = ttk.Label(retrieveFrm, textvariable=progressLabels["sizeTransfered"])
    storeSizeLabel.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
    
    #Progress Bar
    myProgressBar.grid(row=7, column=0)

# Open the Retrieve Page
def retrievePage():
    retrieveRoot = Toplevel(root)
    retrieveFrm = ttk.Frame(retrieveRoot, padding=10)
    retrieveFrm.grid()
    app_width = 600
    app_height = 500
    screen_width = retrieveRoot.winfo_screenwidth()
    screen_height = retrieveRoot.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    retrieveRoot.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    populateRetrievePage(retrieveFrm, retrieveRoot)
    retrieveRoot.mainloop()

## DOWNLOAD PAGE
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
        '--impersonate', 'firefox',
        "--get-title",
        url
    ], capture_output=True, text=True, check=True)
    
    # Extract the title from the result
    title = result.stdout.strip()
    print(title)
    return title
  except subprocess.CalledProcessError as e:
    return ""

def instantiate_checkpoint_files(urls):
    with open('urls.txt', 'w') as f:
      f.write(urls)
      pass
    with open('completed.txt', 'w') as f:
      pass
    with open('failed_downloads.txt', 'w') as f:
      pass
    with open('downloaded already.txt', 'w') as f:
      pass

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

def download(my_text):

        content = my_text.get("1.0", "end-1c")  # from line 1, char 0 to end (minus the auto newline)
        urls = [line for line in content.split("\n") if line.strip()]

        # Check if the infofiles have been instantiated
        if not os.path.exists('urls.txt'):
            instantiate_checkpoint_files(urls)

        # Read Checkpoint files
        with open('completed.txt', 'r') as f:
          completed = f.read().splitlines()[:]
        with open('failed_downloads.txt', 'r') as f:
          failed = f.read().splitlines()[:]
        with open('downloaded already.txt', 'r') as f:
          zipped = f.read().splitlines()[:]
    
        for url in urls:
            # Get the video title
            title = getTitle(url)
            if url not in completed and url not in failed and title + '.zip' not in zipped:
              if getVideo(url, title):
                title = getTitle(url)
                with open('completed.txt', 'a') as f:
                  f.write(url + '\n')
            else:
              print('SKIPPED: ' + title + '.zip')
  
def populateDownloadPage(downloadFrm, downloadRoot):
    my_text = Text(downloadRoot, width=60, height=20)
    my_text.grid(pady=20)
    
    transferButton = Button(downloadRoot, text="Download", command=lambda: download(my_text))
    transferButton.grid(pady=20)
    
    # Separator
    
    # Percentage button
    
    # Total size of the download
    
    # If it has failed or not 
    
def downloadPage():
    downloadRoot = Toplevel(root)
    downloadFrm = ttk.Frame(downloadRoot, padding=10)
    downloadFrm.grid()
    app_width = 600
    app_height = 500
    screen_width = downloadRoot.winfo_screenwidth()
    screen_height = downloadRoot.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    downloadRoot.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    populateDownloadPage(downloadFrm, downloadRoot)
    downloadRoot.mainloop()

## MAIN PAGE
def populateMainpage():
    # Line 1
    welcomeLabel = ttk.Label(frm, text="Welcome to the Aniyomi GUI!")
    welcomeLabel.grid(row=0, column=0)
    
    # Line 2
    # Column 0: Set Phone Directory Label
    phoneDirectoryLabel = ttk.Label(frm, text="Set Phone Directory")
    phoneDirectoryLabel.grid(row=1, column=0)
    
    # Column 1: Set Phone Directory Button
    phoneDirectoryButton = ttk.Button(frm, text="...", command=lambda: setPhoneDirectory())
    phoneDirectoryButton.grid(row=1, column=1)
    
    # Column 2: Phone Directory
    phoneDirectoryVariableLabel = ttk.Label(frm, textvariable=labels["Phone Directory"])
    phoneDirectoryVariableLabel.grid(row=1, column=2)
    
    
    # Line 3
    # Column 0: Set PC Directory Label
    pcDirectoryLabel = ttk.Label(frm, text="Set PC Directory")
    pcDirectoryLabel.grid(row=2, column=0)
    
    # Column 1: Set PC Directory Button
    pcDirectoryButton = ttk.Button(frm, text="...", command=lambda: setPCDirectory())
    pcDirectoryButton.grid(row=2, column=1)
    
    # Column 2: PC Directory
    pcDirectoryVariableLabel = ttk.Label(frm, textvariable=labels["PC Directory"])
    pcDirectoryVariableLabel.grid(row=2, column=2)
    
    # Line 4
    # Column 0: Retrieve Button
    retrieveButton = ttk.Button(frm, text="Retrieve", command=lambda: retrievePage())
    retrieveButton.grid(row=3, column=0)
    
    # Column 1: Store Button
    storeButton = ttk.Button(frm, text="Store", command=lambda: storePage())
    storeButton.grid(row=3, column=1)
    
    # Column 2: Download Button
    downloadButton = ttk.Button(frm, text="Download", command=lambda: downloadPage())
    downloadButton.grid(row=3, column=2)
     
# Make the mainpage
def main():
    global data
    global labels
    frm.grid()
    app_width = 600
    app_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    # Check that Infofile has been instantiated
    if os.path.exists(INFOFILE):
        with open(INFOFILE, 'r') as json_file:
            dataValues = json.load(json_file)
            data["PC Directory"] = dataValues["PC Directory"]
            data["PC Capacity"] = dataValues["PC Capacity"]
            data["PC storage usage"] = dataValues["PC storage usage"]
            data["Phone Directory"] = dataValues["Phone Directory"]
            data["Phone Capacity"] = dataValues["Phone Capacity"]
            data["Phone storage usage"] = dataValues["Phone storage usage"]
            labels["Phone Directory"].set(f"{dataValues['Phone Directory']}")
            labels["PC Directory"].set(f"{dataValues['PC Directory']}")
            
    # Cannot find INFOFILE. Create and populate with random data
    else:
        labels = {
            "PC Directory": "testing",
            "PC Capacity": "testing",
            "PC storage usage": "testing",
            "Phone storage usage": "testing",
            "Phone Directory": "testing",
            "Phone Capacity": "testing",
        }
        with open(INFOFILE, 'w') as json_file:
            json.dump(labels, json_file, indent=4)
        data = labels
            
    if not os.path.exists(INFOFILE):
        print("ERROR: Cannot make the INFOFILE")
    
    populateMainpage()
    root.mainloop()
main()
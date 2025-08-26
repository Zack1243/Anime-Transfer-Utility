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
import re

INFOFILE = 'information.json'
global root
global frm
global retrieveFrm
global retrieveRoot
global downloadRoot
global storeRoot
global storeFrm
global downloadFrm
global data
global labels
global retrieveAnimeMap
global storeAnimeMap
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


# Set the Phone Directory
def setPCDirectory():
    
    # Prompt user to select file location
    folder_path = filedialog.askdirectory()
    
    # Update JSON and data with file location
    data["PC Directory"] = folder_path
    with open(INFOFILE, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Set the Phone Directory
def setPhoneDirectory():
    
    # Prompt user to select file location
    folder_path = filedialog.askdirectory()
    # Update JSON and data with file location
    data["Phone Directory"] = folder_path
    with open(INFOFILE, 'w') as json_file:
        json.dump(data, json_file, indent=4)

## STORE PAGE
def gridStoreListbox(storeFrm):
    my_scrollbar = Scrollbar(storeFrm, orient=VERTICAL)
    my_listbox = Listbox(storeFrm, width=50, yscrollcommand=my_scrollbar.set, selectmode=MULTIPLE)
    my_scrollbar.config(command=my_listbox.yview)
    my_listbox.grid(pady=15)
    my_listbox.grid(row=0, column=0)
    my_scrollbar.grid(row=0, column=1, sticky='ns')
    for show in storeAnimeMap:
        my_listbox.insert(0, show)
    my_listbox.grid()
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
    
def storeShows(my_listbox):
    dst = data['PC Directory']
    dst = dst.replace("/", "\\")
    if my_listbox.curselection():
        for index in my_listbox.curselection():
            title = my_listbox.get(index)
            titleDir = storeAnimeMap[title]
            print(f"Beginning to store title: {title}")
            print(f"Directory of title: {storeAnimeMap[title]}")
            
            # The title is in the localanime directory
            if titleDir.split('/')[-2] == "localanime":
                print("This print condition should trigger for anything within localanime")
                # PC Directory -> downloads -> source -> title
                dst = os.path.join(dst, storeAnimeMap[title].split('/')[-1])
            # we will assume our title is in a source within the downloads folder
            
            
            # The title is in the downloads directory
            else:
                # We found out that its a local download can directly move
                dst = os.path.join(dst, "downloads", storeAnimeMap[title].split('/')[-2], storeAnimeMap[title].split('/')[-1])
            shutil.move(titleDir, dst)
            #os.move src to dst
            
        for index in reversed(my_listbox.curselection()):
            title = my_listbox.get(index)
            # Remove from the dictionary
            if title in storeAnimeMap:
                del storeAnimeMap[title]
            my_listbox.delete(index)
        my_listbox.delete(ANCHOR)

def populateStorePage(storeFrm, storeRoot):
    
    # Get a Dictionary of shows
    getStoreShowMap()

    # Make a listbox of shows
    my_listbox = gridStoreListbox(storeFrm)
    
    # Button to retrieve shows
    storeButton = ttk.Button(storeFrm, text="Store", command=lambda: storeShows(my_listbox))
    storeButton.grid(row=1, column=0)

def storePage():
    storeRoot = Tk()
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
def retrieveShows(my_listbox):
    dst = data['Phone Directory']
    dst = dst.replace("/", "\\")
    if my_listbox.curselection():
        for index in my_listbox.curselection():
            title = my_listbox.get(index)
            titleDir = retrieveAnimeMap[title]
            print("...............................................")
            print("...............................................")
            print("INFO")
            print(f"TITLE: {title}")
            print(f"DIRECTORY: {titleDir}")    
            if titleDir.split('/')[-2] == data['PC Directory'].split('/')[-1]:
                print(f"{title} is within the base PC Directory (Will be transfered to localanime)")
                # PC Directory -> downloads -> source -> title
                dst = os.path.join(dst, "localanime", retrieveAnimeMap[title].split('/')[-1])
            # we will assume our title is in a source within the downloads folder
            
            else:
                print(f"{title} was found within downloads/{retrieveAnimeMap[title].split('/')[-2]}")
                
                # We found out that its a local download can directly move
                dst = os.path.join(dst, "downloads", retrieveAnimeMap[title].split('/')[-2], retrieveAnimeMap[title].split('/')[-1])
            titleDir = os.path.normpath(titleDir)
            print(f"Transfering {titleDir} to {dst}...")
            if os.path.exists(titleDir):
                shutil.move(titleDir, dst)
                if os.path.exists(dst):
                    print(f"{title} was successfully transfered!")
                else:
                    print(f"{title} has failed to transfer!")
            else:
                print(f"src dir {titleDir} does not exist!")
            
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
    my_listbox.grid(pady=15)
    my_listbox.grid(row=0, column=0)
    my_scrollbar.grid(row=0, column=1, sticky='ns')
    for show in retrieveAnimeMap:
        my_listbox.insert(0, show)
    my_listbox.grid()
    return my_listbox


def populateRetrievePage(retrieveFrm, retrieveRoot):
    
    # Get a Dictionary of shows
    getRetrieveShowMap()

    # Make a listbox of shows
    my_listbox = gridListbox(retrieveFrm)
    
    # Button to retrieve shows
    retrieveButton = ttk.Button(retrieveFrm, text="Retrieve", command=lambda: retrieveShows(my_listbox))
    retrieveButton.grid(row=1, column=0)

# Open the Retrieve Page
def retrievePage():
    retrieveRoot = Tk()
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
    try:
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
        
        # Rename cover image to "cover.jpg"
        if os.path.exists(f'{path}/{title}.jpg'):
            os.rename(f'{path}/{title}.jpg', f'{path}/cover.jpg')
        else:
            print("No cover image found.")
        
        # Create empty .nomedia file
        os.chdir(path)
        with open('.nomedia', 'w') as makefile:
            pass
        os.chdir('..')
        
        # Change info.json file to be "details.json"
        if os.path.exists(f'{path}/{title}.info.json'):
            os.rename(f'{path}/{title}.info.json', f'{path}/details.json')
            filter_details(f'{path}/details.json', url, f'{path}/episode.json')
            return True
        else:
            print("No info file found.")
            return title
        
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
    
def downloadPage():
    downloadRoot = Tk()
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
# Start the panel of tkinter
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
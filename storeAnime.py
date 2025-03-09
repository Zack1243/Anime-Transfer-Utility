from tkinter import *
#from functions import Functions
#from popups import Popups
import json
import os
import shutil

INFOFILE = 'information.json'
VIDEO_EXTENSIONS = {".mov", ".mkv", ".mp4"}

class StoreAnime:
    def __init__(self, infofile):
        self.infofile = infofile
    
    def operations(self, root, frm, labels, obj, func_but, data):
        if data:
            # Get the directory of the library
            phoneDir = data["Phone Directory"]
            
            # Get the localanime folder
            localAnimeDir = os.path.join(str(phoneDir), "localanime").replace("/", "\\")
            
            # Get the downloads folder
            downloadsDir = os.path.join(str(phoneDir), "downloads").replace("/", "\\")
            
            # Get list of show directories in localAnime
            localAnimeDirs = [os.path.join(str(localAnimeDir), item).replace("/", "\\") for item in os.listdir(localAnimeDir)]
            
            # Get list of sources in downloads
            downloadDirs = [os.path.join(str(downloadsDir), item).replace("/", "\\") for item in os.listdir(downloadsDir)]
            
            # TODO: Delete this print statement that shows the contents of downloadDirs
            print("........................................................")
            print("Printing each source directory in downloadDirs")
            for show in downloadDirs:
                print(downloadDirs)
            print("........................................................")
            
            # Need list of sources
            # need list of shows within each source
        
            # Invalid shows
            empty_folders = []

            # Check if directories are valid and have files to play
            for show in localAnimeDirs:
                if not os.path.isdir(show):
                    empty_folders.append(show)
                    continue
                found = any(file.endswith(VIDEO_EXTENSIONS) for _, _, files in os.walk(show) for file in files)
                if not found:
                    empty_folders.append(show)
                    continue
            
            # Remove shows from list of folders
            for show in empty_folders:
                localAnimeDirs.remove(show)


            # Isolate the valid titles
            titles = [show.split('\\')[-1] for show in localAnimeDirs]


            # Get the destination directory
            pc_directory = data["PC Directory"]

            store_size = 0
            store_progress = 0

            # Check if the destination directory is valid
            if not pc_directory:
                print(f"{pc_directory} is invalid! Please choose another directory")
            else:
                for show in localAnimeDirs:
                    store_size = store_size + os.path.getsize(show)
                for show in localAnimeDirs:
                    dst = os.path.join(pc_directory, show.split('\\')[-1])
                    shutil.move(show, dst)
                    store_progress = store_progress + os.path.getsize(show)


            for title in titles:
                my_listbox.insert(END, title)
    
    
    
    def main(self, obj, func_but, data, labels):
        root, frm, labels = obj.rootInit()
        self.operations(root, frm, labels obj, func_but, data)
import json
import math
import os
from popups import Popups
import shutil
#from storeAnime import StoreAnime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox

INFOFILE = 'information.json'
VIDEO_EXTENSIONS = {".mov", ".mkv", ".mp4"}

class Button_functions:
    def __init__(self, infofile):
        self.infofile = infofile
        
        
    def confirmInfofileInstantiation(self, file):
        """summary_ Checks if INFOFILE has been instantiated

        Args:
            file (file): File seeking to be instantiated
        Returns:
            data (data): Contents of the file
        """
        with open(file, 'r') as json_file:
            data = json.load(json_file)
        return data

    def setPhoneDirectory(self, obj, labels):
        """
        Prompts the user to select a valid phone directory.
        Takes in a phone directory label in order to change the label to match the newly chosen directory
        """
        obj.checkInfofileInit()

        # Placeholder folder_path (if you named your directory this exact sequence of keys, blame the universe)
        folder_path = "woqpagwewsegraberiknh"

        i = 0

        # Set the folder path to an existing directory
        while os.path.exists(folder_path) or i < 3:

            # Try again for a new phone directory
            if i > 0:
                print(f"Phone directory not valid. Attempts remaining ({3-i}/3)")

            # Have the user choose a phone directory
            folder_path = filedialog.askdirectory()
            
            if folder_path == "":
                print("User has refused to select a directory")
                break
            # Check if folder_path exists
            if os.path.exists(folder_path):


                # Read in data from INFOFILE
                with open(INFOFILE, 'r') as json_file:
                    data = json.load(json_file)

                # Update Phone Directory in INFOFILE
                data["Phone Directory"] = folder_path

                # Write updated data to json_file
                with open(INFOFILE, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                print(f"{INFOFILE} has been updated with the new Phone Directory: {folder_path}")
                # Write the phone directory into the INFOFILE
                with open(INFOFILE, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                labels["Phone Directory"].set(f"{folder_path}")
                labels["Phone Storage Usage"].set("Phone " + obj.getStorageUsage(data["Phone Directory"]))
                break
            i = i + 1
            print(f"User has failed to select a valid Phone directory!")

    def setPCDirectory(self, function_obj, labels):
        function_obj.checkInfofileInit()

        # Placeholder folder_path (if you named your directory this exact sequence of keys, blame the universe)
        folder_path = "woqpagwewsegraberiknh"

        i = 0

        # Set the folder path to an existing directory
        while os.path.exists(folder_path) or i < 4:

            # Try again for a new phone directory
            if i > 0:
                print(f"PC directory not valid. Attempts remaining ({3-i}/3)")

            # Have the user choose a phone directory
            folder_path = filedialog.askdirectory()
            if folder_path == "":
                print("User has refused to select a directory")
                break
            # Check if folder_path exists
            if os.path.exists(folder_path):

                # Read in data from INFOFILE
                with open(INFOFILE, 'r') as json_file:
                    data = json.load(json_file)

                # Update Phone Directory in INFOFILE
                data["PC Directory"] = folder_path

                # Write updated data to json_file
                with open(INFOFILE, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                print(f"{INFOFILE} has been updated with the new PC Directory: {folder_path}")

                # Write the phone directory into the INFOFILE
                with open(INFOFILE, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                labels["PC Directory"].set(f"{folder_path}")
                
                # Update the storage usage
                labels["PC Storage Usage"].set("PC " + function_obj.getStorageUsage(data["PC Directory"]))
                break
            i = i + 1
            print(f"User has failed to select a valid PC directory!")

    def storeAnime(self, function_obj, func_but, frm, labels, data, *args):
        data = function_obj.getInfofileData()
        pops = Popups(INFOFILE)
        
        # Check if the pc directory is valid
        if not os.path.exists(data['PC Directory']):
            if pops.invalidPCDirectory(frm):
                self.setPCDirectory(function_obj, labels)

        # Check if the phone directory is valid
        elif not os.path.exists(data['Phone Directory']):
            if pops.invalidPhoneDirectory(frm):
                self.setPhoneDirectory(function_obj, labels)
            
        # TODO: Include this
        #elif not function_obj.validAniyomiDirectory(pops, data['Phone Directory']):
           # pass
        
        elif not os.path.exists(os.path.join(str(data["Phone Directory"]), "localanime").replace("/", "\\")):
            if pops.noLocalAnimeDetected(frm):
                self.setPhoneDirectory(function_obj, labels)

        elif not os.path.exists(os.path.join(str(data["Phone Directory"]), "downloads").replace("/", "\\")):
            if pops.noDownloadsDetected(frm):
                self.setPhoneDirectory(function_obj, labels)
            
        
        # Check if the pc directory is full
        elif function_obj.getUsedStorage(data['PC Directory']) == function_obj.getAvailableStorage(data['PC Directory']):
            _ = pops.invalidPhoneDirectory(frm)
            
        # Initiate the storeAnime window!
        #else:
            #storeAnimeObj = StoreAnime(INFOFILE)
            #storeAnimeObj.main(function_obj, func_but, labels, data)
            
            
    def makeAlertMessage(self, obj, unstoredTitles):
        text = "Unable to store the following titles:"
        text = obj.listShows(text, unstoredTitles)
        return text
            
    def alertUserUnmovedShows(self, frm, obj, pop, unStoredTitleDirs):
        
        # Message required
        text = self.makeAlertMessage(obj, unStoredTitleDirs)
        
        # Popup required
        pop.unstoredTitles(frm, text)
        
        
            
    def storeAnimeButton(self, frm, pop, obj, data, showListbox, showMap):
        """summary_ Button to store anime
        Args:
            pop (Object): a Popup object
            obj (Object): a Functions object
            labels (dict): a dictionary of StringVar labels
            showListbox (Listbox): a listbox of shows
            showMap (map): a map of show directories and titles
        
        Returns:
            showmap (map): a map of show directories and their respective titles
        """
        unStoredTitles = []
        
        dst = data['PC Directory']
        
        for title in showListbox.curselection():
            titleDir = showMap.get(title)
            
            if titleDir is None:
                unStoredTitles.append(title.split('\\')[-1])
                
            if titleDir.split('\\')[-2] == "localanime":
                # We found out that its a local download can directly move
                dst = os.path.join(dst, showMap.get(title).split('\\')[-1])
                
            # we will assume our title is in a source within the downloads folder
            else:
                dst = os.path.join(dst, showMap.get(title).split('\\')[-2], showMap.get(title).split('\\')[-1])
            
            shutil.move(title, dst)
        self.alertUserUnmovedShows(frm, pop, obj, unStoredTitles)
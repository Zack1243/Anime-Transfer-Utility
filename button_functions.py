import json
import math
import os
from popups import Popups
import shutil
import storeAnimePage
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

    def storeAnime(self, function_obj, frm, labels, *args):
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
        
        # Check if the pc directory is full
        elif function_obj.getUsedStorage(data['PC Directory']) == function_obj.getAvailableStorage(data['PC Directory']):
            _ = pops.invalidPhoneDirectory(frm)
            
        # Initiate the storeAnime window!
        #else:
            #storeAnimePage.main(function_obj, butt_func)
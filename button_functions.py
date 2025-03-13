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
    
    
    def buildProgressBar(self, root, obj):
        """summary_ Instantiates a progressbar

        Args:
            file (file): File seeking to be instantiated
        Returns:
            progressLabels (map): The map of labels corresponding to the progress bar
        """
        
        progressLabels = {
            "Summary": StringVar(), # Transfering NUM files to DIRECTORY
            "Percentage": StringVar(), # NUM% complete
            "numFiles": StringVar(), # Transfering file NUM/TOTAL
            "Name": StringVar(), # Name: NAME
            "sizeTransfered": StringVar(), # Transfered NUM / TOTAL SIZE
        }
        progressLabels["Percentage"].set("0%")
        
        myProgressBar = obj.gridProgressBar(root, 1, 0)

        return myProgressBar, progressLabels
        
            
    def storeAnimeButton(self, root, frm, pop, obj, data, labels, showListbox, showMap):
        """summary_ Button to store anime
        Args:
            pop (Object): a Popup object
            obj (Object): a Functions object
            labels (dict): a dictionary of StringVar labels
            showListbox (Listbox): a listbox of shows
            showMap (map): a map of show directories and titles
        
        #Returns:
            #showmap (map): a map of show directories and their respective titles
        """
        unStoredTitles = []
        print(showListbox.curselection())

        dst = data['PC Directory']
        if showListbox.curselection():
            #TODO: make a progress bar  
            myProgressBar, progressLabels = self.buildProgressBar(root, obj)
            #01: PAUSE
            #02: CANCEL
            numFiles = len(showListbox.curselection())
            
            
            print(f"Selected number of files: {numFiles}")
            
            
            
            progressLabels['numFiles'].set(f"Storing {numFiles} in {data['PC Directory']}")
            
            totalSize = 0
            showSize = []
            showNumSize = []
            
            print(showMap)
            reversed_showMap = {value: key for key, value in showMap.items()}
            
            for index in showListbox.curselection():
                
                
                title = showListbox.get(index)
                print(f"TITLE: {title}")
                
                
                
                # Find the directory of the title
                titleDir = reversed_showMap[title]
                
                
                
                
                
                print(f"Title Directory: {titleDir}")
                
                
                # Get the size of the title
                size = obj.getSize(titleDir)
                
                # Add size of the file to the total size
                totalSize += size
                
                # Adjust the units of size to be a string not an int
                sizeWUnit = obj.convert(size)
                
                
                
                showNumSize[f"{title}"] = size
                
                # Append the show to the showSize map
                showSize[f"{title}"] = sizeWUnit
                
            # Adjust the totalSize to be a string with the actual units
                
            totalSize = obj.convert(totalSize)
            
            index = 1
            
            amountStored = 0
            
            for title in showListbox.curselection():
                
                
                titleDir = reversed_showMap.get(title)
                titleSize = showSize[f"{title}"]

                if titleDir.split('\\')[-2] == "localanime":
                    # We found out that its a local download can directly move
                    dst = os.path.join(dst, showMap.get(title).split('\\')[-1])

                # we will assume our title is in a source within the downloads folder
                else:
                    #PC Directory -> downloads -> source -> title
                    dst = os.path.join(dst, "downloads", showMap.get(title).split('\\')[-2], showMap.get(title).split('\\')[-1])
                    
                
                myProgressBar['numFiles'].set(f"Storing file {index} / {numFiles}")
                
                
                myProgressBar['Name'].set(f"Currently storing title: {title}")
                
                shutil.move(title, dst)
                
                # Update how much has been stored
                myProgressBar['sizeTransfered'].set(f"Stored {titleSize} / {totalSize}")
                
                # Update the amount of data that has been stored
                amountStored += showNumSize[f"{title}"]
                
                percentage = round((amountStored / totalSize) * 100, 2)
                progressLabels["Percentage"].set(f"{percentage}%")
                
                index += 1


            for index in reversed(showListbox.curselection()):
                
                title = showListbox.get(index)
                # Remove from the dictionary
                if title in showMap:
                    del showMap[title]
                    # TODO: Delete debugging statements
                    print(f"Removed {title} from showMap.")
                # Remove item from the Listbox
                showListbox.delete(index)
                
                # TODO: Delete debugging statments
                print(f"Deleted {title} from Listbox.")
                
            #all_entries = [showListbox.get(index) for index in range(showListbox.size())]

            self.alertUserUnmovedShows(frm, pop, obj, unStoredTitles)
            #return showMap
            # Update the storage within the directory of the phone and pc
        #else:
            #return showMap
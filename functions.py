import button_functions as func_but
import json
import math
import os
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
INFOFILE = 'information.json'
VIDEO_EXTENSIONS = {".mov", ".mkv", ".mp4"}
    
class Functions:
    def __init__(self, infofile):
        self.infofile = infofile
        
    def checkInfofileInit(self):
        if not os.path.isfile(INFOFILE):
            # TODO: make an error exception when the infofile was not found
            #print(f"Infofile was not found in current directory({os.curdir()}). Attempting to create it...")
            data = {
                        "PC Directory": "testing",
                        "PC Capacity": "testing",
                        "PC storage usage": "testing",
                        "Phone storage usage": "testing",
                        "Phone Directory": "testing",
                        "Phone Capacity": "testing"
                    }
            with open(INFOFILE, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            if not os.path.isfile(INFOFILE):
                # TODO: Make an error exception when unable to make the infofile
                #print("INFOFILE creation unsuccessful...")
                return False
        return True
    
    def deleteFolders(self, folders):
        for folder in folders:
            shutil.rmtree(folder)
    
    def gridVariableLabel(self, frm, label_cont, r, c):
        label = ttk.Label(frm, textvariable=label_cont)
        label.grid(row=r, column=c)
        return label
    
    def gridLabel(self, frm, label_cont, r, c):
        label = ttk.Label(frm, text=label_cont)
        label.grid(row=r, column=c)
        return label
    
    def gridButton(self, frm, button_lab, button_function, r, c):
        button = ttk.Button(frm, text=button_lab, command = button_function)
        button.grid(row=r, column=c)
        return button
    
    def getInfofileData(self):
        with open(INFOFILE, 'r') as json_file:
            data = json.load(json_file)
        return data
        
    def getStorageUsage(self, directory):
        total_size = 0
        # Walk through each folder, subfolder, and files
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                # Get the full file path
                file_path = os.path.join(dirpath, filename)
                # Add the file size to the total size
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
        _, _, free = shutil.disk_usage(directory)
        if total_size == 0:
            return f"storage usage: 0B / {round(free / (1024**3), 2)} GB"
        
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(total_size, 1024)))
        p = math.pow(1024, i)
        s = round(total_size / p, 2)

        return f"storage usage: {s} {size_name[i]} / {round(free / (1024**3), 2)} GB"

    def getAvailableStorage(self, directory="."):
        total, used, free = shutil.disk_usage(directory)
        return round(free / (1024**3), 2)
    
    def getUsedStorage(self, directory):
        total_size = 0
        # Walk through each folder, subfolder, and files
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                # Get the full file path
                file_path = os.path.join(dirpath, filename)
                # Add the file size to the total size
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
        return round(total_size / (1024**3), 2)
                    
    def rootInit(self):
        """_summary_ Instantiates an instance of tkinter
        """
        root = Tk()
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        app_width = 600
        app_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.checkInfofileInit()
        
        with open(INFOFILE, 'r') as json_file:
            data = json.load(json_file)
            
        # TODO: Make the labels something actually meaningful
        labels = {
            "PC Directory": StringVar(),
            "PC Storage Usage": StringVar(),
            "Phone Directory": StringVar(),
            "Phone Storage Usage": StringVar(),
        }
        
        labels["PC Directory"].set(f"{data['PC Directory']}")
        print(labels['PC Directory'])
        labels["Phone Directory"].set(f"{data['Phone Directory']}")
        
        
        if os.path.exists(data['PC Directory']):
            labels["PC Storage Usage"].set("PC " + self.getStorageUsage(data["PC Directory"]))
        else: 
            labels["PC Storage Usage"].set("Current PC Directory is invalid!")
            
        # TODO: Check if the localanime and downloads subfolders exist within the phone directory as well
        if os.path.exists(data['Phone Directory']):
            labels["Phone Storage Usage"].set("Phone " + self.getStorageUsage(data["Phone Directory"]))
        else: 
            labels["Phone Storage Usage"].set("Current Phone Directory is invalid!")

        return root, frm, labels


















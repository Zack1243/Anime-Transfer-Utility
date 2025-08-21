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
global data
global labels
root = Tk()
frm = ttk.Frame(root, padding=10)
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
        
def populateRetrievePage():
    # List of the titles avaliable
        # Either in downloads -> subsidiary folder
    # os list directory contents
    curDir = os.getcwd()
    print(curDir)
        
        # Or part of what's present there (goes into localanime)
    
    
    # Shows are currently on the pc
    # Shows are within the folders on the pc
    


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
    #populateRetrievePage()
    retrieveRoot.mainloop()





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
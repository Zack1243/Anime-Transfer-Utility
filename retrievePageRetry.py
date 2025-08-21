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

# Get a Dictionaryh of [show: Directory]
def getShowMap():
    animeMap = {}

    # Get PC Directory
    current_dir = data["PC Directory"]
    # Get List of Directories in PC Directory
    directories = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    
    for title in directories:
        
        # Add all the localanime
        if title != "downloads":
            animeMap[title] = str(f"{current_dir}/{title}")
        
        # Add all the anime from sites
        elif title == "downloads":
            siteDirectories = [d for d in os.listdir(str(f"{current_dir}/{title}")) if os.path.isdir(os.path.join(str(f"{current_dir}/{title}"), d))]
            for site in siteDirectories:
                titles = [d for d in os.listdir(str(f"{current_dir}/downloads/{site}")) if os.path.isdir(os.path.join(str(f"{current_dir}/downloads/{site}"), d))]
                for title in titles:
                    animeMap[title] = str(f"{current_dir}/{site}/{title}")
    for anime in animeMap:
        print(anime + animeMap[anime])
    return animeMap

def gridListbox(frm, titles):
    my_scrollbar = Scrollbar(frm, orient=VERTICAL)
    my_listbox = Listbox(frm, width=50, yscrollcommand=my_scrollbar.set, selectmode=MULTIPLE)
    my_scrollbar.config(command=my_listbox.yview)
    my_listbox.grid(pady=15)
    my_listbox.grid(row=0, column=0)
    my_scrollbar.grid(row=0, column=1, sticky='ns')
    for show in titles:
        my_listbox.insert(0, show)
        #END??? instead of the 0 above
    return my_listbox



def populateRetrievePage():
    
    # Get a Dictionary of shows
    animeMap = getShowMap()

    # Make a listbox in tkinter
    showListbox = obj.gridListbox(
        frm,
        titles,
        r = 0,
        c = 0
    )
        

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
    
    populateRetrievePage()
    root.mainloop()
main()
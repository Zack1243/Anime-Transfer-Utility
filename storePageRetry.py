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
global animeMap
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
animeMap = {}


# Get a Dictionaryh of [show: Directory]
def getShowMap():
    global animeMap

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
                        animeMap[title] = str(f"{downloads}/{site}/{title}")
        elif title == "localanime":
            #localAnimeDir = os.path.join(current_dir, title).replace('/', '\\')
            
            
            localAnimeDir = [d for d in os.listdir(os.path.join(current_dir, title)) if os.path.isdir(os.path.join(current_dir, title))]
            #shows = [d for d in os.listdir(os.path.join(current_dir, title)) if os.path.isdir(os.path.join(current_dir, title))]
            print(f"local anime directory: {localAnimeDir}")
            for title in localAnimeDir:
                animeMap[title] = str(f"{current_dir}/localanime/{title}")
                print(f"stored {current_dir}/localanime/{title}")

# Make a list of shows
def gridListbox():
    my_scrollbar = Scrollbar(frm, orient=VERTICAL)
    my_listbox = Listbox(frm, width=50, yscrollcommand=my_scrollbar.set, selectmode=MULTIPLE)
    my_scrollbar.config(command=my_listbox.yview)
    my_listbox.grid(pady=15)
    my_listbox.grid(row=0, column=0)
    my_scrollbar.grid(row=0, column=1, sticky='ns')
    for show in animeMap:
        my_listbox.insert(0, show)
    my_listbox.grid()
    return my_listbox


def storeShows(my_listbox):
    dst = data['PC Directory']
    dst = dst.replace("/", "\\")
    if my_listbox.curselection():
        for index in my_listbox.curselection():
            title = my_listbox.get(index)
            print(f"Beginning to store title: {title}")            
            titleDir = animeMap[title]
            print(f"Directory of title: {animeMap[title]}")
            if titleDir.split('/')[-2] == data['Phone Directory'].split('/')[-1]:
                # PC Directory -> downloads -> source -> title
                dst = os.path.join(dst, "localanime", animeMap[title].split('/')[-1])
            # we will assume our title is in a source within the downloads folder
            
            else:
                # We found out that its a local download can directly move
                dst = os.path.join(dst, "downloads", animeMap[title].split('/')[-2], animeMap[title].split('/')[-1])
                
            print("Destination: " + dst)
            #os.move src to dst
            
        for index in reversed(my_listbox.curselection()):
            title = my_listbox.get(index)
            # Remove from the dictionary
            if title in animeMap:
                del animeMap[title]
            my_listbox.delete(index)
        my_listbox.delete(ANCHOR)

def populateStorePage():
    
    # Get a Dictionary of shows
    getShowMap()

    # Make a listbox of shows
    my_listbox = gridListbox()
    
    # Button to store shows
    retrieveButton = ttk.Button(text="Store", command=lambda: storeShows(my_listbox))
    retrieveButton.grid(row=1, column=0)
    

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
    
    populateStorePage()
    root.mainloop()
main()
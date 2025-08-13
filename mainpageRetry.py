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












def populateMainpage(root, frm, data):
    # Line 1
    welcomeLabel = ttk.Label(frm, text="Welcome to the Aniyomi GUI!")
    welcomeLabel.grid(row=0, column=0)
    
    # Line 2
    
    

# Make the mainpage
# Start the panel of tkinter
def main():
    
    # Make an instance of Tkinter
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

    # Check that Infofile has been instantiated
    if os.path.exists(INFOFILE):
        with open(INFOFILE, 'r') as json_file:
            data = json.load(json_file)
    
    # Cannot find INFOFILE. Create and populate with random data
    else:
        data = {
            "PC Directory": "testing",
            "PC Capacity": "testing",
            "PC storage usage": "testing",
            "Phone storage usage": "testing",
            "Phone Directory": "testing",
            "Phone Capacity": "testing",
        }
        with open(INFOFILE, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            
    if not os.path.exists(INFOFILE):
        print("ERROR: Cannot make the INFOFILE")
    
    populateMainpage(root, frm, data)
    root.mainloop()


main()
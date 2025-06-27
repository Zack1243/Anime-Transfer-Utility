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

class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        
        # Instantiations
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        self.menu = Menu(self)
        
        # Check if the infofile exists (else create one)
        if not os.path.isfile(INFOFILE):
            print("Infofile not found!")
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
                
        # Retrieve data from infofile
        with open(INFOFILE, 'r') as json_file:
            data = json.load(json_file)
        
        # Make variable Labels
        self.labels = {
            "PC Directory": StringVar(),
            "PC Storage Usage": StringVar(),
            "Phone Directory": StringVar(),
            "Phone Storage Usage": StringVar(),
        }
        
        
        self.mainloop()
        
class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.grid()
        self.createLayout()
        self.create_widgets()

    def createLayout(self):
        self.columnconfigure((0,1,2), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4,5,6), weight = 1, uniform = 'a')
        
    def create_widgets(self):
        
        # Line 1 (WELCOME LABEL)
        welcomeLabel = ttk.Label(self, text="Welcome to the anime transfer tool!")
        welcomeLabel.grid(row=0,column=0)
        
        # Line 2 (Choose Phone Directory)
        phoneDirectoryLabel = ttk.Label(self, text="Choose the aniyomi Phone directory (should be called Anime): ")
        phoneDirectoryLabel.grid(row=1,column=0)
        
        # Line 3 (Choose PC Directory)
        pcDirectoryLabel = ttk.Label(self, text="Choose a PC directory: ")
        pcDirectoryLabel.grid(row=2,column=0)

        # line 4
        

App('Class based app', (600,600))
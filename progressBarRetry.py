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
import subprocess
import sys
import re
import math

INFOFILE = 'information.json'
global root
global frm
global retrieveFrm
global retrieveRoot
global downloadRoot
global storeRoot
global storeFrm
global progressRoot
global progressFrm
global downloadFrm
global data
global labels
global retrieveAnimeMap
global storeAnimeMap
global progressLabels

root = Tk()
frm = ttk.Frame(root, padding=10)
retrieveAnimeMap = {}
storeAnimeMap = {}
showNumSize = {}
showSize = {}
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
progressLabels = {
    "Summary": StringVar(), # Transfering NUM files to DIRECTORY
    "Percentage": StringVar(), # NUM% complete
    "numFiles": StringVar(), # Transfering file NUM/TOTAL
    "Name": StringVar(), # Name: NAME
    "sizeTransfered": StringVar(), # Transfered NUM / TOTAL SIZE
}




def buildProgressBar():
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
    myProgressBar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
    myProgressBar.grid(row=0, column=0)
    return myProgressBar

def getSize(titleDir):
    total_size = 0
    # Walk through each folder, subfolder, and files
    for dirpath, dirnames, filenames in os.walk(titleDir):
        for filename in filenames:
            # Get the full file path
            file_path = os.path.join(dirpath, filename)
            # Add the file size to the total size
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def convert(size):
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)

    return f"{s} {size_name[i]}"

def transfer(src, dst):
    global progressLabels
    title = src.split('\\')[-1]
    size = getSize(src)
    convertedSize = convert(size)
    showNumSize[title] = size
    showSize[title] = convertedSize
    progressLabels["Name"] = f"Name: {title}"







def populateProgressPage(progressRoot):
    src = "D:\D Documents\Coding\emulated Aniyomi Phone\localanime\ben 10"
    dst = "D:\D Documents\Coding\emulated Aniyomi Phone\localanime"
    if os.path.exists("D:\D Documents\Coding\emulated Aniyomi Phone\ben 10"):
        dst = src
        src = "D:\D Documents\Coding\emulated Aniyomi Phone\ben 10"

    print("...........................................................")
    print("...........................................................")
    print(f"Source Directory: {src}")
    print(f"Destination Directory: {dst}")
       
    transfer(src, dst)
    



def progressPage():
    progressRoot = Tk()
    progressFrm = ttk.Frame(progressRoot, padding=10)
    progressFrm.grid()
    app_width = 600
    app_height = 500
    screen_width = progressRoot.winfo_screenwidth()
    screen_height = progressRoot.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    progressRoot.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    populateProgressPage(progressRoot)
    progressRoot.mainloop()

progressPage()
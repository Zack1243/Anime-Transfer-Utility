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
    if size == 0:
        return f"0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)

    return f"{s} {size_name[i]}"

# Stores the data of the titles
def storeData(src, dst):
    global progressLabels
    global showSize
    global showNumSize
    title = src.split("\\")[-1]
    size = getSize(src)
    convertedSize = convert(size)
    showNumSize[title] = size
    showSize[title] = convertedSize
    progressLabels["Name"].set(f"Name: {title}")

# This function test stores the items and will delete them afterwards
def storeTitles(srcs, dst, progressBar):
    global progressLabels
    global showSize
    global showNumSize
    transferSize = 0
    sizeTransfered = 0
    percentage = 0
    titleNum = 1
    for src in srcs:
        title = src.split("\\")[-1]
        print(f"THIS IS THE TITLE: {title}")
        transferSize = transferSize + showNumSize[title]
    totalSize = convert(transferSize)
    
    title = srcs[0].split("\\")[-1]
    progressLabels["Percentage"].set(f"{percentage}% Complete")
    progressLabels['Name'].set(f"Name: {title}")
    progressLabels['sizeTransfered'].set(f"Transfered 0 / {totalSize}")
    progressLabels['numFiles'].set(f"Stored {titleNum} / {len(srcs)} titles in {dst}")
        
    for src in srcs:
        title = src.split("\\")[-1]
        
        newDst = os.path.join(dst, title)
        shutil.copytree(src, newDst)
        
        sizeTransfered = sizeTransfered + showNumSize[title]
        cvrtedSizeTransfered = convert(sizeTransfered)
        
        percentage = (sizeTransfered / transferSize) * 100
        progressLabels["Percentage"].set(f"{percentage}% Complete")
        progressLabels['Name'].set(f"Name: {title}")
        progressLabels['sizeTransfered'].set(f"Transfered {cvrtedSizeTransfered} / {totalSize}")
        progressBar['value'] = percentage
        progressLabels['numFiles'].set(f"Stored {titleNum} / {len(srcs)} titles in {dst}")
        titleNum = titleNum + 1

def populateProgressPage(progressRoot, progressFrm):
    global progressLabels
    
    srcs = [
            r"D:\emulated Aniyomi PC\desk wars",
            r"D:\emulated Aniyomi PC\dead cells",
            r"D:\emulated Aniyomi PC\castle"
            #r"D:\emulated Aniyomi PC\pokemon",
            #r"D:\emulated Aniyomi PC\last of us",
            ]
    
    # The number of titles being transfered TODO: Make it into a changeable variable
    numSrcs = 3
    
    # The destination directory for this particular transfer TODO: Make it into a changeable variable
    dst = r"D:\emulated Aniyomi Phone\localanime"
    
    sizeTransferedLabel = ttk.Label(progressFrm, textvariable=progressLabels['numFiles'])
    sizeTransferedLabel.grid(row=0, column=0)
    
    nameLabel = ttk.Label(progressFrm, textvariable=progressLabels['Name'])
    nameLabel.grid(row=1, column=0)
    
    sizeTransferedLabel = ttk.Label(progressFrm, textvariable=progressLabels['sizeTransfered'])
    sizeTransferedLabel.grid(row=2, column=0)
    
    percentageLabel = ttk.Label(progressFrm, textvariable=progressLabels['Percentage'])
    percentageLabel.grid(row=3, column=0)
    
    myProgressBar = ttk.Progressbar(progressFrm, orient="horizontal", length=300, mode='determinate')
    myProgressBar.grid(row=4, column=0)

    storeButton = ttk.Button(progressFrm, text="Store", command=lambda: storeTitles(srcs, dst, myProgressBar))
    storeButton.grid(row=10,column=0)


def startTestTransfer():
    # List of titles to test transfer
    srcs = [
            r"D:\emulated Aniyomi PC\desk wars",
            r"D:\emulated Aniyomi PC\dead cells",
            r"D:\emulated Aniyomi PC\castle"
            #r"D:\emulated Aniyomi PC\pokemon",
            #r"D:\emulated Aniyomi PC\last of us",
            ]
    dst = r"D:\emulated Aniyomi Phone\localanime"

    print("...........................................................")
    print("...........................................................")
    print(f"Source Directories: {srcs}")
    print(f"Destination Directory: {dst}")

    for src in srcs:
        storeData(src, dst)

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
    
    
    startTestTransfer(progressFrm)
    # Info has already been populated
    # Start the progressRoot
    
    
    populateProgressPage(progressRoot, progressFrm)
    progressRoot.mainloop()
progressPage()

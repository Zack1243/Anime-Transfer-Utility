import json
import math
import os
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox

def confirm_infoFile_instantiation(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data





















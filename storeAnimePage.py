import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox


# Run a new instance of ttk
INFOFILE = 'information.json'
VIDEO_EXTENSIONS = {".mov", ".mkv", ".mp4"}

def main(function_obj, butt_func):
    obj = function_obj(INFOFILE)
    func_but = butt_func(INFOFILE)
    root, frm, labels = obj.rootInit()
    if obj.checkInfofileInit():
        data = obj.getInfofileData()
    
    
if __name__ == "__main__":
    main()
    
    











root_store = Tk()
frm_store = ttk.Frame(root_store, padding=10)
frm_store.grid()
app_width = 500
app_height = 500
screen_width = root_store.winfo_screenwidth()
screen_height = root_store.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root_store.geometry(f'{app_width}x{app_height}+{int(x + 100)}+{int(y + 100)}')
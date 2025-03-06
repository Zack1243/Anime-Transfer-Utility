from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
class Popups:
    def __init__(self, infofile):
        self.infofile = infofile

    def invalidPCDirectory(self,frm):
        invalid_pc_messagebox = messagebox.askokcancel(
            title="The chosen PC directory is invalid!",
            message="Please choose a valid pc directory before attempting to retrieve/store anime",
            icon="warning",
            parent=frm
        )
        return invalid_pc_messagebox
















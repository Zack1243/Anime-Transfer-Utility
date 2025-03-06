from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
class Popups:
    def __init__(self, infofile):
        self.infofile = infofile

    def invalidPCDirectory(self,frm):
        """_summary_ Initiates a popup telling the user their pc directory is invalid and to choose a new one
        Args:
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        invalid_pc_messagebox = messagebox.askokcancel(
            title="The chosen PC directory is invalid!",
            message="Please choose a valid pc directory before attempting to retrieve/store anime",
            icon="warning",
            parent=frm
        )
        return invalid_pc_messagebox
    
    def invalidPhoneDirectory(self,frm):
        """_summary_ Initiates a popup telling the user their phone directory is invalid and to choose a new one
        Args:
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        invalid_phone_messagebox = messagebox.askokcancel(
            title="The chosen PC directory is invalid!",
            message="Please choose a valid phone directory before attempting to retrieve/store anime",
            icon="warning",
            parent=frm
        )
        return invalid_phone_messagebox
    
    def fullPC(self,frm):
        """_summary_ Initiates a popup telling the user their pc directory is too full to store anime
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        invalid_phone_messagebox = messagebox.askokcancel(
            title="The chosen PC directory is full!",
            message="Free up space before attempting to store more anime on your pc.",
            icon="error",
            parent=frm
        )
        return invalid_phone_messagebox
    
    def deleteShows(frm, text):
        """_summary_ Initiates a popup telling the user they have invalid folders within their pc directory
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        delete_shows_messagebox = messagebox.askyesno(
            title="Invalid Folders Discovered Within PC Directory",
            message=text,
            icon="warning",
            parent=frm,
            default="no"
        )
        return delete_shows_messagebox
    
    
    def confirmDeleteShows(frm, text):
        """_summary_ Initiates a popup asking if the user is sure they want to delete the invalid show folders
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        confirm_show_deletion = messagebox.askyesno(
            title="Are you sure?",
            message=text,
            icon="question",
            parent=frm,
            default="no"
        )
        return confirm_show_deletion















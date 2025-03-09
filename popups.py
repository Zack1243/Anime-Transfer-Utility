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
    
    def cannotFindAniyomiFolder(self,frm):
        """_summary_ Initiates a popup telling the user their aniyomi folder is probably invalid
        Args:
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        cannotFindAniyomiFolderMessagebox = messagebox.askokcancel(
            title="Your aniyomi folder might be invalid!",
            message="The user has continuously failed to find a proper aniyomi folder.\nDoublecheck if your aniyomi folder has \"localanime\" and \"downloads\" \n(you can manually add them as subfolder(s) if you want to brute force this program to work)",
            icon="error",
            parent=frm
        )
        return cannotFindAniyomiFolderMessagebox
    
    def noLocalAnimeDetected(self, frm):
        """_summary_ Initiates a popup telling the user their phone directory is invalid because localAnime is not detected
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        noLocalAnimeMessagebox = messagebox.askokcancel(
            title="The chosen folder for aniyomi is invalid",
            message="Please choose a valid phone directory before attempting to retrieve/store anime.\nReason: no localanime folder detected",
            icon="warning",
            parent=frm
        )
        return noLocalAnimeMessagebox
    
    def noDownloadsDetected(self, frm):
        """_summary_ Initiates a popup telling the user their phone directory is invalid because downloads folder is not detected
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        noDownloadsMessagebox = messagebox.askokcancel(
            title="The chosen folder for aniyomi is invalid",
            message="Please choose a valid phone directory before attempting to retrieve/store anime.\nReason: no downloads folder detected",
            icon="warning",
            parent=frm
        )
        return noDownloadsMessagebox
    
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
    
    def deletePhoneShows(self, frm, text):
        """_summary_ Initiates a popup telling the user they have invalid folders within their Phone directory
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        delete_shows_messagebox = messagebox.askyesno(
            title="Invalid Folders Discovered Within Phone Directory",
            message=text,
            icon="warning",
            parent=frm,
            default="no"
        )
        return delete_shows_messagebox
    
    def deletePCShows(self, frm, text):
        """_summary_ Initiates a popup telling the user they have invalid folders within their PC directory
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        deletePCShowsMessagebox = messagebox.askyesno(
            title="Invalid Folders Discovered Within PC Directory",
            message=text,
            icon="warning",
            parent=frm,
            default="no"
        )
        return deletePCShowsMessagebox
    
    
    def duplicatesFound(self, frm, duplicateMessage, duplicateShows):
        """_summary_ Initiates a popup asking if the user would like to delete the duplicate shows
            frm (frm): The framework to show the popup over
        Returns:
            Choice (Boolean): The choice the user picks
        """
        confirm_show_deletion = messagebox.askyesno(
            title="Duplicate titles found",
            message=duplicateMessage,
            icon="question",
            parent=frm,
            default="no"
        )
        return confirm_show_deletion
    
    
    def confirmDeleteShows(self, frm, text):
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
    
    
    def unstoredTitles(self, frm, text):
        """_summary_ Some of your titles were not stored on the PC
        Args:
            frm (frm): The framework to show the popup over
            text (string): The message to fill the message window with
        Returns:
            Choice (Boolean): The choice the user picks
        """
        confirm_show_deletion = messagebox.ok(
            title="Unable to store some titles",
            message=text,
            icon="Error",
            parent=frm,
            default="no"
        )
        return confirm_show_deletion
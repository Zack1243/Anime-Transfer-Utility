import json
import math
import os
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter import Listbox
INFOFILE = 'information.json'
VIDEO_EXTENSIONS = {".mov", ".mkv", ".mp4"}
    
class Functions:
    def __init__(self, infofile):
        self.infofile = infofile
        
    def checkInfofileInit(self):
        if not os.path.isfile(INFOFILE):
            # TODO: make an error exception when the infofile was not found
            #print(f"Infofile was not found in current directory({os.curdir()}). Attempting to create it...")
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
            if not os.path.isfile(INFOFILE):
                # TODO: Make an error exception when unable to make the infofile
                #print("INFOFILE creation unsuccessful...")
                return False
        return True
    
    def deleteFolders(self, folders):
        for folder in folders:
            shutil.rmtree(folder)
    
    def gridVariableLabel(self, frm, label_cont, r, c):
        print(str(label_cont))
        label = ttk.Label(frm, textvariable=label_cont)
        label.grid(row=r, column=c)
        return label
    
    def gridLabel(self, frm, label_cont, r, c):
        label = ttk.Label(frm, text=label_cont)
        label.grid(row=r, column=c)
        return label
    
    def gridListbox(self, frm, titles, r, c):
        my_scrollbar = Scrollbar(frm, orient=VERTICAL)
        my_listbox = Listbox(frm, width=50, yscrollcommand=my_scrollbar.set, selectmode=MULTIPLE)
        my_scrollbar.config(command=my_listbox.yview)
        my_listbox.grid(pady=15)
        my_listbox.grid(row=0, column=0)
        my_scrollbar.grid(row=0, column=1, sticky='ns')
        for show in titles:
            my_listbox.insert(0, show)
            #END??? instead of the 0 above
    
    def gridEntrybox(self, root, r, c):
        my_entrybox = Entry(root)
        my_entrybox.grid()
        
    # TODO:
    #def gridProgressBar(self, frm, label_cont, r, c):
        
    
    def gridButton(self, frm, button_lab, button_function, r, c):
        button = ttk.Button(frm, text=button_lab, command = button_function)
        button.grid(row=r, column=c)
        return button
    
    def getInfofileData(self):
        with open(INFOFILE, 'r') as json_file:
            data = json.load(json_file)
        return data
        
    def getStorageUsage(self, directory):
        total_size = 0
        # Walk through each folder, subfolder, and files
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                # Get the full file path
                file_path = os.path.join(dirpath, filename)
                # Add the file size to the total size
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
        _, _, free = shutil.disk_usage(directory)
        if total_size == 0:
            return f"storage usage: 0B / {round(free / (1024**3), 2)} GB"
        
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(total_size, 1024)))
        p = math.pow(1024, i)
        s = round(total_size / p, 2)

        return f"storage usage: {s} {size_name[i]} / {round(free / (1024**3), 2)} GB"

    def getAvailableStorage(self, directory="."):
        total, used, free = shutil.disk_usage(directory)
        return round(free / (1024**3), 2)
    
    def getUsedStorage(self, directory):
        total_size = 0

        # Walk through each folder, subfolder, and files
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                # Get the full file path
                file_path = os.path.join(dirpath, filename)
                # Add the file size to the total size
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
                    
        return round(total_size / (1024**3), 2)
                    
    def rootInit(self):
        """_summary_ Instantiates an instance of tkinter
        """
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
        self.checkInfofileInit()
        
        with open(INFOFILE, 'r') as json_file:
            data = json.load(json_file)
            
        # TODO: Make the labels something actually meaningful
        labels = {
            "PC Directory": StringVar(),
            "PC Storage Usage": StringVar(),
            "Phone Directory": StringVar(),
            "Phone Storage Usage": StringVar(),
        }
        
        labels["PC Directory"].set(f"{data['PC Directory']}")
        print( "pc directory: " + str(labels['PC Directory']) )
        labels["Phone Directory"].set(f"{data['Phone Directory']}")
        
        if os.path.exists(data['PC Directory']):
            labels["PC Storage Usage"].set("PC " + self.getStorageUsage(data["PC Directory"]))
        else: 
            labels["PC Storage Usage"].set("Current PC Directory is invalid!")
            
        # TODO: Check if the localanime and downloads subfolders exist within the phone directory as well
        if os.path.exists(data['Phone Directory']):
            labels["Phone Storage Usage"].set("Phone " + self.getStorageUsage(data["Phone Directory"]))
        else: 
            labels["Phone Storage Usage"].set("Current Phone Directory is invalid!")

        return root, frm, labels
    
    
    def validAniyomiDirectory(self, frm, function_obj, func_but, pop, phoneDir, labels, *args):
        """summary_ Checks if the chosen phone directory is valid by the presence of the localanime and downloads subfolders

        Args:
            frm (Frame): the framework of the tkinter
            Pop (obj): The object of the Popup class
            obj (obj): Object of the Functions Class
            func_but (Obj): Object of the Button_Function class
            phoneDir (Str): Phone directory being referenced
            labels (dictionary): A dictionary of StringVars for the mainpage tkinter
        Returns:
            Boolean (T/F): if it's valid of the file
        """
        # Get localanime directory
        localAnimeDir = os.path.join(str(phoneDir), "localanime").replace("/", "\\")
        
        # Get downloads directory
        downloadsDir = os.path.join(str(phoneDir), "downloads").replace("/", "\\")
        
        # True and true
        attemptsRemaining = 3
        
        while (not os.path.exists(localAnimeDir) or not os.path.exists(downloadsDir)) and attemptsRemaining < 1:
            print(f"localanime? {os.path.exists(localAnimeDir)}")
            print(f"downloads? {os.path.exists(downloadsDir)}")
            print(f"attempts remaining count: {attemptsRemaining}")
            
            
            # Check if localanime subfolder exists
            if not os.path.exists(localAnimeDir):
                if pop.noLocalAnimeDetected(frm):
                    func_but.setPhoneDirectory(function_obj, labels)
            
            # Check if downloads subfolder exists
            if not os.path.exists(downloadsDir):
                if pop.noDownloadsDetected(frm):
                    func_but.setPhoneDirectory(function_obj, labels)
    
            attemptsRemaining = attemptsRemaining - 1
            
            
        if attemptsRemaining == 0:
            _ = pop.cannotFindAniyomiFolder(frm)
            return False
        return True
    
    def getEmptyShows(self, localAnimeDirs):
        """summary_ Finds empty shows and returns a list of them

        Args:
            showDirectory (directory): User's directory for their aniyomi folder
        Returns:
            emptyShows (list): list of empty shows
        """
        emptyFolders = []
        for show in localAnimeDirs:
                if not os.path.isdir(show):
                    emptyFolders.append(show)
                    continue
                found = any(file.endswith((".mov", ".mkv", ".mp4")) for _, _, files in os.walk(show) for file in files)
                if not found:
                    emptyFolders.append(show)
                    continue
        return emptyFolders
    
    def listShows(self, text, shows):
        """summary_ Returns a list of shows

        Args:
            text (string): string to add the shows to
            shows (list): list of show directories
        Returns:
            text (string): string with shows added
        """
        for show in shows:
            title = show.split('\\')[-1]
            text += f"- {title}\n"
        return text
    
    
    
    def cullEmptyShows(self, srcDir, frm, pops, data, *args):
        """summary_ Identifies and eliminates empty shows with user's consent

        Args:
            phonedirectory (directory): User's directory for their aniyomi folder
        Returns:
            Boolean (T/F): if it's valid of the file
        """
        
        # Get localanime directory
        localAnimeDir = os.path.join(str(srcDir), "localanime").replace("/", "\\")
        
        
        # Get list of show directories in localAnime
        localAnimeDirs = [os.path.join(str(localAnimeDir), item).replace("/", "\\") for item in os.listdir(localAnimeDir)]
        
        
        emptyFolders = self.getEmptyShows(localAnimeDirs)
        
        if emptyFolders:
            
            # Remove shows from list of folders    
            for show in emptyFolders:
                localAnimeDirs.remove(show)

            # Construct a message informing the user of the missing titles in their phone storage
            missing_titles_warning_message = f"The following titles within {data['Phone Directory']} contain no .mkv, .mp4, or .mov files and cannot be stored. (You may wish to confirm if you are using the right Phone Directory)\n\n"
            missing_titles_warning_message = self.listShows(missing_titles_warning_message, emptyFolders)
            missing_titles_warning_message = missing_titles_warning_message + "\nWould you like to delete them?"

            # Construct a message asking the user if they are sure whether they would like to delete the shows or not
            if pops.deletePhoneShows(frm, missing_titles_warning_message):
                confirm_deletion_message = "Are you sure you would like to delete the following titles?\n\n"
                confirm_deletion_message = self.listShows(confirm_deletion_message , emptyFolders)

                # If the user clicks yes, delete the shows
                if pops.confirmDeleteShows(frm, confirm_deletion_message):
                    for folder in emptyFolders:
                        shutil.rmtree(folder)
        return localAnimeDirs
    
    def getDuplicateShowMessage(self, duplicateShows):
        # Construct a message informing the user of the missing titles in their phone storage
        duplicateShowMessage = f"The following titles are duplicates of existing titles.\n\n"
        duplicateShowMessage = self.listShows(duplicateShowMessage, duplicateShows)
        duplicateShows += "\nWould you like to delete them?"
        
    def cullDuplicates(self, pop, frm, duplicateShows):
        """summary_ Asks the user if they would like to get rid of any duplicate titles

        Args:
            pop (Object): an object of the Popups class
            frm (Tkinter Frame): a Tkinter frame
            duplicateShows (list): A list of directories of duplicate shows
        """
        duplicateMessage = self.getDuplicateShowMessage(duplicateShows)
        
        if pop.duplicatesFound(frm, duplicateMessage, duplicateShows):
            confirm_deletion_message = "Are you sure you would like to delete the following titles?\n\n"
            confirm_deletion_message = self.listShows(duplicateMessage, duplicateShows)
            
            if pop.confirmDeleteShows(self, frm, confirm_deletion_message):
                for show in duplicateShows:
                    shutil.rmtree(show)
    
    def getShowMap(self, frm, pop, localAnimeDirs, downloadsDir):
        """summary_ Assembles a map of show directories and their respective titles. Also calls cullDuplicates to get rid of duplicate titles

        Args:
            frm (Tkinter Frame): a Tkinter frame
            pop (Object): an object of the Popups class
            duplicateShows (list): A list of show directories in localanime
            downloadsDir (string): the downloads directory inside of aniyomi
        
        Returns:
            showmap (map): a map of show directories and their respective titles
        """
        showMap = {}
        duplicateShows = []
        
        for show in localAnimeDirs:
            if show.split('\\')[-1] not in showMap:
                showMap[show] = show.split('\\')[-1]
            else:
                title = show.split('\\')[-1]
                print(f"Duplicate show found: {title}, skipping.")
                duplicateShows[show] = show.split('\\')[-1]
        
        all_items = os.listdir(downloadsDir)

        # Filter out only the subdirectories
        sources = [item for item in all_items if os.path.isdir(os.path.join(downloadsDir, item))]
        
        for show in sources:
            if show.split('\\')[-1] not in showMap:
                showMap[show] = show.split('\\')[-1]
            else:
                title = show.split('\\')[-1]
                print(f"Duplicate show found: {title}, skipping.")
                duplicateShows.append(show)
        
        if duplicateShows:
            # Get rid of any duplicate shows
            self.cullDuplicates(pop, frm, duplicateShows)

        return showMap
        
    #def storeSelected(my_listbox, root, data, ):
        """summary_ Transfers selected titles into the Phone storage

        Args:
            emptyShows (list): List of empty show directories
        """
        #for title in my_listbox.curselection():
            
        
        
        
        
        
        #test = []
        #for item in my_listbox.curselection():
            #test.append(str.strip((my_listbox.get(item)))       )
        #combined_text = ', '.join(test)
        #combined_label = Label(root, text=combined_text)
        #combined_label.grid()  # Place it below the individual labels
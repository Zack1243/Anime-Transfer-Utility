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
        return my_listbox
    
    def gridEntrybox(self, root, r, c):
        my_entrybox = Entry(root)
        my_entrybox.grid()
        
        
    def getSize(self, titleDir):
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
        
    
    # TODO:
    def gridProgressBar(self, root, r, c):
        myProgressBar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
        myProgressBar.grid(row=r, column=c)
        return myProgressBar
        
    
    def gridButton(self, frm, button_lab, button_function, r, c):
        button = ttk.Button(frm, text=button_lab, command = button_function)
        button.grid(row=r, column=c)
        return button
    
    def getInfofileData(self):
        with open(INFOFILE, 'r') as json_file:
            data = json.load(json_file)
        return data
    
    
    def convert(self, size):
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size, 1024)))
        p = math.pow(1024, i)
        s = round(size / p, 2)

        return f"{s} {size_name[i]}"
        
        
        
        
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
    
    
    
    def cullEmptyShows(self, frm, pops, data, emptyShows, *args):
        """summary_ Identifies and eliminates empty shows with user's consent

        Args:
            phonedirectory (directory): User's directory for their aniyomi folder
        Returns:
            Boolean (T/F): if it's valid of the file
        """
        # Construct a message informing the user of the missing titles in their phone storage
        missing_titles_warning_message = f"The following titles within {data['Phone Directory']} contain no .mkv, .mp4, or .mov files and cannot be stored. (You may wish to confirm if you are using the right Phone Directory)\n\n"
        missing_titles_warning_message = self.listShows(missing_titles_warning_message, emptyShows)
        missing_titles_warning_message = missing_titles_warning_message + "\nWould you like to delete them?"
        # Construct a message asking the user if they are sure whether they would like to delete the shows or not
        if pops.deletePhoneShows(frm, missing_titles_warning_message):
            confirm_deletion_message = "Are you sure you would like to delete the following titles?\n\n"
            confirm_deletion_message = self.listShows(confirm_deletion_message , emptyShows)
            # If the user clicks yes, delete the shows
            if pops.confirmDeleteShows(frm, confirm_deletion_message):
                for folder in emptyShows:
                    shutil.rmtree(folder)
    
    def getDuplicateShowMessage(self, duplicateShows):
        # Construct a message informing the user of the missing titles in their phone storage
        duplicateShowMessage = f"The following titles are duplicates of existing titles.\n\n"
        duplicateShowMessage = self.listShows(duplicateShowMessage, duplicateShows)
        duplicateShowMessage += "\nWould you like to delete them?"
        return duplicateShowMessage
        
    def cullDuplicates(self, pop, frm, duplicateShows):
        """summary_ Asks the user if they would like to get rid of any duplicate titles

        Args:
            pop (Object): an object of the Popups class
            frm (Tkinter Frame): a Tkinter frame
            duplicateShows (list): A list of directories of duplicate shows
        """
        duplicateMessage = self.getDuplicateShowMessage(duplicateShows)
        print(duplicateMessage)
        if pop.duplicatesFound(frm, duplicateMessage):
            text = "Would you like to delete from 'local anime'?\n(hit no to delete from downloads or cancel to cancel deletion)"
            if pop.dirToCullDups(frm, text):
                confirm_deletion_message = "Are you ABSOLUTELY sure you would like to delete the following titles?\nfinal warning I promise :)\n\n"
                confirm_deletion_message = self.listShows(duplicateMessage, duplicateShows)

                
                # TODO: ADD A SCROLLBOX SELECTION FOR THE USER TO DELETE FROM
                if pop.confirmDeleteShows(self, frm, confirm_deletion_message):
                    for show in duplicateShows:
                        shutil.rmtree(show)
    
    
    def getShowMap(self, frm, pop, localAnimeDirs, sourceTitleDirs):
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
        if localAnimeDirs:
            for show in localAnimeDirs:
                if show.split('\\')[-1] not in showMap:
                    showMap[show] = show.split('\\')[-1]
                else:
                    title = show.split('\\')[-1]
                    print(f"Duplicate show found: {title}, skipping.")
                    duplicateShows[show] = show.split('\\')[-1]
                
        if sourceTitleDirs:
            
            for show in sourceTitleDirs:
                if show.split('\\')[-1] not in showMap:
                    print(f"APPENDED TITLE: {show}")
                    showMap[show] = show.split('\\')[-1]
                else:
                    title = show.split('\\')[-1]
                    print(f"Duplicate show found: {title}, skipping.")
                    duplicateShows.append(show)

        if duplicateShows:
            # Get rid of any duplicate shows
            self.cullDuplicates(pop, frm, duplicateShows)

        return showMap
        
            
    def isEmpty(self, title):
        if not os.path.isdir(title):
            return False
        
        found = any(file.endswith((".mov", ".mkv", ".mp4")) for _, _, files in os.walk(title) for file in files)
        if not found:
            return True
        return False
        
    
    def checkValid(self, showMap, titleList):
        invalidTitles = []
        duplicateTitles = []
        emptyTitles = []
        
        
        for title in titleList:
            # Check if the path exists
            if not os.path.exists(title):
                invalidTitles.append(title)
                
            # Check if the path is an empty directory
            elif self.isEmpty(title):
                emptyTitles.append(title)
                
            # Check if the path is a duplicate of an existing title
            elif title.split('\\')[-1] not in showMap.values():
                
                show = title.split('\\')[-1]
                showMap[title] = title.split('\\')[-1]
            else:
                duplicateTitles.append(title)
                
        return invalidTitles, duplicateTitles, emptyTitles, showMap
        
    def isValidSources(self, downloadedSourcesDirs):
        sourceTitleDirs = []
        for source in downloadedSourcesDirs:
            if os.path.exists(source):
                sourceTitles = [os.path.join(str(source), item).replace("/", "\\") for item in os.listdir(source)]
                if sourceTitles:
                    for sourceTitle in sourceTitles:
                            if os.path.exists(sourceTitle):
                                if sourceTitle not in downloadedSourcesDirs:
                                    sourceTitleDirs.append(sourceTitle)
        return sourceTitleDirs
                
    
    def getValidShowMap(self, frm, obj, func_but, pop, phoneDir, labels):
        # Get local anime directory
        localAnimeDir = os.path.join(str(phoneDir), "localanime").replace("/", "\\")
        
        # Get downloads directory
        downloadsDir = os.path.join(str(phoneDir), "downloads").replace("/", "\\")
        
        # Get a list of the title directories in the 'local anime' folder
        localAnimeTitleDirs = [os.path.join(str(localAnimeDir), item).replace("/", "\\") for item in os.listdir(localAnimeDir)]
        
        # Get a list of directories of the sources in the downloads folder
        downloadedSourcesDirs = [os.path.join(str(downloadsDir), item).replace("/", "\\") for item in os.listdir(downloadsDir)]
        
        # Instantiate a list of title directories in the source directories
        sourceTitleDirs = []
        
        # Instanitate a list of invalid directories
        invalidSources = []
        
        # Instantiate a showMap that matches titles to their directories
        showMap = dict([])
        
        if downloadedSourcesDirs:
            # Check if all sources are valid
            sourceTitleDirs = self.isValidSources(downloadedSourcesDirs)
        
        if sourceTitleDirs and localAnimeTitleDirs:
            invalidTitles, duplicateTitles, emptyTitles, showMap = self.checkValid(showMap, localAnimeTitleDirs + sourceTitleDirs)
        elif sourceTitleDirs:
            invalidTitles, duplicateTitles, emptyTitles, showMap = self.checkValid(showMap, sourceTitleDirs)
        elif localAnimeTitleDirs:
            invalidTitles, duplicateTitles, emptyTitles, showMap = self.checkValid(showMap, localAnimeTitleDirs)
        else:
            _ = pop.noTitlesToStore(frm)
            return showMap
        return invalidTitles, duplicateTitles, emptyTitles, showMap
    
    
    
    def printInvalidSources(invalidSources):
        print("....................................")       
        print("The following sources are invalid....")
        for source in invalidSources:
            print(source)
        print("....................................")
        
        
        
    
    
    
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
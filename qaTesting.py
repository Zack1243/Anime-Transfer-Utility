import unittest
import json
import os
from unittest.mock import patch
from mainpageRetry import App, INFOFILE  # Assuming your App class and INFOFILE are in a file called 'app.py'


class TestApp(unittest.TestCase):
    
    # Test 1: Check if the infofile is created when it does not exist
    @patch("os.path.isfile")
    def test_infofile_creation(self, mock_isfile):
        # Simulate that the file doesn't exist
        mock_isfile.return_value = False
        
        # Create the App instance
        app = App("Test App", (600, 600))

        # Verify that the infofile was created
        self.assertTrue(os.path.isfile(INFOFILE))
        
        # Read the content of the infofile
        with open(INFOFILE, 'r') as file:
            data = json.load(file)
        
        # Check if the default data is written to the file
        self.assertEqual(data["PC Directory"], "testing")
    
    # Test 2: Test the setPCDirectory method when the user selects a directory
    @patch("tkinter.filedialog.askdirectory")
    @patch("os.path.exists")
    def test_set_pc_directory(self, mock_exists, mock_askdirectory):
        # Simulate the user selecting a valid directory
        mock_askdirectory.return_value = "/mock/directory"
        mock_exists.return_value = True  # Simulate that the directory exists
        
        # Create the App instance
        app = App("Test App", (600, 600))
        menu = app.menu  # Access the menu that contains the setPCDirectory method

        # Call the setPCDirectory method which should update the infofile
        menu.setPCDirectory()

        # Verify that the infofile was updated with the new directory
        with open(INFOFILE, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(data["PC Directory"], "/mock/directory")
    
    # Test 3: Test the setPCDirectory method when the user cancels directory selection
    @patch("tkinter.filedialog.askdirectory")
    def test_directory_selection_cancelled(self, mock_askdirectory):
        # Simulate the user canceling the directory selection
        mock_askdirectory.return_value = ""
        
        # Create the App instance
        app = App("Test App", (600, 600))
        menu = app.menu  # Access the menu that contains the setPCDirectory method

        # Call the setPCDirectory method, which should handle the cancellation
        menu.setPCDirectory()

        # Verify that the infofile was not updated (i.e., it should remain as the initial state)
        with open(INFOFILE, 'r') as file:
            data = json.load(file)
        
        # Check that the directory is still set to the default value
        self.assertEqual(data["PC Directory"], "testing")


if __name__ == "__main__":
    unittest.main()

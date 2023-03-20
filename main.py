# Import os and sys modules to work with files, directories and command line arguments
import os
import sys

# Check if a command line argument is given
if len(sys.argv) > 1:
    # Get the folder path from the first argument
    folder_path = sys.argv[1]
else:
    # If no argument is given, print an error message and exit
    print("Please provide a folder path as an argument.")
    sys.exit()

# Loop through all the items in the folder
for item in os.listdir(folder_path):
    # Get the full path of the item
    item_path = os.path.join(folder_path, item)
    # Check if the item is a file or a directory
    if os.path.isfile(item_path):
        # Get the file extension of the item
        file_ext = os.path.splitext(item)[1]
        # Create a new folder name based on the file extension
        new_folder = file_ext[1:].upper() + " Files"
        # Create a new folder path based on the folder name
        new_folder_path = os.path.join(folder_path, new_folder)
        # Check if the new folder already exists, if not create it
        if not os.path.exists(new_folder_path):
            os.mkdir(new_folder_path)
        # Move the file to the new folder
        os.rename(item_path, os.path.join(new_folder_path, item))
    elif os.path.isdir(item_path):
        # Create a new folder name for folders
        new_folder = "Folders"
        # Create a new folder path based on the folder name
        new_folder_path = os.path.join(folder_path, new_folder)
        # Check if the new folder already exists, if not create it
        if not os.path.exists(new_folder_path):
            os.mkdir(new_folder_path)
        # Move the directory to the new folder
        os.rename(item_path, os.path.join(new_folder_path, item))
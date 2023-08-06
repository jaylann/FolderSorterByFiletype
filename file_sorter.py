import os
import shutil
from pathlib import Path
import argparse

from tqdm import tqdm


class FileSorter:
    """
    Class that sorts files in a specified directory based on their file extensions.
    It moves the files to their respective folders named after their file extensions.
    """

    def __init__(self, directory):
        """
        Initialize the FileSorter with the target directory.
        """
        self.directory = Path(directory)
        self.folders_folder = self.directory / 'Folders'
        self.file_folders = {}

        self.classify_files_and_folders()

    def classify_files_and_folders(self):
        """
        Classify files and folders in the directory into loose and bound, based on their parent directories.
        """
        # Find all loose files and folders
        loose_files = [file for file in self.directory.glob('*') if file.is_file()]
        loose_folders = [folder for folder in self.directory.glob('*') if
                         folder.is_dir() and folder != self.folders_folder]

        # Create a mapping from file extension to destination folder
        self.file_folders = {file.suffix[1:].upper(): self.directory / f'{file.suffix[1:].upper()} Files' for file in
                             loose_files}

        # Classify loose and bound files
        self.loose_files = {file for file in loose_files if file.suffix[1:].upper() in self.file_folders}
        self.bound_files = {file: file.parent for file in self.directory.rglob('*.*') if
                            file.is_file() and file.parent != self.directory}

        # Save loose folders
        self.loose_folders = loose_folders

    def resolve_duplicate_path(self, path):
        """
        Modify the path to ensure it does not duplicate an existing one.
        """
        if not path.exists():
            return path

        base_path = path.parent / path.stem
        extension = path.suffix
        counter = 1

        while path.exists():
            path = Path(str(base_path) + f"_{counter}" + extension)
            counter += 1

        return path

    def move_files(self):
        """
        Move the loose files to their respective folders.
        """
        for file in self.loose_files:
            classification = file.suffix[1:].upper()
            destination_folder = self.file_folders[classification]
            destination_folder.mkdir(exist_ok=True)
            destination = self.resolve_duplicate_path(destination_folder / file.name)
            shutil.move(str(file), str(destination))

    def move_folders(self):
        """
        Move the loose folders to a central 'Folders' folder.
        """
        for folder in self.loose_folders:
            if folder == self.folders_folder:
                continue
            destination = self.resolve_duplicate_path(self.folders_folder / folder.name)
            shutil.move(str(folder), str(destination))

    def calculate_hash(self, file_path):
        """
        Calculate the MD5 hash of a file.
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def find_and_remove_duplicates(self):
        """
        Find duplicate files based on their MD5 hash and remove them.
        """
        hashes = {}
        duplicates = []
        for folder in tqdm(self.file_folders.values()):
            for file in folder.glob('*'):
                file_hash = self.calculate_hash(file)
                if file_hash in hashes:
                    duplicates.append(file)
                else:
                    hashes[file_hash] = file

        self.prompt_to_delete_duplicates(duplicates)

    def prompt_to_delete_duplicates(self, duplicates):
        """
        Ask the user if they want to delete the duplicate files, and handle their response.
        """
        while True:
            response = input(f"Do you want to delete {len(duplicates)} files? (yes/no/show): ").strip().lower()
            if response == 'yes':
                for file in duplicates:
                    file.unlink()
                break
            elif response == 'no':
                break
            elif response == 'show':
                for file in duplicates:
                    print(file)
            else:
                print("Invalid option. Please enter 'yes', 'no', or 'show'.")

    def sort(self, unique=False):
        """
        The main function that sorts both files and folders.
        If unique is True, it also checks for and removes duplicate files.
        """
        self.move_files()
        self.move_folders()
        if unique:
            self.find_and_remove_duplicates()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Sort files in a specified directory into folders by file type.")
    parser.add_argument('directory', type=str, help="The target directory to sort.")
    parser.add_argument('--unique', action='store_true', help="Remove duplicate files after sorting.")

    args = parser.parse_args()

    sorter = FileSorter(args.directory)
    sorter.sort(unique=args.unique)

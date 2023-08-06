# File Sorter

File Sorter is a simple Python script that organizes files in a specified directory based on their file extensions. It moves the files to their respective folders named after their file extensions. Loose folders will also be moved to a central 'Folders' folder.

## Features

- Classifies files based on their extensions and moves them to corresponding folders.
- Handles duplicate file names by renaming.
- Moves loose folders to a central 'Folders' folder.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jaylann/FolderSorterByFiletype.git
   ```

2. Navigate to the project directory:
   ```bash
   cd FolderSorterByFiletype
   ```

## Usage

You can use the script from the command line by specifying the target directory as an argument:

```bash
python file_sorter.py /path/to/target/directory
```

### Example

If you have a directory with the following structure:

```
Documents/
├── file1.txt
├── file2.pdf
└── Folder1/
```

Running the script on this directory will reorganize it as:

```
Documents/
├── TXT Files/
│   └── file1.txt
├── PDF Files/
│   └── file2.pdf
└── Folders/
    └── Folder1/
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

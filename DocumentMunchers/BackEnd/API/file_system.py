import bm25s
from collections.abc import Sequence
import json
from keywords import KeywordExtractor
import os
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text
import pickle
import platform
import pypdfium2 as pdfium
from PyPDF2 import PdfReader
import shutil
from spire.doc import *
from spire.doc.common import *
import sqlite3
import subprocess
from summarizer import Summarizer
import tkinter as tk
from tkinter import filedialog

# Get platform and user
PLATFORM = platform.system()
UNAME = os.getlogin()

# Construct root dir for save data
if PLATFORM == "Linux":
    MAIN_FOLDER = f"/home/{UNAME}/.local/share/DocumentMunchers"
elif PLATFORM == "Darwin":
    MAIN_FOLDER = f"/Users/{UNAME}/Library/Application/DocumentMunchers"
elif PLATFORM == "Windows":
    MAIN_FOLDER = f"C:\\Users\\f{UNAME}\\AppData\\Roaming\\DocumentMunchers"

# Generate path for the workspace save files
WORKSPACE_FOLDER = os.path.join(MAIN_FOLDER, "workspace_files")
# Make the root if it doesnt exist
if(not os.path.exists(MAIN_FOLDER)):
    os.makedirs(MAIN_FOLDER, exist_ok=True)
# Make the workspace save folder if it doesnt exist
if(not os.path.exists(WORKSPACE_FOLDER)):
    os.makedirs(WORKSPACE_FOLDER, exist_ok=True)

# Hardcoded file names
METADATA_FNAME = "metadata.json"
DB_FNAME = "database.db"
WORKSPACE_FP = os.path.join(WORKSPACE_FOLDER, METADATA_FNAME)
# Implemented file types
VALID_FILE_TYPES = set(["pdf", "docx", "txt", "json", "odt", "pptx", "xlsx", "csv", "ods"])

# Substrings to purge from ingested text
DELIMS = ["(cid:0)"]

"""
Private function, mines pdf documents
@param filepath The filepath of the pdf document to mine
@return The string data mined from the pdf document
"""
def __convert_pdf(filepath) -> str:
    try:
        doc = pdfium.PdfDocument(filepath)
        text_parts = []
        for page in doc:
            textpage = page.get_textpage()
            text = textpage.get_text_range()
            text_parts.append(text)

        text = "\n".join(text_parts)
        doc.close()
        return text
    except Exception as e:
        print(e)
        print(f"Could not mine {filepath}")


"""
From https://medium.com/@alice.yang_10652/extract-text-from-word-documents-with-python-a-comprehensive-guide-95a67e23c35c
Private helper function, mines word documents
@param filepath The filepath of the word document
@return The string data from the word document
"""
def __convert_docx(filepath) -> str:

    # Create a Document object
    document = Document()
    # Load a Word document
    document.LoadFromFile(filepath)

    # Extract the text of the document
    document_text = document.GetText()

    document.Close()

    return document_text

"""
Uses depth first search to get all files under some directory
@param directory The root of the file tree to parse
@param files The list to store paths in
"""
def __directory_dfs(directory:str, files:list):
    # Make sure the user didn't click cancel when choosing a directory
    if directory != '':
        # Iterate through each file in the directory
        for entry in os.listdir(directory):
            # Construct the full path of the file
            full_path = os.path.join(directory, entry)
            # If the filepath points to a directory, recursively search it
            if os.path.isdir(full_path):
                __directory_dfs(full_path, files)
            # Else, its a file, potentially save its path if we want to read it
            else:
                ext = __get_extension(full_path)
                if(ext in VALID_FILE_TYPES):
                    files.append(full_path)

"""
Private helper function, reads in a file as if it is plaintext
@param filepath The filepath of the file to read in
@return The string content of the file
"""
def __convert_generic(filepath) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        doc = f.read()

    return doc

"""
Private helper function, gets the file extension of a filepath
@param filepath The filepath to extract the extension from
@return the file extension
"""
def __get_extension(filepath) -> str:
    return filepath.split(".")[-1]

"""
Reads the file at filepath into a string
@param filepath The filepath to read
@return The string data in the file
"""
def read_file_content(filepath) -> str:
    # Get file extension
    extension = __get_extension(filepath)
    content = ""
    print(f"Mining {filepath}")
    # Pdf mine
    if(extension == "pdf"):
        content = __convert_pdf(filepath)
    # Word Doc mine
    elif(extension == "docx"):
        content = __convert_docx(filepath)
    # Just read the contents in
    else:
        content = __convert_generic(filepath)
    
    for delim in DELIMS:
        content = content.replace(delim, "")

    return content

"""
Opens the file
@param filepath The filepath of the file to open
"""   
def open_with_default_viewer(filepath):
    if not os.path.exists(filepath):
        raise Exception(f"'{filepath}' not found!")
    # https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
    if PLATFORM == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif PLATFORM == 'Windows':    # Windows
        os.startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

"""
Writes to write some object to a file
@param content The content to convert to a string and write to a file
@param filepath The path to write the file to
"""
def write_to_file(content, filepath):
    extension = __get_extension(filepath)
    if(extension == "json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

def does_file_exist(fp) -> bool:
    return os.path.exists(fp)

"""
Gets the time last modified of a file at 'filepath'
@param filepath The filepath to look at
@return The UNIX representation of the last modified date, with the type 'float'
"""
def get_date(filepath) -> float:
    if(not os.path.exists(filepath)):
        return float(-1)
    return os.path.getmtime(filepath)

"""
Checks if a saved date is the same as the last modified date of a file at the given filepath
@param filepath The filepath to look at
@param saved_date The date to check
@return True if the dates match, false else
"""
def is_inconsistent_date(filepath, saved_date) -> bool:
    if(not os.path.exists(filepath)):
        raise Exception(f"'{filepath}' does not exist!")
    actual_date = os.path.getmtime(filepath)
    return float(actual_date) != float(saved_date)

"""
Loads the workspaces into a dictionary
@return The dictionary of workspaces
"""
def load_workspace_metadata():
    last_selected = ""
    if(not os.path.exists(os.path.join(WORKSPACE_FOLDER, METADATA_FNAME))):
        wss = dict()
        with open(WORKSPACE_FP, "w", encoding="utf-8") as f:
            json.dump([wss, last_selected], f, indent=4)
    else:
        with open(WORKSPACE_FP, "r", encoding="utf-8") as f:
            wss, last_selected = json.load(f)
    return wss, last_selected

def write_workspace_metadata(met):
    write_to_file(met, os.path.join(WORKSPACE_FOLDER, METADATA_FNAME))

def get_database_fp():
    return os.path.join(WORKSPACE_FOLDER, DB_FNAME)

def get_bm25s(ws_id):
    try:
        return bm25s.BM25.load(os.path.join(WORKSPACE_FOLDER, f"{ws_id}_indices"), load_corpus=True)
    except:
        return None

def save_bm25s(ws_id, bm25_obj:bm25s.BM25):
    bm25_obj.save(os.path.join(WORKSPACE_FOLDER, f"{ws_id}_indices"))
def delete_bm25s(ws_id):
    shutil.rmtree(os.path.join(WORKSPACE_FOLDER, f"{ws_id}_indices"))
"""
Dumps the workspaces to the workspaces file
@param wss The dictionary of workspaces to write to a file
"""
def dump_workspace_metadata(wss, last_selected):
    with open(WORKSPACE_FP, "w", encoding="utf-8") as f:
        json.dump([wss, last_selected], f, indent=4)
    

"""
Opens a file browser where the user can enter in a directory
to index
@return A list of all the files somewhere under that directory
"""
def ask_user_for_directory():
    files = []
    directory = filedialog.askdirectory()
    __directory_dfs(directory, files)
    return files



class PathIterator(Sequence):
    """A custom list implementation"""
    
    def __init__(self, items=None):
        self._paths:list = list(items) if items else []
        self._summaries:list = []
        self._keywords = []
        self._summarizer = Summarizer()
        self._kw_extractor = KeywordExtractor()
    
    def __getitem__(self, index):
        path = self._paths[index]

        if not os.path.exists(path):
            raise IndexError(f"{path} cannot be indexed")

        content = read_file_content(path)

        large_summary = self._summarizer.summarize(content, max_chars=100000000, num_sentences=20)
        self._keywords.append(self._kw_extractor.get_keywords(large_summary))
        self._summaries.append(large_summary[:200])
        return large_summary
        
    
    def __setitem__(self, index, value):
        if not os.path.exists(value):
            raise FileNotFoundError(f"Invalid filepath {value}")
        self._paths[index] = value
    
    def __delitem__(self, index):
        """Allow item deletion"""
        del self._paths[index]
    
    def __len__(self):
        """Return length"""
        return len(self._paths)
    
    def __repr__(self):
        """String representation"""
        return f"CustomList({self._paths})"
    
    def insert(self, index, value):
        """Insert item at index"""
        self._paths.insert(index, value)
    
    def append(self, value):
        """Add item to the end"""
        self._paths.append(value)
    
    def extend(self, items):
        """Add multiple items"""
        self._paths.extend(items)
    
    def remove(self, value):
        """Remove first occurrence of value"""
        self._paths.remove(value)
    
    def pop(self, index=-1):
        """Remove and return item at index"""
        return self._paths.pop(index)
    
    def clear(self):
        """Remove all items"""
        self._paths.clear()
    
    def index(self, value, start=0, stop=None):
        """Return index of first occurrence"""
        if stop is None:
            return self._paths.index(value, start)
        return self._paths.index(value, start, stop)
    
    def count(self, value):
        """Return number of occurrences"""
        return self._paths.count(value)
    
    def sort(self, key=None, reverse=False):
        """Sort items in place"""
        self._paths.sort(key=key, reverse=reverse)
    
    def reverse(self):
        """Reverse items in place"""
        self._paths.reverse()
    
    def get_summaries(self):
        return self._summaries
    
    def get_keywords(self):
        return self._keywords

    

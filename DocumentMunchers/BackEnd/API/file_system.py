import json
import os
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import pickle
import platform
# from PyPDF2 import PdfFileReader
from PyPDF2 import PdfReader
from spire.doc import *
from spire.doc.common import *
import subprocess
import tkinter as tk
from tkinter import filedialog

WORKSPACE_FP = os.path.dirname(os.path.abspath(__file__)) + "/workspace_files/workspaces.json"
TFIDF_DIR = os.path.dirname(os.path.abspath(__file__)) + "/workspace_files/TFIDFS/"
VALID_FILE_TYPES = set(["pdf", "docx", "txt", "json", "odt", "pptx", "xlsx", "csv", "ods"])

"""
Private function, mines pdf documents
@param filepath The filepath of the pdf document to mine
@return The string data mined from the pdf document
"""
def __convert_pdf(filepath) -> str:
    try:
        with open(filepath, 'rb') as file:
            #pdfFile = PdfFileReader(file)
            pdfFile = PdfReader(file)
            #totalPages = pdfFile.getNumPages()
            totalPages = len(pdfFile.pages)
        content = ""

        # Set paramters of extraction
        laparam = LAParams(detect_vertical=True)
        # get content of pdf
        # Parsing over only a few pages seperately may take longer but uses less memory
        step = 3
        for pg in range(0, totalPages, step):
            content += extract_text(filepath, page_numbers=list(range(pg, pg+step)), laparams=laparam)

        # Check length of content, exclude entries with less than 200 characters
        if len(content) < 200:
            raise Exception
        else:
        ## Output to file:
            return content
    except Exception as e:
        print(e)
        print(f"Could not mine '{filepath}'")

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
    # Pdf mine
    if(extension == "pdf"):
        return __convert_pdf(filepath)
    # Word Doc mine
    elif(extension == "docx"):
        return __convert_docx(filepath)
    # Just read the contents in
    else:
        return __convert_generic(filepath)

"""
Opens the file
@param filepath The filepath of the file to open
"""   
def open_with_default_viewer(filepath):
    if not os.path.exists(filepath):
        raise Exception(f"'{filepath}' not found!")
    # https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
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

"""
Gets the time last modified of a file at 'filepath'
@param filepath The filepath to look at
@return The UNIX representation of the last modified date, with the type 'float'
"""
def get_date(filepath) -> float:
    if(not os.path.exists(filepath)):
        raise Exception(f"'{filepath}' does not exist!")
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
def load_workspaces() -> dict:
    last_selected = ""
    # If the workspaces file doesn't exist, create it
    if(not os.path.exists(WORKSPACE_FP)):
        wss = dict()
        # Ensure fp exists
        with open(WORKSPACE_FP, "w", encoding="utf-8") as f:
            json.dump([wss, last_selected], f, indent=4)
    # If the file does exist, load it
    else:
        with open(WORKSPACE_FP, "r", encoding="utf-8") as f:
            wss, last_selected = json.load(f)
    # Return the loaded contents
    return wss, last_selected

"""
Dumps the workspaces to the workspaces file
@param wss The dictionary of workspaces to write to a file
"""
def dump_workspaces(wss, last_selected):
    with open(WORKSPACE_FP, "w", encoding="utf-8") as f:
        json.dump([wss, last_selected], f, indent=4)

"""
Takes a tfidf table and dumps it to a binary
@param output_fp The filepath to write the binary to
@param obj The tfidf table to dump
"""
def pickle_tfidf(output_fp, obj):
    if(not os.path.exists(TFIDF_DIR)):
        os.mkdir(TFIDF_DIR)
    with open(f"{TFIDF_DIR}{output_fp}", "wb") as f:
        pickle.dump(obj, f)

"""
Loads a tfidf table binary from the passed filepath
@param output_fp The filepath the tfidf table was written to
@return The loaded contents of the binary
"""
def unpickle_tfidf(output_fp):
    with open(f"{TFIDF_DIR}{output_fp}", "rb") as f:
        obj = pickle.load(f)
    return obj

"""
Opens a file browser where the user can enter in a directory
to index
@return A list of all the files somewhere under that directory
"""
def ask_user_for_directory():
    files = []
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    __directory_dfs(directory, files)
    return files
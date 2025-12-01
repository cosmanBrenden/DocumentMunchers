# Document Munchers
> 📢*Latest Update:*
> 1. AI summarization for files.
> 2. Workspaces for compartmentalizing collections of files the program is indexing.
> 3. Made the UI more responsive.
> 4. Bug Fixes:
>> All background processes properly terminate.
>> The program no longer crashes when attempting to make a search without selecting a workspace, instead bringing the user to an empty search page.
>> Fixed some CSS formatting issues.
>> Users can now open the file selection menu multiple times per session.

## 📝 Description
Document Munchers is an AI file search engine that helps you find the exact file that you are looking for on your computer. If you do not remember the title of the file, you can describe what the file is about to the AI search engine, and it will search through your files and give you files that are the most relevant to your query. Worried about your privacy, don't! The entire program runs entirely locally, so nothing ever leaves your computer.

## 🌟 Provided Features
1. Semantic search based on the text content of files.
2. Workspaces to compartmentalize what files are indexed by the software.
3. Summarization of file contents.
4. Keywords derived from the contents of files.
5. Cross-platform availability (Windows, MacOS, Linux).

## 🔎 Getting Started

* Ensure that you have the most recent version of Python installed: 
    * macOS: https://www.python.org/downloads/macos/
    * Linux, ensure you are a super-user and run the following: 
        * For Debian/Ubuntu: ```sudo apt install python3```
        * For Fedora: ```sudo dnf install python3```
        * For Arch/SteamOS: ```sudo pacman -S python3```
    * Windows: https://www.python.org/downloads/windows/

* Ensure that pip is installed:
    * macOS, run the following in your terminal: ```python3 get-pip.py```
    * Linux, ensure you are a super-user and run the following:
        * For Debian/Ubuntu: ```sudo apt install python3-pip```
        * For Fedora: ```sudo dnf install python3-pip```
        * For Arch/SteamOS: ```sudo pacman -S python3-pip```
    * Windows, run the following in your terminal: ```python get-pip.py```

* In the terminal, navigate to the main directory ./DocumentMunchers/

* Depending on the platform, run the following script to install all required dependencies:
    * macOS:  ```./setup.zsh```
    * Linux:  ```./setup.sh```
    * Windows:  ```./setup.bat```

* Next, run one of the following scripts to start the program:
    * macOS:  ```./run.zsh```
    * Linux:  ```./run.sh```
    * Windows:  ```./run.bat```

* A window will open displaying the program's home page



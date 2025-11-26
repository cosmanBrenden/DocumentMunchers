from datetime import datetime
import time

import file_system
from semantic_similarity import Similarity
from subscribers import BasicSubscriber
from summarizer import Summarizer
from tf_idf import TFIDF

DUMP_DELTA = 300

class Database:
    """
    Manages the files and workspaces for the program
    Format of self.workspaces:
    {
        ws1:{
            files: {
                fp1: {
                    ai: T | F
                    summary: str | None
                    tfidf: {
                        data
                        ...
                    }
                    date_modified: float
                    id: int
                }
                ...
            }
            search_history: [
                ...
            ]
            file_history: [
                ...
            ]
            name: str
            description: str
        }
        ...
    }
    @param similarity The similarity object for search queries
    @param summarizer The summarizer object to use for file summarization, default=None
    """
    def __init__(self, similarity:Similarity, summarizer:Summarizer=None):
        self.workspaces, last_selected = self.__load()
        self.current_ws_id = None
        self.summarizer = summarizer
        self.similarity = similarity
        self.subscribers = dict()
        self.last_dump = 0

        # Shouldn't throw an exception
        if(last_selected):
            self.select_workspace(last_selected)

    """
    Loads the workspaces from a file
    """
    def __load(self) -> dict:
        wss, last_selected = file_system.load_workspaces()
        # Recombine every tfidif vectorizer
        for ws_key in wss.keys():
            files = wss[ws_key]["files"]
            for fp in files:
                curr_file = files[fp]
                output_fp = curr_file["tfidf"]
                if output_fp != None:
                    tfidf_dat = file_system.unpickle_tfidf(output_fp)
                    tfidf = TFIDF(vectorizer_data=tfidf_dat)
                    curr_file["tfidf"] = tfidf
        
        return wss, last_selected
    """
    Dump the workspaces to a file
    """
    def dump_workspaces(self):
        # Copy all the workspaces
        wss = self.workspaces.copy()
        # Go thru each workspace, rip appart every vectorizer
        for ws_key in wss.keys():
            curr_ws = wss[ws_key].copy()
            files = curr_ws["files"].copy()
            for fp in files:
                curr_file = files[fp].copy()
                tfidf = curr_file["tfidf"]
                if tfidf != None:
                    temp = tfidf.export()
                    output_fp = f"{ws_key}_{curr_file['id']}"
                    curr_file["tfidf"] = output_fp
                    file_system.pickle_tfidf(output_fp, temp)
                files[fp] = curr_file
            curr_ws["files"] = files
            wss[ws_key] = curr_ws

        # Take a dump
        file_system.dump_workspaces(wss, self.current_ws_id)
        self.__notify_subscribers("Dump workspaces.")
        self.last_dump = time.time()

    """
    Checks if the workspace should be dumped, default every 5 minutes
    @return True if should dump, False else
    """
    def should_dump(self):
        return self.last_dump + DUMP_DELTA < time.time()
    
    """
    Preprocesses all the files indexed by a workspace
    @param ws_id The id of the workspace to index
    """
    def preprocess(self, ws_id):
        # Raise an exception if the workspace doesn't exist
        if(not ws_id in self.workspaces.keys()):
            raise Exception(f"Workspace '{ws_id}' does not exist, cannot preprocess it!")
        # Update subscribers about the preprocessing begining
        self.__notify_subscribers(f"Starting preprocessing of '{ws_id}'")
        # Get the workspace out
        curr_ws = self.workspaces[ws_id]
        # Iterate through all files
        for fp in curr_ws["files"].keys():
            # Update subscribers about what file is being processed
            self.__notify_subscribers(f"Processing {fp}...")
            # Get the file out
            file = curr_ws["files"][fp]
            # If there is a summary and there shouldn't be, remove it
            if(not file["ai"] and file["summary"] != None):
                file["summary"] = None
            # Copy the last modified date
            saved_date = file["date_modified"]
            # If the last modified date we have saved is different from the actual date in the os, reprocess
            if(file_system.is_inconsistent_date(fp, saved_date)):
                # Get the real date
                file["date_modified"] = file_system.get_date(fp)
                # Read the file content in
                file_content = file_system.read_file_content(fp)
                # If there should be summarization, summarize the file
                if(file["ai"] and self.summarizer != None):
                    self.__notify_subscribers(f"Summarizing {fp}...")
                    file["summary"] = self.summarizer.summarize(file_content)
                else:
                    
                    file["summary"] = None
                # Fit a tfidf table
                file["tfidf"] = TFIDF(document=file_content)
            # Notifiy subs that file is done
            self.__notify_subscribers(f"Done processing {fp}...")
        # Notify subs that the ws is done
        self.__notify_subscribers(f"Finished preprocessing of '{ws_id}'")

        
    """
    Getter for workspace ids
    @return The set of workspace ids
    """
    def get_workspace_ids(self):
        return set(self.workspaces.keys())
    
    """
    Returns the name, description, and number of files indexed by a workspace at "ws_id".
    Used for when all info is not needed
    @param ws_id The id of the workspace to get the info of
    @return The above listed info
    """
    def get_workspace_info(self, ws_id: str):
        # Raise an exception if the workspace doesn't exist
        if(not ws_id in self.workspaces.keys()):
            raise Exception(f"'{ws_id}' does not exist, cannot get its info!")
        # Get the workspace out
        ws = self.workspaces[ws_id]
        # Return info
        return {
            "name": ws["name"],
            "description":ws["description"],
            "num_files": len(ws["files"].keys())
        }

    """
    Returns the entire workspace at 'ws_id'
    @param ws_id The id of the workspace desired
    @return The workspace at 'ws_id'
    """
    def get_entire_workspace(self, ws_id:str):
        if(not ws_id in self.workspaces.keys()):
            raise Exception(f"'{ws_id}' does not exist, cannot get its info!")
        
        curr = self.workspaces[ws_id]
        filepaths = []

        for fp in curr["files"].keys():
            filepaths.append((fp, curr["files"][fp]["ai"]))
        
        return {
            "name":curr["name"],
            "description":curr["description"],
            "filepaths":filepaths,
            "id":ws_id
        }

    
    """
    Selects the current workspace to act upon
    @param ws_id The name of the workspace to act upon
    @raises Exception If 'ws_id' does not exist
    """
    def select_workspace(self, ws_id):
        if not ws_id in self.workspaces.keys():
            raise Exception(f"Workspace '{ws_id}' does not exist, cannot select it!")
        self.__notify_subscribers(f"Selecting '{ws_id}' as the current workspace.")
        self.current_ws_id = ws_id
        self.preprocess(ws_id)

    """
    Generates a unique workspace id to based off of a workspace name
    @param workspace_name The name to generate the id based on
    @return The new workspace id
    """
    def generate_ws_id(self, workspace_name:str):
        # If the name is too short to truncate, init id as raw name
        if len(workspace_name) < 7:
            ws_id = workspace_name
        # If its long enough to truncate, truncate it
        else:
            ws_id = workspace_name[:3] + "_" + workspace_name[len(workspace_name) - 3:]
        
        # Gets the current day of the month as an int to string
        day_str = str(datetime.fromtimestamp(round(time.time())).day)
        # Gets the current month as an int to string
        month_str = str(datetime.fromtimestamp(round(time.time())).month)

        # Append the month and day to the id
        ws_id += month_str + day_str

        # If that id already exists, add a suffix
        if(ws_id in self.workspaces.keys()):
            ws_id += "-2"

        # If for some reason that didn't work, keep trying suffixes until one works
        count = 3
        while(ws_id in self.workspaces.keys()):
            # Remove suffix
            ws_id = ws_id[:len(ws_id)-( len(str(count)) + 1)]
            # Add new suffix
            ws_id += f"-{count}"
            # Increment count
            count += 1
        
        self.__notify_subscribers(f"Generated id '{ws_id}'")

        return ws_id
        
    
    """
    Adds a workspace
    @param ws_id The workspace's name to add
    @param filepaths A list of tuples with the filepath, and t/f of whether it should
    be summarized
    """
    def add_workspace(self, ws_id:str, filepaths:list[tuple[str,bool]], name:str, description:str):
        self.__notify_subscribers(f"Adding workspace '{ws_id}'")
        # Init new workspace
        ws = {
            "files": dict(),
            "search_history": [], # TODO: Search and file history stuff
            "file_history": [],
            "name": name,
            "description":description
        }
        # Iterate thru each filepath
        for i in range(len(filepaths)):
            fp, ai = filepaths[i]
            # If the added workspace exists already, and the filepath was already indexed,
            # copy what info can be copied
            if(ws_id in self.workspaces.keys() and fp in self.workspaces[ws_id]["files"].keys()):
                ws["files"].update({fp:{
                    "ai":ai,
                    "summary":self.workspaces[ws_id]["files"][fp]["summary"],
                    "tfidf":self.workspaces[ws_id]["files"][fp]["tfidf"],
                    "date_modified":self.workspaces[ws_id]["files"][fp]["date_modified"],
                    "id":i
                }})
            # If there should be a new entry, make it
            else:   
                ws["files"].update({fp:{
                    "ai":ai,
                    "summary":None,
                    "tfidf":None,
                    "date_modified":0, # Will guarantee that this file gets processed, as today > jan 1st, 1970
                    "id":i
                }})

        # Add workspace to list of workspaces
        self.workspaces.update({ws_id:ws})
        # Preprocess
        self.preprocess(ws_id)
        self.__notify_subscribers(f"Added workspace '{ws_id}'")
        self.dump_workspaces()

    """
    Removes the workspace at "ws_id"
    @param ws_id The id of the workspace to remove
    """
    def remove_workspace(self, ws_id: str):
        # Raise exception if the workspace id is not an existing id
        if(not ws_id in self.workspaces.keys()):
            raise Exception(f"'{ws_id}' does not exist, cannot select it!")
        # Ensure that if the current workspace is the one to remove, deselect it
        if(self.current_ws_id == ws_id):
            self.current_ws_id = None
        # Remove the workspace
        self.workspaces.pop(ws_id)

        self.__notify_subscribers(f"Removed workspace '{ws_id}'")
        self.dump_workspaces()
        

    """
    Gets a list of search results based on the query, sorted in descending order
    of relevance score
    @param query The search query to generate results from
    @param num_results The number of results to return, default=20
    """
    def get_search_results(self, query:str, num_results=20):
        if self.current_ws_id == None:
            raise Exception("No workspace selected!")
        
        self.__notify_subscribers(f"Making search '{query}'")

        curr_ws = self.workspaces[self.current_ws_id]

        sim_pairs = []
        for file in curr_ws["files"].keys():
            curr_file = curr_ws["files"][file]
            res = self.similarity.get_similarity(query, curr_file)
            file_info = {
                    "summary": curr_file["summary"],
                    "keywords":curr_file["tfidf"].get_keywords(),
                    "date_modified": curr_file["date_modified"],
                    "id": curr_file["id"]
            }
            sim_pairs.append([file, file_info, str(res)])

        sim_pairs = sorted(sim_pairs, key=lambda x: x[2])
        sim_pairs.reverse()

        self.__notify_subscribers(f"Made search '{query}'")
        
        return sim_pairs[:num_results]
    
    """
    Add a subscriber.
    @param subscriber The subscriber to add
    @param s_id The id to associate the subscriber with
    """
    def add_subscriber(self, subscriber:BasicSubscriber, s_id:str):
        self.subscribers.update({s_id:subscriber})
        self.__notify_subscribers(f"Added subscriber '{s_id}'")
    """
    Remove a subscriber
    @param s_id The id of the subscriber to remove
    """
    def remove_subscriber(self, s_id:str):
        if(s_id in self.subscribers.keys()):
            self.subscribers.pop(s_id)
            self.__notify_subscribers(f"Removed subscriber '{s_id}'")
    
    """
    Private method, updates all subscribers
    @param message The message to pass along
    """
    def __notify_subscribers(self, message:str):
        for s_id in self.subscribers.keys():
            subscr:BasicSubscriber = self.subscribers[s_id]
            subscr.update(message)
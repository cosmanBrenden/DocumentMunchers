from datetime import datetime
import time
import sqlite3
import file_system
from subscribers import BasicSubscriber
import bm25s
import Stemmer
from embedding_model import Embedding_Model

DUMP_DELTA = 300
BACKLOG_SUB_ID = "backlog"

class Database:
    """
    Manages the files and workspaces for the program
    Format of self.workspace_metadata:
    {
        ws1:{
            files: {
                fp1: {
                    ai: T | F
                    summary: str | None
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
    def __init__(self, emb_model:Embedding_Model):
        # self.workspace_metadata, last_selected = file_system.load_workspaces()
        # self.current_ws_id = None
        # self.summarizer = summarizer
        # self.similarity = similarity
        # self.subscribers = dict()
        # self.last_dump = 0
        # self.curr_bm25_obj = None

        # Load metadata from json
        self.workspace_metadata, last_selected = file_system.load_workspace_metadata()
        # self.similarity = similarity
        # Build subscriber dictionary
        self.subscribers = dict()
        # Initialize timestamp for the last time the database has been dumped
        self.last_dump = 0
        # Initialize the current bm25s object
        self.curr_bm25_obj = None
        # Initalize stemmer
        self.stemmer = Stemmer.Stemmer("english")
        # Initialize the embedding model
        self.emb_model = emb_model

        # Connect to the database
        database_fp = file_system.get_database_fp()
        self.con = sqlite3.connect(database_fp)
        self.cur = self.con.cursor()
        self.current_ws_id = ""
        self.is_preproc = False

        self.add_subscriber(BasicSubscriber(), BACKLOG_SUB_ID)

        # Shouldn't throw an exception
        if(last_selected != "" and (not last_selected is None)):
            self.__notify_subscribers(f"The last workspace used was {last_selected}")
            self.select_workspace(last_selected)

    # """
    # Loads the workspaces from a file
    # """
    # def __load(self) -> dict:
    #     wss, last_selected = file_system.load_workspaces()
    #     # Recombine every tfidif vectorizer
    #     for ws_key in wss.keys():
    #         files = wss[ws_key]["files"]
    #         for fp in files:
    #             curr_file = files[fp]
    #             output_fp = curr_file["tfidf"]
    #             if output_fp != None:
    #                 tfidf_dat = file_system.unpickle_tfidf(output_fp)
    #                 tfidf = TFIDF(vectorizer_data=tfidf_dat)
    #                 curr_file["tfidf"] = tfidf
    
    def get_is_preprocessing(self):
        return self.is_preproc

    """
    Close the connection to the database
    """
    def close(self):
        self.con.close()
        self.con = None
        self.cur = None

    #     return wss, last_selected
    """
    Dump the workspaces to a file
    """
    def dump_workspaces(self):
        # Copy all the workspaces
        # wss = self.workspace_metadata.copy()
        # # Go thru each workspace, rip appart every vectorizer
        # for ws_key in wss.keys():
        #     curr_ws = wss[ws_key].copy()
        #     files = curr_ws["files"].copy()
            # for fp in files:
            #     curr_file = files[fp].copy()
            #     tfidf = curr_file["tfidf"]
            #     if tfidf != None:
            #         temp = tfidf.export()
            #         output_fp = f"{ws_key}_{curr_file['id']}"
            #         curr_file["tfidf"] = output_fp
            #         file_system.pickle_tfidf(output_fp, temp)
            #     files[fp] = curr_file
            # curr_ws["files"] = files
            # wss[ws_key] = curr_ws

        # Take a dump
        file_system.dump_workspace_metadata(self.workspace_metadata, self.current_ws_id)
        if (self.current_ws_id is not None) and (self.current_ws_id != ""):
            file_system.save_bm25s(self.current_ws_id, self.curr_bm25_obj)
        self.__notify_subscribers("Dumped workspaces.")
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
    def preprocess(self, ws_id, files=None):
        self.is_preproc = True
        print(f"Files is {files}")
        # # Raise an exception if the workspace doesn't exist
        # if(not ws_id in self.workspace_metadata.keys()):
        #     raise Exception(f"Workspace '{ws_id}' does not exist, cannot preprocess it!")
        # # Update subscribers about the preprocessing beginning
        # self.__notify_subscribers(f"Starting preprocessing of '{ws_id}'")
        # # Get the workspace out
        # curr_ws = self.workspace_metadata[ws_id]
        # # Iterate through all files
        # for fp in curr_ws["files"].keys():
        #     # Update subscribers about what file is being processed
        #     self.__notify_subscribers(f"Processing {fp}...")
        #     # Get the file out
        #     file = curr_ws["files"][fp]
        #     # If there is a summary and there shouldn't be, remove it
        #     if(not file["ai"] and file["summary"] != None):
        #         file["summary"] = None
        #     # Copy the last modified date
        #     saved_date = file["date_modified"]
        #     # If the last modified date we have saved is different from the actual date in the os, reprocess
        #     if(file_system.is_inconsistent_date(fp, saved_date)):
        #         # Get the real date
        #         file["date_modified"] = file_system.get_date(fp)
        #         # Read the file content in
        #         file_content = file_system.read_file_content(fp)
        #         # If there should be summarization, summarize the file
        #         if(file["ai"] and self.summarizer != None):
        #             self.__notify_subscribers(f"Summarizing {fp}...")
        #             file["summary"] = self.summarizer.summarize(file_content)
        #         else:
                    
        #             file["summary"] = None
        #         # Fit a tfidf table
        #         file["tfidf"] = TFIDF(document=file_content)
        #     # Notifiy subs that file is done
        #     self.__notify_subscribers(f"Done processing {fp}...")
        # # Notify subs that the ws is done
        # self.__notify_subscribers(f"Finished preprocessing of '{ws_id}'")
        if(not ws_id in self.workspace_metadata.keys()):
            raise Exception(f"Workspace '{ws_id}' does not exist, cannot preprocess it!")
        
        should_preproc = True

        # If no files were passed to the method, query the database for a list
        if(files is None):
            try:
                self.cur.execute(f"""
                select filepath from index_file where ws_id = ? order by indx asc;
                """, (ws_id,))
                files_raw = self.cur.fetchall()
                files_raw = [x[0] for x in files_raw]
                should_preproc = False
                for f in files_raw:
                    self.cur.execute("""
                        select date_modified from files where filepath = ?;
                    """, (f,))
                    rec_date = self.cur.fetchone()
                    rec_date = int(rec_date[0])
                    act_date = int(file_system.get_date(f))
                    if(act_date > rec_date or act_date == -1):
                        print(f"Found old file {f}")
                        should_preproc = True

            except:
                should_preproc = True
                files_raw = []
        # If files were passed, make a shallow copy of the list
        else:
            files_raw = files.copy()
        files = []


        if(not should_preproc and len(files_raw) != 0):
            self.is_preproc = False
            self.curr_bm25_obj = file_system.get_bm25s(ws_id)
            return
        
            

        # Delete all indices from the workspace
        self.cur.execute("""
            delete from index_file where ws_id = ?;
        """, (ws_id, ))
        # Delete all file metadata from files in
        self.cur.executemany("""
            delete from files where filepath = ?;
        """, [(x,) for x in files_raw])
        self.con.commit()
        # Ensure all files exist
        for i in range(len(files_raw)):
            curr_file = files_raw[i]
            if file_system.does_file_exist(curr_file):
                files.append(curr_file)

        self.__notify_subscribers(f"Starting preprocessing of '{ws_id}'")
        
        # Build iterator for the corpus
        iterator = file_system.PathIterator(files)
        # Tokenize corpus with iterator
        tokens = bm25s.tokenize(iterator, stopwords="en", stemmer=self.stemmer)
        # Make the bm25s object
        bm25_obj = bm25s.BM25()
        # Index the corpus with it
        bm25_obj.index(tokens)
        # Save bm25 obj
        self.curr_bm25_obj = bm25_obj
        # Get the summaries out of the iterator
        summaries = iterator.get_summaries()
        # Get the keyword lists out of the iterator
        keyword_lists = iterator.get_keywords()
        keyword_lists = ["|".join(ls) for ls in keyword_lists]

        # Insert files into database
        rows = [(
            files[i], 
            summaries[i], 
            int(file_system.get_date(files[i])), 
            keyword_lists[i]
            ) for i in range(len(files))]
        self.cur.executemany("""
            insert or replace into files (filepath, summary, date_modified, keywords)
            values (?, ?, ?, ?);
            """,
        rows)
        # Insert indices into database
        rows=[(
            ws_id,
            i,
            files[i]
        ) for i in range(len(files))]
        self.cur.executemany("""
            insert or replace into index_file (ws_id, indx, filepath)
            values (?, ?, ?);
        """, rows)

        self.con.commit()

        self.is_preproc = False
        
        

        
    """
    Getter for workspace ids
    @return The set of workspace ids
    """
    def get_workspace_ids(self):
        return set(self.workspace_metadata.keys())
    
    """
    Returns the name, description, and number of files indexed by a workspace at "ws_id".
    Used for when all info is not needed
    @param ws_id The id of the workspace to get the info of
    @return The above listed info
    """
    def get_workspace_info(self, ws_id: str):
        # Raise an exception if the workspace doesn't exist
        if(not ws_id in self.workspace_metadata.keys()):
            raise Exception(f"'{ws_id}' does not exist, cannot get its info!")
        # Get the workspace out
        ws = self.workspace_metadata[ws_id]

        # Return info
        return ws

    """
    Returns the entire workspace at 'ws_id'
    @param ws_id The id of the workspace desired
    @return The workspace at 'ws_id'
    """
    def get_entire_workspace(self, ws_id:str):
        if(not ws_id in self.workspace_metadata.keys()):
            raise Exception(f"'{ws_id}' does not exist, cannot get its info!")
        
        curr = self.workspace_metadata[ws_id]
        
        self.cur.execute("""
            select filepath from index_file where ws_id = ? order by indx asc;
        """, (ws_id, ))
        filepaths = self.cur.fetchall()
        filepaths = [fp[0] for fp in filepaths]
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
        if not ws_id in self.workspace_metadata.keys():
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


        # If for some reason that didn't work, keep trying suffixes until one works
        count = 2
        while(ws_id in self.workspace_metadata.keys()):
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
    def add_workspace(self, ws_id:str, filepaths:list[str], name:str, description:str):
        
        # Init new workspace
        # ws = {
        #     "files": dict(),
        #     "search_history": [], # TODO: Search and file history stuff
        #     "file_history": [],
        #     "name": name,
        #     "description":description
        # }
        try:
            self.remove_workspace(ws_id)
            self.__notify_subscribers(f"Overwriting workspace '{ws_id}'")
        except:
            self.__notify_subscribers(f"Adding workspace '{ws_id}'")
        metadata = {
            "name": name,
            "description":description,
            "num_files":len(filepaths)
        }
        # # Iterate thru each filepath
        # for i in range(len(filepaths)):
        #     fp, ai = filepaths[i]
        #     # If the added workspace exists already, and the filepath was already indexed,
        #     # copy what info can be copied
        #     if(ws_id in self.workspace_metadata.keys() and fp in self.workspace_metadata[ws_id]["files"].keys()):
        #         ws["files"].update({fp:{
        #             "ai":ai,
        #             "summary":self.workspace_metadata[ws_id]["files"][fp]["summary"],
        #             "date_modified":self.workspace_metadata[ws_id]["files"][fp]["date_modified"],
        #             "id":i
        #         }})
        #     # If there should be a new entry, make it
        #     else:   
        #         ws["files"].update({fp:{
        #             "ai":ai,
        #             "summary":None,
        #             "date_modified":0, # Will guarantee that this file gets processed, as today > jan 1st, 1970
        #             "id":i
        #         }})


        """
        create table if not exists index_file (
            ws_id text, 
            indx integer, 
            filepath text, 
            primary key (ws_id, indx), 
            foreign key (filepath) references files(filepath)
        );

        create table if not exists files (
            filepath text, 
            summary text, 
            date_modified integer,
            keywords text, 
            primary key (filepath)
        );
        """
        # self.cur.execute(f'''
        #     create table if not exists {ws_id} (
        #         indx integer,
        #         filepath text,
        #         primary key (indx),
        #         foreign key (filepath) references files(filepath),
        #     );
        # ''')
        self.cur.execute("""
            create table if not exists index_file (
                ws_id text, 
                indx integer, 
                filepath text, 
                primary key (ws_id, indx), 
                foreign key (filepath) references files(filepath)
            );
        """)
        self.cur.execute("""
            create table if not exists files (
                filepath text, 
                summary text, 
                date_modified integer,
                keywords text, 
                primary key (filepath)
            );
        """)
        self.con.commit()
        # Add workspace to list of workspaces
        self.workspace_metadata.update({ws_id:metadata})
        # Preprocess
        print(f"ws_id: {ws_id}")
        self.preprocess(ws_id, files=filepaths)
        self.current_ws_id = ws_id
        self.__notify_subscribers(f"Added workspace '{ws_id}'")
        self.dump_workspaces()

    """
    Removes the workspace at "ws_id"
    @param ws_id The id of the workspace to remove
    """
    def remove_workspace(self, ws_id: str):
        # Raise exception if the workspace id is not an existing id
        if(not ws_id in self.workspace_metadata.keys()):
            raise Exception(f"'{ws_id}' does not exist, cannot select it!")
        # Ensure that if the current workspace is the one to remove, deselect it
        if(self.current_ws_id == ws_id):
            self.current_ws_id = None
        # Remove the workspace
        self.workspace_metadata.pop(ws_id)


        self.cur.execute("""
            delete from index_file where ws_id = ?;
        """, (ws_id, ))

        self.con.commit()

        self.cur.execute("""
            delete from files where filepath not in (select filepath from index_file);
        """)

        self.con.commit()

        file_system.delete_bm25s(ws_id)

        self.curr_bm25_obj = None

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
            return []
        
        self.__notify_subscribers(f"Making search '{query}'")

        # curr_ws = self.workspace_metadata[self.current_ws_id]


        """

        create table if not exists index_file (
            ws_id text, 
            indx integer, 
            filepath text, 
            primary key (ws_id, indx), 
            foreign key (filepath) references files(filepath)
        );

        create table if not exists files (
            filepath text, 
            summary text, 
            date_modified integer,
            keywords text, 
            primary key (filepath)
        );
        """
        self.cur.execute("""
            SELECT index_file.indx, files.filepath, files.summary, files.date_modified, files.keywords
            FROM index_file
            JOIN files ON index_file.filepath = files.filepath
            WHERE index_file.ws_id = ?
        """, (self.current_ws_id,))

        rows = self.cur.fetchall()
        rows = [(indx, filepath, summary, date_modified, keywords.split("|")) 
            for indx, filepath, summary, date_modified, keywords in rows]
        rows = sorted(rows, key=lambda x: x[0])
        rows = [(filepath, summary, date_modified, keywords)
            for indx, filepath, summary, date_modified, keywords in rows]
        sim_pairs = []
        query_tokens = bm25s.tokenize(query, stemmer=self.stemmer)
        results, scores = self.curr_bm25_obj.retrieve(query_tokens, k=len(rows))
        div = scores[0,0]
        if(scores[0,0] == 0):
            div = 1
        calced_scores = []
        for i in range(results.shape[1]):
            doc, bm_score = results[0, i], scores[0, i]/div
            summ = rows[doc][1]
            em_score = self.emb_model.embedded_similarity(gt=summ, actual=query)
            total_score = (bm_score + em_score) / 2
            calced_scores.append((doc, f"{float(total_score)}"))

        calced_scores = sorted(calced_scores, key=lambda x: x[1])
        calced_scores.reverse()

        sim_pairs = []

        for i in range(min(len(calced_scores), num_results)):
            curr_indx, score = calced_scores[i]
            filepath, summary, date_modified, keywords = rows[curr_indx]
            file_info = {
                "summary": summary,
                "keywords": keywords,
                "date_modified": date_modified,
                "id": f"{curr_indx}"
            }
            sim_pairs.append([filepath, file_info, score])
        
        # for i in range(len(rows)):
        #     filepath, summary, date_modified, keywords = rows[i]


        #     if curr_file["tfidf"]:
        #         res = self.similarity.get_similarity(query, curr_file)
        #         file_info = {
        #                 "summary": curr_file["summary"],
        #                 "keywords":curr_file["tfidf"].get_keywords(),
        #                 "date_modified": curr_file["date_modified"],
        #                 "id": curr_file["id"]
        #         }
        #         sim_pairs.append([file, file_info, str(res)])

        # sim_pairs = sorted(sim_pairs, key=lambda x: x[2])
        # sim_pairs.reverse()

        self.__notify_subscribers(f"Made search '{query}'")
        
        return sim_pairs[:num_results]
    
    """
    Add a subscriber.
    @param subscriber The subscriber to add
    @param s_id The id to associate the subscriber with
    """
    def add_subscriber(self, subscriber:BasicSubscriber, s_id:str):
        self.subscribers.update({s_id:subscriber})
        if(BACKLOG_SUB_ID in self.subscribers.keys()):
            backlog:BasicSubscriber = self.subscribers[BACKLOG_SUB_ID]
            temp = []
            while(backlog.has_update()):
                temp.append(backlog.get_oldest_update(with_timestamp=False))
            for t in temp:
                subscriber.update(t)
                backlog.update(t)
            
        self.__notify_subscribers(f"Added subscriber '{s_id}'")
    """
    Remove a subscriber
    @param s_id The id of the subscriber to remove
    """
    def remove_subscriber(self, s_id:str):
        if(s_id in self.subscribers.keys()):
            self.subscribers.pop(s_id)
            self.__notify_subscribers(f"Removed subscriber '{s_id}'")
    
    def purge_backlog_sub(self):
        self.remove_subscriber(BACKLOG_SUB_ID)

    """
    Private method, updates all subscribers
    @param message The message to pass along
    """
    def __notify_subscribers(self, message:str):
        for s_id in self.subscribers.keys():
            subscr:BasicSubscriber = self.subscribers[s_id]
            subscr.update(message)
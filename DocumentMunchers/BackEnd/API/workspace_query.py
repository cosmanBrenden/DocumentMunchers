from database import Database

"""
Correct input format
{
    "sort_by":"name"|"num_files"|"description",
    "action":"list_workspaces"
}
Example input from the FrontEnd
{"type":"workspace_query", "content":{"action":"list_workspaces", "sort_by": "name"}}
"""
def __list_workspaces(content:dict, database:Database):
    ids = database.get_workspace_ids()
    workspaces_info = []
    for ws_id in ids:
        curr = database.get_workspace_info(ws_id)
        curr.update({"id": ws_id})
        workspaces_info.append(curr)
    
    try:
        sort_by = content["sort_by"]
        workspaces_info = sorted(workspaces_info, key=lambda x : x[sort_by])
    except:
        workspaces_info = sorted(workspaces_info, key=lambda x : x["name"])

    return workspaces_info
    
"""
Correct input format
{
    "action": "open_workspace",
    "id": "some-id"
}
Example input from the FrontEnd
{"type":"workspace_query", "content":{"action":"open_workspace", "id":"ws1"}}
"""
def __open_workspace(content:dict, database:Database):
    if not "id" in content.keys():
        raise Exception("No id supplied!")
    
    ws_id = content["id"]
    # Will raise an exception if the id is invalid
    ws = database.get_entire_workspace(ws_id)
    return ws

"""
Correct input format
{
    "action": "add_workspace",
    ""
}
Example input form the FrontEnd
{
  "content": {
    "data": {
        "description": "Bungus",
        "filepaths": [
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Simon-CanadianInuitgoing-2011.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/BANNISTER-AtlanticCanadaAtlantic-2014.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Nelles-SocialHistoryCanada-1976.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Sarkonak-BriefChronologyFrench-1983.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Clare-OralHistoryCanada-1973.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Kozyrskyj-HISTORYPUBLICHEALTH-1996.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Bryant-HistoricalEmpathyCanada-2006.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Robidoux-ImaginingCanadianIdentity-2002.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Rich-CanadianHistory-1971.pdf",
            true
        ],
        [
            "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/DocumentMunchers/BackEnd/API/test_files/Hartland-FactorsEconomicGrowth-1955.pdf",
            true
        ]
        ],
        "id": "ws1",
        "name": "Fungus"
    },
    "action":"add_workspace"
  },
  "type": "workspace_query"
}
"""
def __add_workspace(content:dict, database:Database):
    if not "data" in content.keys():
        raise Exception("No data given!")
    
    has_correct_data_fmt = len(set(["name", "filepaths", "description"]) & set(content["data"].keys())) >= 3

    if not has_correct_data_fmt:
        raise Exception("Malformed data format!")
    
    
    name = content["data"]["name"]
    if("id" in content["data"].keys()):
        ws_id = content["data"]["id"]
    else:
        ws_id = database.generate_ws_id(name)
    description = content["data"]["description"]
    filepaths = content["data"]["filepaths"]
    filepaths = [tuple(x) for x in filepaths]

    # Will throw an exception if something doesnt jive
    database.add_workspace(ws_id, filepaths, name, description)
    database.dump_workspaces()
    database.select_workspace(ws_id)
    

"""
Correct input format
{
    "action": "remove_workspace",
    "id": "some-id"
}
Example input from the FrontEnd
{"type":"workspace_query", "content":{"action":"remove_workspace", "id":"ws1"}}
"""
def __remove_workspace(content:dict, database:Database):
    if not "id" in content.keys():
        raise Exception("No id supplied!")
    
    ws_id = content["id"]
    # Will throw an exception if it doesn't jive
    database.remove_workspace(ws_id)


"""
Correct input format
{
    "action": "gen_id",
    "name": "some-name"
}
Example input from the FrontEnd
{"type": "workspace_query", "content": {"action": "gen_id", "name": "bigchungusforlife"}}
"""
def __gen_id(content:dict, database:Database):
    if not "name" in content.keys():
        raise Exception("No name provided!")

    name = content["name"]
    ws_id = database.generate_ws_id(name)
    return ws_id

"""
Correct input format
{
    "action": "select_workspace",
    "id": "some-id"
}
Example input from the FrontEnd
{"type": "workspace_query", "content": {"action": "select_workspace", "id": "ws1"}}
"""
def __select_workspace(content:dict, database:Database):
    if "id" not in content.keys():
        raise Exception("No id provided!")
    
    # Will throw an exception if something doesnt jive
    database.select_workspace(content["id"])

def process(content:dict, database:Database):
    res = None
    res_msg = ""
    if content["action"] == "list_workspaces":
        workspaces_info = __list_workspaces(content, database)
        res = workspaces_info
    elif content["action"] == "open_workspace":
        workspace = __open_workspace(content, database)
        res = workspace
    elif content["action"] == "add_workspace":
        __add_workspace(content, database)
    elif content["action"] == "remove_workspace":
        __remove_workspace(content, database)
    elif content["action"] == "gen_id":
        ws_id = __gen_id(content, database)
        res = [ws_id]
    elif content["action"] == "select_workspace":
        __select_workspace(content, database)
    else:
        raise Exception("Invalid Action!")
    
    return res, res_msg
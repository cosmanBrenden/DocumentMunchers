import file_system

"""
Correct input format
{
    "filepath":fp,
    "action":"open"
}
Example input from the FrontEnd
{"type":"os_query", "content":{"action":"open", "filepath": "/home/monke/Documents/COMP4721/Proj/Term-Project-Group-1/TestTexts/R9MZT9VU.txt"}}
"""
def __open_file(content:dict):
    if("filepath" not in content.keys()):
        raise Exception("No filepath supplied!")
    filepath = content["filepath"]
    file_system.open_with_default_viewer(filepath)

"""
Correct input format
{
    "action": "ask_directory"
}
Example input from the FrontEnd
{"type":"os_query", "content":{"action":"ask_directory"}}
"""
def __ask_directory():
    files = file_system.ask_user_for_directory()
    return files

def process(content:dict) -> dict:
    res = None
    res_msg = ""
    if(content["action"] == "open"):
        __open_file(content)
        res_msg = f"Opened '{content['filepath']}'"
    elif(content["action"] == "ask_directory"):
        files = __ask_directory()
        res = files
        res_msg = f"Asked for directory"
    else:
        raise Exception("Invalid Action!")

    return res, res_msg
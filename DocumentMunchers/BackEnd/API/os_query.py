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

def process(content:dict) -> dict:
    if(content["action"] == "open"):
        __open_file(content)
        return f"Opened {content['filepath']}"
    else:
        raise Exception("Invalid Action!")
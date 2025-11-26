from database import Database
from datetime import datetime, timezone, timedelta

"""
Correct input format
{
    "query":query_str,
    "action":"open"
}
Example input from the FrontEnd
{"type":"search_query", "content":{"action":"search", "query":"Show me some documents about the inuit"}}
"""

def __make_search(content:dict, db:Database):
    if("query" not in content.keys()):
        raise Exception("No search query passed!")
    query = content["query"]
    res = db.get_search_results(query)
    res = __format_results(res)
    return res

def process(content:dict, db:Database) -> dict:
    if(content["action"] == "search"):
        res = __make_search(content, db)
        return res, ""
    else:
        raise Exception("Invalid Action!")


'''
Format the results so the front end can make use of them 
'''
def __format_results(raw_results):
    formatted_results = []
    for i, item in enumerate(raw_results):
        formatted_results.append({
            "id": item[1]['id'],
            "title": item[0],
            "summary": item[1]["summary"] if item[1]["summary"] != None else "No summary available!",
            "relevance": int(float(item[2]) * 100), 
            "lastOpened": datetime.fromtimestamp(item[1]['date_modified'], tz=timezone(timedelta(hours=-4), 'AST')),
            "keywords": item[1]['keywords']
        })
        print(datetime.fromtimestamp(item[1]['date_modified'], tz=timezone(timedelta(hours=-4), 'AST')))

    return formatted_results
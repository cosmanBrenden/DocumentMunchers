import os
from pathlib import Path

'''
Use to reset all pre-processed data (for testing purposes)
'''
check = input("Are you sure you want to delete all pre-processed data? y/n  ")
if check.lower() == 'y':
    api_path = os.path.dirname(os.path.abspath(__file__))

    # Clear path in test_dir.txt
    #with open(api_path + '/workspace_files/test_dir.txt', "w", encoding="utf-8") as f:
        #f.writelines([])

    # Delete all files in TFIDFS
    tfidfs_path = api_path + '/workspace_files/TFIDFS/'
    files = os.listdir(tfidfs_path)
    print("TFIDFS: ", files)
    for file in files:
        try:
            print("Deleting: " + file)
            os.remove(tfidfs_path + file)

        except Exception as e:
            print("Error trying to delete {file}: ", e)
    
    try:
        # Delete main workspaces.json file
        workspaces = api_path + '/workspace_files/workspaces.json'
        print("Removing workspaces.json from: ", workspaces)
        os.remove(workspaces)
       
    except Exception as e:
        print("Error trying to delete workspaces.json: ", e)
    
import json
import requests
import sys
import getopt
import os
import dotenv
import codecs

# dotenv
dotenv.load_dotenv()

# Get Joplin API URL and token from environment variables
joplin_url = os.getenv("JOPLIN_URL", "http://localhost:41184")
api_token = os.getenv("JOPLIN_TOKEN", None)

# Function to fetch all notebooks and find target notebook ID
def get_notebook_id(notebook_name):
    try:
        params = {'token': api_token}

        response = requests.get(f"{joplin_url}/folders", params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        notebooks = response.json().get('items', [])  # Get notebooks from response

        # Find notebook with matching name
        for notebook in notebooks:
            if notebook['title'] == notebook_name:
                return notebook['id']

        return None  # Return None if no match found
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



# Function to create a note in a specific notebook
def create_note(note_title, note_body, notebook_id=None):
    try:
        payload = {
            "title": note_title,
            "body": note_body
        }

        params = {'token': api_token}

        # Add notebook_id to payload if provided
        if notebook_id:
            payload["parent_id"] = notebook_id

        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(f"{joplin_url}/notes", headers=headers, json=payload, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors

        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":

# get options from cli

    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:n:b:", ["title=", "notebook=", "body="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    note_title = None
    notebook_name = None
    note_body = None

    for opt, arg in opts:
        if opt in ("-t", "--title"):
            note_title = arg
        elif opt in ("-n", "--notebook"):
            notebook_name = arg
        elif opt in ("-b", "--body"):
            # fixup newlines and other escaped characters
            note_body = codecs.decode(arg, 'unicode_escape')

        else:
            assert False, "unhandled option"

    if note_title is None:
        print("Note title is required")
        sys.exit(2)

    if notebook_name is None:
        print("Notebook name is required")
        sys.exit(2)

    if note_body is None:
        print("Note body is required")
        sys.exit(2)

    notebook_id = get_notebook_id(notebook_name)
    if notebook_id is None:
        print(f"Notebook with name {notebook_name} not found")
        sys.exit(2)

    note = create_note(note_title, note_body, notebook_id)
    if note:
        print(f"Note created with ID: {note['id']}")
    else:
        print("Note creation failed")
        sys.exit(2)


#    # Get Notebook ID for a notebook named 'My Notebook'
#    print("Get notebook id")
#    notebook_id = get_notebook_id("My Notebook")
#    print(f"Notebook id {notebook_id}")

    
#    # Create a note
#    print("Create note")
#    note = create_note("My Note Title", "This is the note body", notebook_id)
#    if note:
#        print(f"Note created with ID: {note['id']}")


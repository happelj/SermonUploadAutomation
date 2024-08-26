import json
import requests
import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to handle the sermon upload process
def upload_sermon():
    # Collecting user input from GUI
    API_KEY = api_key_entry.get().strip()
    BROADCASTERID = broadcaster_id_entry.get().strip()
    TITLE = title_entry.get().strip()
    SHORTITLE = short_title_entry.get().strip()
    SUBTITLE = subtitle_entry.get().strip()
    SPEAKER = speaker_entry.get().strip()
    PREACH_DATE = preach_date_entry.get().strip()
    PUBLISH_DATE = publish_date_entry.get().strip()
    BIBLE = bible_entry.get().strip()
    MORE_INFO = more_info_entry.get().strip()
    EVENT_TYPE = event_type_entry.get().strip()
    LANG = language_entry.get().strip()
    KEYWORDS = keywords_entry.get().strip()
    MEDIA_PATH = media_file_entry.get().strip()

    # Checking if the file exists
    if not MEDIA_PATH:
        messagebox.showerror("Error", "Please select a media file.")
        return

    # Extracting directory and filename from MEDIA_PATH
    MEDIA_DIR = os.path.dirname(MEDIA_PATH)
    MEDIA_FILENAME = os.path.basename(MEDIA_PATH)

    # Ensure that MEDIA_FILENAME does not contain any invalid characters
    if '/' in MEDIA_FILENAME or '\0' in MEDIA_FILENAME:
        messagebox.showerror("Error", "Media filename contains invalid characters.")
        return

    HOST = "https://api.sermonaudio.com"
    ENDPOINT = f"{HOST}/v2/node/sermons"

    # Create a JSON payload with the sermon create parameters.
    json_payload = {
        "broadcasterID": BROADCASTERID,
        "fullTitle": TITLE,
        "displayTitle": SHORTITLE,
        "subtitle": SUBTITLE,
        "speakerName": SPEAKER,
        "preachDate": PREACH_DATE,
        "publishDate": PUBLISH_DATE,
        "bibleText": BIBLE,
        "moreInfoText": MORE_INFO,
        "eventType": EVENT_TYPE,
        "languageCode": LANG,
        "keywords": KEYWORDS,
        "acceptCopyright": "true"
    }

    # Send the payload to the sermons endpoint.
    response = requests.post(
        ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        },
        json=json_payload
    )

    # Print the response in a formatted way
    print(json.dumps(response.json(), indent=4))

    # Extract the sermonID from the response
    try:
        sermon_id = response.json()['sermonID']
        print(f"New sermonID is: {sermon_id}")
    except KeyError:
        messagebox.showerror("Error", "Could not retrieve sermonID from response")
        return

    # Now let's upload media to the new sermon.
    ENDPOINT = f"{HOST}/v2/media"

    # Create a JSON payload for the media upload.
    json_payload = {
        "sermonID": sermon_id,
        "uploadType": "original-video",  # change to "original-audio" if uploading audio
        "originalFilename": MEDIA_FILENAME
    }

    # First, post to the media endpoint to create a media upload for the sermon.
    response = requests.post(
        ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        },
        json=json_payload
    )

    # Print the response in a formatted way
    print(json.dumps(response.json(), indent=4))

    # Extract the upload URL from the response
    try:
        upload_url = response.json()['uploadURL']
        print(f"Media upload URL is: {upload_url}")
    except KeyError:
        messagebox.showerror("Error", "Could not retrieve upload URL from response")
        return

    # Now upload the media.
    try:
        with open(MEDIA_PATH, 'rb') as media_file:
            response = requests.post(
                upload_url,
                headers={
                    "X-API-Key": API_KEY
                },
                data=media_file
            )
        print(response.status_code)
        print(response.text)
        messagebox.showinfo("Success", "Sermon uploaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to open file dialog and select media file
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Media files", "*.mp4;*.mp3;*.mov;*.avi")])
    media_file_entry.delete(0, tk.END)
    media_file_entry.insert(0, filename)

# Creating the GUI
root = tk.Tk()
root.title("SermonAudio Uploader")

# API Key
tk.Label(root, text="API Key:").grid(row=0, column=0, sticky=tk.E)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.grid(row=0, column=1, padx=5, pady=5)
api_key_entry.insert(0, '<api_key>') # Change <api_key> to the default api key

# Broadcaster ID
tk.Label(root, text="Broadcaster ID:").grid(row=1, column=0, sticky=tk.E)
broadcaster_id_entry = tk.Entry(root, width=50)
broadcaster_id_entry.grid(row=1, column=1, padx=5, pady=5)
broadcaster_id_entry.insert(0, '<boardcaster_id') # Change <broadcaster_id> to the default broadcaster id

# Sermon Title
tk.Label(root, text="Sermon Title:").grid(row=2, column=0, sticky=tk.E)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=2, column=1, padx=5, pady=5)

# Short Title
tk.Label(root, text="Short Title (Optional):").grid(row=3, column=0, sticky=tk.E)
short_title_entry = tk.Entry(root, width=50)
short_title_entry.grid(row=3, column=1, padx=5, pady=5)

# Subtitle
tk.Label(root, text="Subtitle:").grid(row=4, column=0, sticky=tk.E)
subtitle_entry = tk.Entry(root, width=50)
subtitle_entry.grid(row=4, column=1, padx=5, pady=5)

# Speaker Name
tk.Label(root, text="Speaker Name:").grid(row=5, column=0, sticky=tk.E)
speaker_entry = tk.Entry(root, width=50)
speaker_entry.grid(row=5, column=1, padx=5, pady=5)
speaker_entry.insert(0, '<speaker_name>') # Change <speaker_name> to the default speaker name

# Preach Date
tk.Label(root, text="Preach Date (YYYY-MM-DD):").grid(row=6, column=0, sticky=tk.E)
preach_date_entry = tk.Entry(root, width=50)
preach_date_entry.grid(row=6, column=1, padx=5, pady=5)

# Get today's date in YYYY-MM-DD format and insert it as the default value
today_date = datetime.today().strftime('%Y-%m-%d')
preach_date_entry.insert(0, today_date) # Default is today's date

# Publish Date
tk.Label(root, text="Publish Date (YYYY-MM-DD):").grid(row=7, column=0, sticky=tk.E)
publish_date_entry = tk.Entry(root, width=50)
publish_date_entry.grid(row=7, column=1, padx=5, pady=5)
publish_date_entry.insert(0, today_date) # Default is today's date

# Bible Text
tk.Label(root, text="Bible Text (e.g., John 3:16):").grid(row=8, column=0, sticky=tk.E)
bible_entry = tk.Entry(root, width=50)
bible_entry.grid(row=8, column=1, padx=5, pady=5)

# More Info Text
tk.Label(root, text="More Info Text:").grid(row=9, column=0, sticky=tk.E)
more_info_entry = tk.Entry(root, width=50)
more_info_entry.grid(row=9, column=1, padx=5, pady=5)

# Event Type
tk.Label(root, text="Event Type:").grid(row=10, column=0, sticky=tk.E)
event_type_entry = tk.Entry(root, width=50)
event_type_entry.grid(row=10, column=1, padx=5, pady=5)
event_type_entry.insert(0, '<event_type>') # Change <event_type> to the default event type
# Language Code
tk.Label(root, text="Language Code:").grid(row=11, column=0, sticky=tk.E)
language_entry = tk.Entry(root, width=50)
language_entry.grid(row=11, column=1, padx=5, pady=5)

# Keywords
tk.Label(root, text="Keywords (comma-separated):").grid(row=12, column=0, sticky=tk.E)
keywords_entry = tk.Entry(root, width=50)
keywords_entry.grid(row=12, column=1, padx=5, pady=5)

# Media File
tk.Label(root, text="Media File:").grid(row=13, column=0, sticky=tk.E)
media_file_entry = tk.Entry(root, width=40)
media_file_entry.grid(row=13, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=13, column=2, padx=5, pady=5)

# Upload Button
upload_button = tk.Button(root, text="Upload Sermon", command=upload_sermon)
upload_button.grid(row=14, columnspan=3, pady=10)

# Start the GUI
root.mainloop()

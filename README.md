# SermonAudio Uploader

This is a Python application for uploading sermons to SermonAudio. It provides a graphical user interface (GUI) for entering sermon details and selecting a media file for upload.

## Features

- **User-Friendly GUI:** Built with `tkinter` for easy use.
- **Secure Uploads:** Supports secure sermon uploads to SermonAudio via their API.
- **Flexible Input:** Allows for various sermon details, including title, subtitle, speaker name, dates, and more.

## Requirements

- Python 3.x
- `requests` library
- `tkinter` library (usually included with Python)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/sermonaudio-uploader.git
    cd sermonaudio-uploader
    ```

2. Install the required packages:
    ```bash
    pip install requests
    ```

## Usage

1. Run the script:
    ```bash
    python sermonaudio_uploader.py
    ```

2. Enter the required information in the GUI:
   - API Key
   - Broadcaster ID
   - Sermon details (title, speaker, dates, etc.)
   - Media file for upload

3. Click the "Upload Sermon" button to upload the sermon to SermonAudio.

## Notes

- Replace the placeholder text in the GUI with your actual API key and other information before uploading.
- Make sure the media file is correctly formatted and supported by SermonAudio.

## Disclaimer

This tool is provided "as is" without any warranties. Use at your own risk.


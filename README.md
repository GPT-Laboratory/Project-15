# Downloading Youtube video

## Requirements

Python 3.10+

## Install

1. Create a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

    ```bash
    sudo ./install_yt_dlp_ffmpeg.sh
    ```

3. Create and add [caption.ai api key](https://help.captions.ai/api-reference/api) to .env file "CAPTIONS_API_KEY=[your key]"

## Usage

```
python youtube.py
```

Follow the instructions. Mind, that for my demo of 6 second video it took ~10 mins to create the AI Avatar.

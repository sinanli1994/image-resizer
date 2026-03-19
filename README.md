# Image Resizer

A desktop image resizing/compression app built with PyQt6 and Pillow.

## Features
- Select an input image from disk
- Choose output file location and format
- Set max width and height
- Keep aspect ratio while resizing
- Set max quality for JPEG and WEBP output
- Optionally target a specific output file size in MB
- Automatic quality adjustment until the image is below the target size
- Grouped desktop layout for files, resize settings, compression, and status

## Supported Output Formats
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- WEBP (`.webp`)

Notes:
- Target-size compression is available for JPEG and WEBP output.
- PNG output is supported, but it does not use quality-based target-size compression.

## Project Structure
- `src/main.py`
- `src/core/compressor.py`
- `src/ui/main_window.py`
- `docs/PRD.md`
- `requirements.txt`

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python src/main.py
```

Or:

```bash
python -m src.main
```

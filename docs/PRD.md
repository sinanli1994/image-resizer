# Product Requirements Document (PRD)

## Product Name
Image Resizer

## Overview
Image Resizer is a lightweight desktop application for resizing and compressing images locally on the user's machine. The app supports direct file selection, grouped resize/compression controls, and size-aware export for quality-adjustable formats.

## Goals
- Provide a simple desktop UI for single-image resize/compression.
- Preserve image quality with configurable compression.
- Allow users to export images under a target file size when the format supports quality adjustment.
- Keep processing local with no cloud upload.

## Target Users
- Designers and content creators preparing assets.
- Developers optimizing image sizes for web/apps.
- General users needing quick image resizing.

## Core Features
- Input image selection via file picker.
- Output path selection via file picker.
- Width and height controls.
- Optional keep-aspect-ratio toggle.
- Compression quality control.
- Optional target file size control in MB.
- Automatic quality search for JPEG and WEBP output to stay below the target size.
- Grouped UI sections for files, resize settings, compression, and status.
- Success/error feedback in UI.

## Non-Goals
- Batch processing (future enhancement).
- Advanced editing (crop, filters).
- Cloud storage integrations.
- Guaranteed target-size compression for formats without a practical quality setting, such as PNG.

## Technical Requirements
- Python 3.10+
- PyQt6 for desktop interface.
- Pillow for image processing.
- Package-compatible entrypoint that supports both `python src/main.py` and `python -m src.main`.

## Acceptance Criteria
- App launches successfully from `python src/main.py` and `python -m src.main`.
- User can select an image and output path.
- User can resize image with chosen dimensions.
- User can optionally set a target file size for JPEG or WEBP output.
- Output file is created successfully.
- When target size is enabled for JPEG or WEBP, the app reduces quality automatically until the file size is below the requested limit or returns a clear error if the target cannot be reached.
- Errors are shown when input is invalid.

# Product Requirements Document (PRD)

## Product Name
Image Resizer

## Overview
Image Resizer is a lightweight desktop application for preparing images locally on the user's machine. The app is designed around a size-first workflow: by default it tries to keep the original resolution and adjusts compression quality to get under a target file size, while dimension limits remain optional fallback controls.

## Goals
- Provide a simple desktop UI for single-image resize/compression.
- Make file size the primary constraint by default.
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
- Size target enabled by default with MB input.
- Automatic quality search for JPEG and WEBP output to stay below the target size while getting as close as possible to the limit.
- Optional width and height controls used only when the user enables dimension limiting.
- Optional keep-aspect-ratio toggle for dimension-limited exports.
- Compression quality control.
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
- Entrypoint supports `python src/main.py`.

## Acceptance Criteria
- App launches successfully from `python src/main.py`.
- User can select an image and output path.
- User can optionally set a target file size for JPEG or WEBP output.
- Target file size is enabled by default and starts at `5.0 MB`.
- By default, the app preserves the original image resolution unless the user enables dimension limits.
- Output file is created successfully.
- When target size is enabled for JPEG or WEBP, the app reduces quality automatically until the file size is below the requested limit and should prefer the largest result under that limit.
- If quality-only compression cannot reach the target, the app returns a clear error telling the user to enable dimension limits, choose a different format, or use a larger target.
- Errors are shown when input is invalid.

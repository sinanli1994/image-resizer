# Image Resizer

A simple desktop tool to resize and compress images to meet size and dimension limits for uploads.

---

## ✨ Why this tool

Many websites require images to meet strict file size or dimension limits.

However:
- Photos from phones are often too large
- Online tools are inconvenient or unreliable
- Existing software is overly complex

This tool provides a **simple and fast way** to prepare images for upload.

---

## 🚀 Features

- Resize images by width and height
- Compress images using adjustable quality
- Target specific file sizes (e.g., under 5MB)
- Maintain aspect ratio
- Simple desktop interface

---

## 🖼️ Use Cases

- Uploading documents to government websites
- Insurance claim submissions
- Job application portals
- Social media uploads

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python src/main.py
```

---

## 🧩 Supported Formats

- Input: PNG, JPG, JPEG, WEBP, BMP, TIFF
- Output: JPG, JPEG, PNG, WEBP
- Target file size mode is available for JPEG and WEBP output
- PNG output is supported, but it does not use quality-based target-size compression

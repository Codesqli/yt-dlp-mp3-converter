# 🎶 yt-dlp MP3 Converter

A simple Python-based application that allows you to **download your own content** from YouTube (and other supported platforms) in MP3 format.  

⚠️ **Note:** This project is for **educational purposes only**. Do not use it to download or share copyrighted content.  

---

## 📥 Installation

### 1️⃣ Clone the repository
Type the following commands in your terminal or PowerShell:

`git clone https://github.com/Anonyuser-x/yt-dlp-mp3-converter.git`  
`cd yt-dlp-mp3-converter`

### 2️⃣ Install Python dependencies

`pip install -r requirements.txt`

### 3️⃣ Install FFmpeg

FFmpeg is required for audio conversion.

**Windows:**  
`winget install ffmpeg`  

Default installation path (example):  
`C:\Users\<USERNAME>\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg...\bin`

Add it to your PATH environment variable:  
- Press `Win + R`, type `sysdm.cpl` → Advanced → Environment Variables  
- Select "Path" → Edit → New → Add the `...bin` folder  
- Close and reopen CMD or PowerShell  

Test installation:  
`ffmpeg -version`

**Linux (Debian/Ubuntu):**  
`sudo apt update`  
`sudo apt install ffmpeg`

**macOS (Homebrew):**  
`brew install ffmpeg`

---

## ▶️ Usage

Provide one or multiple YouTube links. Links can be comma-separated:

`python main.py "https://www.youtube.com/watch?v=xxxx, https://www.youtube.com/watch?v=yyyy"`

MP3 files will be saved in the `Muzikler/` folder.

---

## 📌 Example

`python main.py "https://www.youtube.com/watch?v=z3wAjJXbYzA"`

Expected output:

`Downloading: Norm Ender - Mekanın Sahibi`  
`Converting: MP3`  
`Saved: Muzikler/Norm Ender - Mekanın Sahibi.mp3`

---

## 🛠 Requirements

- Python 3.8+  
- yt-dlp  
- ffmpeg

---

## ⚖️ License

This project is for **educational purposes**.  
You are free to use it to download and convert **your own videos**.  
Use of copyrighted content is **the user's responsibility**.

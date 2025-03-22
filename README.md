# 📥 Video Downloader Web App

This project is a web-based tool for downloading videos and audio from YouTube, TikTok, and Instagram using [yt-dlp](https://github.com/yt-dlp/yt-dlp). It is implemented with **Flask** and offers a simple user interface.

---

## 🚀 Features
- Download videos in **MP4** or audio in **MP3**
- Paste URL from **YouTube, TikTok, Instagram**
- Displays a progress bar and file status
- Supports cookies-based authentication (for downloading private or region-restricted videos)
- **Dark/Light theme toggle**

---

## 🔒 Why is the homepage blocked?
The root route (`/`) of the deployed site returns a 403 Forbidden message with the following notice:

> **Access Denied**  
> *This site is blocked and intended for educational purposes only.*

This was done intentionally to prevent public access to the tool and to ensure it is only used in **controlled, educational environments**.

---

## 📁 File Download Location
Originally, downloaded files were served from the `static/` directory. This was **insecure**, because anyone could access them via direct URL.

### 🔐 Important Change:
- ✅ Files are now saved in a secure custom `downloads/` folder
- ✅ They are **not** accessible via direct URL anymore
- ✅ Downloads are only provided through a Flask route (`/download/<filename>`) using `send_from_directory()`

This improves privacy and prevents unauthorized file access.

---

## 📂 Folder Structure
```
project/
├── app.py                  # Main Flask app
├── templates/
│   └── index.html          # Frontend HTML
├── static/
│   ├── styles.css          # UI styling
│   └── script.js           # Download logic and interactivity
├── downloads/              # (New) secure location for downloaded files
├── .env                    # Environment configs (not in Git)
├── .gitignore              # Ignores cookies and downloads from repo
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 📦 Dependencies
Install using pip:
```bash
pip install -r requirements.txt
```

---

## 💾 Cookie Support
To access private content, cookies can be saved from your browser (using tools like **EditThisCookie**) and stored as:
- `youtube_cookies.txt`
- `tiktok_cookies.txt`
- `instagram_cookies.txt`

> These files are **excluded from Git** and should be stored locally only.

---

## ☁️ Deployment to Render
To deploy on [Render](https://render.com):

1. Create a new Web Service from your GitHub repo
2. Use the following build & start commands:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
flask run --host=0.0.0.0 --port=5000
```

3. Add environment variable:
```env
FLASK_ENV=production
```

4. If needed, add:
```env
SAVE_PATH=/tmp/Downloads
```

> ⚠️ Flask’s development server is not intended for production. Consider using `gunicorn` for more robust deployments.

---

## 📜 License
This project is intended **strictly for educational purposes.**
All use must comply with the terms of service of the video platforms.

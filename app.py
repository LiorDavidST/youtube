from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import yt_dlp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get save path from environment variable or use default
DEFAULT_SAVE_PATH = os.getenv("SAVE_PATH", "/tmp/Downloads")  # Use a temporary directory for production
os.makedirs(DEFAULT_SAVE_PATH, exist_ok=True)

# Get cookies file path from environment variable or use default
COOKIES_PATH = os.getenv("YT_COOKIES_FILE", r"C:\Users\stlio\Download\cookies.txt")  # Default path for cookies

def download_youtube_video(url, save_path, format_choice):
    """
    Downloads a video from a supported platform using yt-dlp with dynamic cookie support.
    """
    try:
        # Determine appropriate cookie file based on URL
        if "instagram.com" in url:
            cookies = "instagram_cookies.txt"
        elif "tiktok.com" in url:
            cookies = "tiktok_cookies.txt"
        else:
            cookies = "youtube_cookies.txt"

        os.makedirs(save_path, exist_ok=True)

        # Set the appropriate format
        if format_choice == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'cookiefile': cookies,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'cookiefile': cookies,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return {"success": True, "message": f"Downloaded successfully: {url}"}

    except yt_dlp.utils.DownloadError as e:
        return {"success": False, "message": f"❌ Download Error: {e}"}
    except Exception as e:
        return {"success": False, "message": f"❌ Unexpected error: {e}"}


# Block homepage access with message
from flask import abort, make_response

@app.route("/", methods=["GET", "POST"])
def index():
    return make_response("<h1>Access Denied</h1><p>This site is blocked and intended for educational purposes only.</p>", 403)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        format_choice = request.form.get("format", "mp4").strip()
        save_path = request.form.get("save_path", "").strip()
        if not save_path:
            save_path = DEFAULT_SAVE_PATH

        if not url:
            return jsonify({"success": False, "message": "❌ Please enter a valid YouTube URL!"})

        result = download_youtube_video(url, save_path, format_choice)
        return jsonify(result)

    return render_template("index.html")

@app.route("/download/<filename>")
def serve_download(filename):
    return send_from_directory(DEFAULT_SAVE_PATH, filename, as_attachment=True)

if __name__ == "__main__":
    # Set debug to False in production
    app.run(debug=os.getenv("FLASK_DEBUG", "False") == "True")

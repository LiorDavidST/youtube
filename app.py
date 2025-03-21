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

def download_youtube_video(url, save_path, format_choice):
    try:
        os.makedirs(save_path, exist_ok=True)
        if format_choice == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Fix extension if post-processing changed it
            if format_choice == "mp3":
                filename = os.path.splitext(filename)[0] + ".mp3"
            elif filename.endswith(".webm"):
                filename = os.path.splitext(filename)[0] + ".mp4"

        file_only = os.path.basename(filename)
        return {
            "success": True,
            "message": f"✅ Downloaded successfully: {file_only}",
            "filename": file_only
        }

    except yt_dlp.utils.DownloadError as e:
        return {"success": False, "message": f"❌ Download Error: {e}"}
    except Exception as e:
        return {"success": False, "message": f"❌ An unexpected error occurred: {e}"}

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

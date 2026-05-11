from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "static/downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    data = request.get_json()

    url = data.get("url")
    download_type = data.get("type")

    if not url:
        return jsonify({
            "status": "error",
            "message": "No URL provided"
        })

    unique_id = str(uuid.uuid4())

    try:

        if download_type == "video":

            output_path = os.path.join(
                DOWNLOAD_FOLDER,
                f"{unique_id}.mp4"
            )

            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": output_path,
                "merge_output_format": "mp4",
                "quiet": True,
                "noplaylist": True
            }

        else:

            output_path = os.path.join(
                DOWNLOAD_FOLDER,
                f"{unique_id}.mp3"
            )

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_path,
                "quiet": True,
                "noplaylist": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320"
                }]
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({
            "status": "success",
            "file": output_path
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


@app.route("/file")
def get_file():

    path = request.args.get("path")

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

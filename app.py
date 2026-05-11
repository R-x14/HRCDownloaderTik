from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    data = request.get_json()

    url = data.get("url")
    mode = data.get("mode")

    if not url:
        return jsonify({
            "status": "error",
            "message": "Please enter TikTok URL"
        })

    unique_id = str(uuid.uuid4())

    try:

        # AUDIO

        if mode == "audio":

            output_template = os.path.join(
                DOWNLOAD_FOLDER,
                f"{unique_id}.%(ext)s"
            )

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_template,
                "quiet": True,
                "noplaylist": True,

                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320"
                }]
            }

        # VIDEO

        else:

            output_template = os.path.join(
                DOWNLOAD_FOLDER,
                f"{unique_id}.%(ext)s"
            )

            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": output_template,
                "merge_output_format": "mp4",
                "quiet": True,
                "noplaylist": True
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            downloaded_file = ydl.prepare_filename(info)

            if mode == "audio":
                downloaded_file = downloaded_file.rsplit(".", 1)[0] + ".mp3"

        return jsonify({
            "status": "success",
            "file": downloaded_file
        })

    except Exception as e:

        error_message = str(e)

        # PRIVATE VIDEO

        if "You do not have permission to view this post" in error_message:

            return jsonify({
                "status": "error",
                "message": "المقطع خاص أو غير متاح للمشاهدة"
            })

        return jsonify({
            "status": "error",
            "message": "حدث خطأ أثناء التحميل"
        })


@app.route("/file")
def file():

    path = request.args.get("path")

    if not os.path.exists(path):
        return "File not found"

    return send_file(path, as_attachment=True)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

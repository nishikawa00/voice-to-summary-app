from flask import Flask, request, jsonify, send_from_directory
import os
import smtplib
from email.mime.text import MIMEText
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="../public")

# 📦 静的ファイルのルート（PWA対応）
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# 🎙 音声アップロード → Whisper → GPT → Gmail送信
openai.api_key = os.getenv("OPENAI_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

@app.route("/upload", methods=["POST"])
def upload_audio():
    file = request.files["file"]
    audio_path = "temp.webm"
    file.save(audio_path)

    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    text = transcript["text"]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "以下のテキストを会議の議事録として要約してください。"},
            {"role": "user", "content": text},
        ],
    )
    summary = response["choices"][0]["message"]["content"]

    msg = MIMEText(summary)
    msg["Subject"] = "議事録の要約"
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)

    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
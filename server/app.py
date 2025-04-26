from flask import Flask, request, jsonify
import openai
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

@app.route('/upload', methods=['POST'])
def upload_audio():
    file = request.files['file']
    audio_path = 'temp.webm'
    file.save(audio_path)

    # Whisper 文字起こし
    with open(audio_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    text = transcript['text']

    # 要約
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "以下のテキストを会議の議事録として要約してください。"},
            {"role": "user", "content": text}
        ]
    )
    summary = response['choices'][0]['message']['content']

    # Gmail送信
    msg = MIMEText(summary)
    msg['Subject'] = '議事録の要約'
    msg['From'] = GMAIL_USER
    msg['To'] = TO_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)

    return jsonify({'summary': summary})

from flask import Flask, request, jsonify
import openai
import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
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

    # メール送信
    message = Mail(
        from_email='from@example.com',
        to_emails=TO_EMAIL,
        subject='議事録の要約',
        plain_text_content=summary
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(e)

    return jsonify({'summary': summary})

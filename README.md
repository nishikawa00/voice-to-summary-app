# 音声議事録アプリ（PWA対応、Gmail送信）

## セットアップ手順（Flask）

### 1. 環境準備
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
pip install -r requirements.txt
```

### 2. .envファイルを作成
`.env.example` を `.env` にリネームしてAPIキーを設定。

必要な項目：
- OPENAI_API_KEY
- GMAIL_USER
- GMAIL_PASS
- TO_EMAIL

### 3. サーバー起動
```bash
python server/app.py
```

### 4. Webアプリにアクセス
ブラウザで `http://localhost:5000/public/index.html` にアクセス。

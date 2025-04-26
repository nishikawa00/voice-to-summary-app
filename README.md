# 音声議事録アプリ（PWA対応）

## セットアップ手順（Flask）

### 1. 環境準備
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
pip install -r requirements.txt
```

### 2. .envファイルを作成
`.env.example` を `.env` にリネームしてAPIキーを設定。

### 3. サーバー起動
```bash
python server/app.py
```

### 4. Webアプリにアクセス
ブラウザで `http://localhost:5000/public/index.html` にアクセス。

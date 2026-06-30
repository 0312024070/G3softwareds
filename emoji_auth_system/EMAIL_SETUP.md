# メール送信設定

このシステムでは、ログイン後に生成された3つの絵文字認証コードを、ユーザーに登録されているメールアドレスへ送信できます。

## 1. SMTP設定を行う

PowerShellで、`emoji_auth_system` フォルダに移動してから、以下を設定します。

```powershell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="送信元メールアドレス"
$env:SMTP_PASSWORD="アプリパスワード"
$env:SMTP_FROM="送信元メールアドレス"
```

Gmailを使う場合、通常のログインパスワードではなく、アプリパスワードを使います。

## 2. 起動する

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe init_db.py
.\.venv\Scripts\python.exe app.py
```

ブラウザで以下を開きます。

```text
http://127.0.0.1:5000
```

## 3. 動作確認

新規登録画面で、自分が受信できるメールアドレスを登録します。
そのユーザーでログインすると、絵文字認証画面に進むタイミングで、登録メールアドレスへ認証コードが送信されます。

SMTP設定がされていない場合や送信に失敗した場合は、授業用確認のためターミナルに認証コードを表示します。

## 注意

- メールパスワードやアプリパスワードは、絶対にソースコードやGitHubに書かないでください。
- `.env` などに保存する場合は、必ず `.gitignore` に追加してください。
- 送信元メールアドレスと `SMTP_USER` は同じものにするのが分かりやすいです。

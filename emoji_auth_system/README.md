# 絵文字シャッフル認証システム

株式会社村田サービス向けの「ID・パスワード認証 + 絵文字シャッフル認証」による二要素認証システムのサンプル実装です。  
VS Code で開発・実行しやすいように、Flask + SQLite 構成で作成しています。

## 1. 実装した機能

- ユーザーID・パスワードによるログイン
- 5分間有効な絵文字認証コードの生成
- 絵文字ボタンのランダムシャッフル表示
- 登録メールアドレスへの絵文字認証コード送信
- 新規登録時のメール確認コード送信
- メール確認コードが一致した場合のみアカウント作成
- パスワード再設定
- ログイン成功・失敗・タイムアウトの履歴保存
- 管理者用のユーザー一覧画面
- 管理者用の認証ログ履歴画面

## 2. 新規登録の流れ

この版では、新規登録フォームを送信しただけではアカウントは作成されません。

```text
新規登録画面で情報入力
↓
登録メールアドレスへ6桁の確認コード送信
↓
確認コード入力画面でコード入力
↓
コード一致・有効期限内ならアカウント作成
```

SMTP設定がない場合やメール送信に失敗した場合は、授業用確認のためターミナルにも確認コードを表示します。

## 3. VS Code での実行手順

### 手順1: フォルダを開く

VS Code で `emoji_auth_system` フォルダを開きます。

### 手順2: 仮想環境を作成する

```powershell
python -m venv .venv
```

### 手順3: 必要なライブラリを入れる

PowerShellの実行権限エラーを避けるため、仮想環境を有効化せずに実行できます。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 手順4: データベースを初期化する

```powershell
.\.venv\Scripts\python.exe init_db.py
```

### 手順5: Flask を起動する

```powershell
.\.venv\Scripts\python.exe app.py
```

ブラウザで次を開きます。

```text
http://127.0.0.1:5000
```

## 4. メール送信設定

毎回ターミナルにSMTP設定を入力したくない場合は、`.env.example` をコピーして `.env` を作成してください。

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=送信用Gmailアドレス
SMTP_PASSWORD=Googleで作成した16桁のアプリパスワード
SMTP_FROM=送信用Gmailアドレス
```

`.env` はGitHubへアップロードしないでください。

## 5. 動作確認用アカウント

| 種別 | ユーザーID | パスワード |
|---|---|---|
| 利用者 | murata_taro | password123 |
| 管理者 | admin | admin123 |
| 利用者 | tanaka_ken | password123 |

## 6. フォルダ構成

```text
emoji_auth_system/
├─ app.py
├─ config.py
├─ database.py
├─ init_db.py
├─ models.py
├─ requirements.txt
├─ .env.example
├─ .gitignore
├─ routes/
│  ├─ admin_routes.py
│  └─ auth_routes.py
├─ services/
│  ├─ auth_service.py
│  ├─ emoji_service.py
│  ├─ log_service.py
│  └─ notification_service.py
├─ static/
│  ├─ css/style.css
│  └─ js/emoji_auth.js
└─ templates/
   ├─ admin_logs.html
   ├─ admin_users.html
   ├─ base.html
   ├─ emoji_auth.html
   ├─ forgot_password.html
   ├─ login.html
   ├─ menu.html
   ├─ register.html
   └─ verify_registration.html
```

## 7. 注意

このソースコードは授業課題・プロトタイプ用です。実運用する場合は、HTTPS、CSRF対策、試行回数制限、監査ログ強化などを追加してください。

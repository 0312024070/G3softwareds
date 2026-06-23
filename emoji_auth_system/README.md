# 絵文字シャッフル認証システム

株式会社村田サービス向けの「ID・パスワード認証 + 絵文字シャッフル認証」による二要素認証システムのサンプル実装です。  
VS Code で開発・実行しやすいように、Flask + SQLite 構成で作成しています。

## 1. 実装した機能

- ユーザーID・パスワードによるログイン
- 5分間有効な絵文字認証コードの生成
- 絵文字ボタンのランダムシャッフル表示
- 通知された順番どおりに絵文字を選択する二要素認証
- ログイン成功・失敗・タイムアウトの履歴保存
- 管理者用のユーザー一覧画面
- 管理者用の認証ログ履歴画面

## 2. VS Code での実行手順

### 手順1: フォルダを開く

VS Code で `emoji_auth_system` フォルダを開きます。

### 手順2: 仮想環境を作成する

```bash
python -m venv .venv
```

### 手順3: 仮想環境を有効化する

PowerShell の場合:

```bash
.venv\Scripts\Activate.ps1
```

コマンドプロンプトの場合:

```bash
.venv\Scripts\activate.bat
```

### 手順4: 必要なライブラリを入れる

```bash
pip install -r requirements.txt
```

### 手順5: データベースを初期化する

```bash
python init_db.py
```

### 手順6: Flask を起動する

```bash
python app.py
```

ブラウザで次を開きます。

```text
http://127.0.0.1:5000
```

## 3. 動作確認用アカウント

| 種別 | ユーザーID | パスワード |
|---|---|---|
| 利用者 | murata_taro | password123 |
| 管理者 | admin | admin123 |
| 利用者 | tanaka_ken | password123 |

## 4. フォルダ構成

```text
emoji_auth_system/
├─ app.py
├─ config.py
├─ database.py
├─ init_db.py
├─ models.py
├─ requirements.txt
├─ pyproject.toml
├─ .editorconfig
├─ .vscode/
│  ├─ launch.json
│  └─ settings.json
├─ routes/
│  ├─ __init__.py
│  ├─ admin_routes.py
│  └─ auth_routes.py
├─ services/
│  ├─ __init__.py
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
   ├─ login.html
   └─ menu.html
```

## 5. プログラミング規約

- Python は PEP8 を基本とする。
- クラス名は `PascalCase` とする。
- 関数名・変数名は `snake_case` とする。
- 定数は `UPPER_SNAKE_CASE` とする。
- 画面処理、認証処理、DB処理を分離する。
- SQL 文はパラメータバインドを使用し、文字列連結で値を埋め込まない。
- パスワードは平文保存せず、ハッシュ化して保存する。
- 認証コードには有効期限と使用済みフラグを持たせる。

## 6. 注意

このソースコードは授業課題・プロトタイプ用です。実運用する場合は、HTTPS、メール送信設定、CSRF対策、試行回数制限、監査ログ強化などを追加してください。

# プログラミング規約

## 1. 命名規則

| 対象 | 規則 | 例 |
|---|---|---|
| クラス名 | PascalCase | AuthService |
| 関数名 | snake_case | verify_password |
| 変数名 | snake_case | user_id |
| 定数名 | UPPER_SNAKE_CASE | CODE_EXPIRATION_MINUTES |
| HTMLファイル名 | snake_case | emoji_auth.html |

## 2. ファイル分割

- `routes/`: URLごとの画面制御を担当する。
- `services/`: 認証、絵文字コード、通知、ログなどの業務処理を担当する。
- `templates/`: HTMLテンプレートを保存する。
- `static/`: CSS、JavaScriptを保存する。
- `database.py`: SQLite接続とDB共通処理を担当する。

## 3. セキュリティ規約

- パスワードは必ずハッシュ化する。
- SQLは必ずプレースホルダを用いて実行する。
- 認証コードは5分で期限切れにする。
- 一度使った認証コードは再利用できないようにする。
- ログイン失敗・成功・タイムアウトを履歴として残す。

## 4. コーディング規約

- 1つの関数に複数の責任を持たせない。
- 画面処理と認証ロジックを混在させない。
- 重要な関数にはdocstringを書く。
- 例外発生時は利用者向けメッセージを表示する。
- コメントは「なぜそうするか」が分かる内容にする。

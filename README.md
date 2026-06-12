# G3softwareds
# Git / GitHub チーム開発ルール

> **重要**
>
> * `main` ブランチへ直接 `push` しない
> * 必ず自分の作業ブランチで開発する
> * 作業前には最新の `main` を取り込む
> * 分からない場合は勝手に `merge` せず相談する

---

# 初回のみ：自分の作業ブランチを作成する

## 1. mainブランチへ移動

```bash
git checkout main
```

## 2. 最新のmainを取得

```bash
git pull origin main
```

## 3. 自分の作業ブランチを作成

```bash
git checkout -b 自分のブランチ名
```

例：

```bash
git checkout -b feature/ui
git checkout -b feature/backend
```

## 4. ブランチが作成されたことを確認

```bash
git branch
```

例：

```text
  main
* feature/ui
```

`*` が付いているものが現在作業中のブランチです。

## 5. GitHubへブランチを登録（初回のみ）

```bash
git push -u origin 自分のブランチ名
```

例：

```bash
git push -u origin feature/ui
```

### `-u` とは？

`-u` は、

* GitHub上のブランチ (`origin/feature/ui`)
* ローカルのブランチ (`feature/ui`)

を関連付ける設定です。

この設定を行うことで、次回以降は送信先を指定する必要がなくなります。

---

# 毎日の作業フロー

## 1. 作業開始前

### ① mainブランチへ移動

```bash
git checkout main
```

### ② チームの最新状態を取得

```bash
git pull origin main
```

### ③ 自分の作業ブランチへ移動

例：

```bash
git checkout feature/ui
```

### ④ 最新のmainを自分のブランチへ取り込む

```bash
git merge main
```

### なぜ必要？

* 他のメンバーの変更を取り込むため
* 大きな競合（コンフリクト）を防ぐため
* 最新状態で動作確認するため

---

## 2. 開発作業

通常通りコードを編集する。

### 作業後の確認項目

* アプリが起動するか
* エラーが発生していないか
* 自分が追加・修正した機能が正しく動作するか
* 他の機能に影響を与えていないか

---

## 3. 変更をGitへ記録

### 変更状況確認

```bash
git status
```

### ファイルをステージング

すべて追加する場合：

```bash
git add .
```

特定ファイルのみ追加する場合：

```bash
git add ファイル名
```

例：

```bash
git add src/components/Timetable.tsx
```

### コミット

```bash
git commit -m "変更内容"
```

コミットメッセージ例：

```bash
git commit -m "時間割表示機能を追加"
git commit -m "単位計算処理のバグを修正"
git commit -m "講義検索機能を実装"
```

---

## 4. GitHubへ送信

### 2回目以降

```bash
git push
```

### なぜ `git push` だけでいいの？

初回セットアップ時に、

```bash
git push -u origin 自分のブランチ名
```

を実行しているためです。

`-u` によって、自分のブランチとGitHub上のブランチが関連付けられています。

そのため、2回目以降は

```bash
git push
```

だけで、自動的に自分の作業ブランチへ送信されます。

### 注意

`main` ブランチへ直接 `push` は行いません。

変更内容は自分の作業ブランチへ `push` し、その後 Pull Request を作成して `main` へ反映します。

---

# Pull Request (PR) の作成方法

## 1. GitHubを開く

リポジトリページへアクセスする。

---

## 2. 「Compare & pull request」をクリック

または、

```text
Pull requests
↓
New pull request
```

を選択する。

---

## 3. マージ先を確認

```text
base: main
compare: 自分のブランチ
```

例：

```text
base: main
compare: feature/ui
```

---

## 4. タイトルを記入する

### 良い例

```text
時間割表示機能を追加
講義検索機能を実装
卒業要件計算処理を修正
```

---

## 5. 説明欄を記入する

### 必ず記載する内容

#### ① 何を追加・修正したか

例：

```text
時間割表示機能を追加しました。
```

---

#### ② どのような操作をしたときに何が起きるか

例：

```text
講義を選択すると、右側の時間割へ自動追加されます。
```

```text
講義検索欄に講義名を入力すると、一致する講義のみ表示されます。
```

```text
履修講義を追加すると、不足単位数がリアルタイムで更新されます。
```

---

#### ③ 動作確認内容

例：

```text
【確認内容】
- 講義追加時に時間割へ反映されることを確認
- 講義削除時に時間割から削除されることを確認
- 他の画面表示に影響がないことを確認
```

---

### Pull Request 記入例

```text
## 変更内容
時間割表示機能を追加しました。

## 動作
講義一覧から講義を選択すると、時間割へ自動で追加されます。
講義を削除すると、時間割からも削除されます。

## 動作確認
- 講義追加時の表示確認
- 講義削除時の表示確認
- 他機能への影響がないことを確認
```

---

## 6. 「Create pull request」をクリック

---

## 7. レビュー後、「Merge pull request」

レビュー担当者の確認後にマージを行う。

---

# 困ったとき

## 現在のブランチ確認

```bash
git branch
```

`*` が付いているものが現在のブランチ。

---

## 変更状況確認

```bash
git status
```

---

## リモートリポジトリ確認

```bash
git remote -v
```

以下のように表示されればOK。

```text
origin  https://github.com/Waterseaocean/G1.git
origin  https://github.com/Waterseaocean/G1.git
```

---

## コンフリクト（競合）が発生した場合

```text
CONFLICT
```

と表示された場合は、勝手に解決せずチームメンバーまたはリーダーへ相談してください。

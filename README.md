# MMD Original Motion Maker

ブラウザ上でベースモーションを生成し、MMD用の `.vmd` ファイルとして保存する試作ツールです。

## GitHub Pagesで公開する方法（初心者向け）

1. GitHubにログインし、右上の `+` → `New repository` を選びます。
2. Repository name に `mmd-original-motion-maker` と入力します。
3. `Public` を選択し、`Create repository` を押します。
4. 作成したリポジトリで `Add file` → `Upload files` を選びます。
5. ZIPを展開し、中の `index.html` と `.nojekyll` をアップロードします。`README.md` も一緒にアップロードして構いません。
6. `Commit changes` を押して保存します。
7. リポジトリの `Settings` → `Pages` を開きます。
8. `Build and deployment` の `Source` で `Deploy from a branch` を選びます。
9. Branch を `main`、フォルダを `/(root)` にして `Save` を押します。
10. 少し待ってから `Settings` → `Pages` に戻り、表示された `Visit site` を押します。

公開URLは通常、`https://あなたのGitHubユーザー名.github.io/mmd-original-motion-maker/` の形式です。

公開反映には数分かかることがあります。GitHub Pagesは公開サイトがインターネット上で見られるため、個人情報や秘密情報はアップロードしないでください。

## 使い方

1. ページを開きます。
2. 曲の長さ、BPM、スタイル、動きの大きさを設定します。
3. `VMDを生成して保存` を押します。
4. 保存した `.vmd` をMMDで読み込み、モデルに合わせて動作を確認します。

## 注意

- 試作版です。完成された振付というより、編集の土台となるベースモーションを生成します。
- モデルによってボーン名や構造が異なるため、すべてのモデルで同じ動きになるとは限りません。
- 足IKやモデル固有ボーンの自動調整には未対応です。
- 公開前にMMDで動作確認し、必要に応じて改善してください。

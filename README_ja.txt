MMD Original Motion Maker（試作版）

内容:
- MMD_OriginalMotionMaker.py : Windows向けGUIツール。Python 3で実行
- sample_original_dance_120s_bpm120.vmd : 120秒/BPM120のサンプルVMD

使い方:
1. WindowsにPython 3をインストール（インストール時にAdd Python to PATHを有効にすると便利）。
2. MMD_OriginalMotionMaker.pyをダブルクリック、またはコマンドプロンプトで
   python MMD_OriginalMotionMaker.py
   と実行。
3. 長さ、BPM、雰囲気、動きの大きさを設定して「VMDを生成して保存」。
4. MMDでモデルを読み込み、モデルを選択した状態で生成したVMDを読み込んで再生確認。

注意:
- この試作版は、ボーンの回転とセンターの小さな移動を数式で生成する基本ツールです。
- 完成度の高い振り付けや、モデルごとのボーン差異、足IK、物理演算、曲のビート解析には未対応です。
- モデルに存在しないボーン名は無視される場合があります。MMDで必ず動作確認してください。
- サンプルVMDは技術確認用の初期サンプルで、完成済みの高品質ダンスモーションではありません。
- 元モーションの改変・配布をする場合は、配布規約を確認してください。

# Agent Handoff Rules

このファイルは、別のAgentが同じ運用方針で作業するための引き継ぎルールです。

## 目的

- Qlibで何ができるかを評価し、利用価値を判断する
- 現在は学習モデル中心ではなく、ルールベース戦略検討を優先する

## 必須ルール

1. 作業開始前にIssueを作る（日本語）
- 目的、作業内容、完了条件を明記する

2. 作業中はIssueに進捗コメントを残す（日本語）
- 何を変更したか
- 何を実行して確認したか
- 出力先（resultsパスなど）

3. ドキュメントは日本語で書く
- README
- docs/ 以下
- Issue本文・コメント

4. 変更後は必ず実行確認する
- スクリプトを実行して結果を確認
- 失敗時は原因と対応をIssueコメントに残す

5. Git運用
- 小さくコミットする
- mainへpush前に変更内容を確認する
- 破壊的操作（reset --hard など）はしない

## 推奨フロー

1. Issue作成
2. 実装
3. 実行確認
4. ドキュメント更新
5. コミット・push
6. Issueへ進捗コメント

## 現在の主要コマンド

- ルールベース単体実行
`python .\\scripts\\run_rule_backtest.py`

- ルールベース比較実行
`python .\\scripts\\run_rule_sweep.py`

- 学習モデル実行（必要時）
`python .\\scripts\\run_experiment.py`
`python .\\scripts\\export_report.py`

# AI Programmer – Code Reverse‑Engineering & Refactoring Assistant

> **Status : Experimental / PoC**  
> Phase 1（ファイルシステム解析）まで実装済み。次フェーズは Zod スキーマ定義と CLI 強化です。

---

## ✨ 主要コンセプト
| フェーズ | 概要 | 実装状況 |
|---------|------|----------|
| 1. Code Ingestion | ファイル走査・言語判定 | ✅ 完了 |
| 2. Dependency Analyzer | package.json 依存解析 | 🔄 進行中 |
| 3. Static Analyzer | Tree‑sitter AST / メトリクス | 🔜 次フェーズ |
| 4. AI Analyzer | LLM による意味解析 | 📝 未着手 |
| 5. Document Generator | YAML 生成 | 📝 未着手 |
| 6. Validation & Feedback | スキーマ検証・AI 評価 | 📝 未着手 |

詳細は **[`architecture.md`](./architecture.md)** を参照してください。

---

## ⚡ クイックスタート

```bash
# 1. Bun が入っていなければインストール
curl -fsSL https://bun.sh/install | bash

# 2. 依存インストール
bun install

# 3. テスト実行
bun test

# 4. 解析を試す
bun run src/cli.ts /path/to/your/project
```

> **Note:** CLI はまだ最小実装です。今後、`--format yaml` などのオプションが追加されます。

---

## 🗂️ プロジェクト構成（抜粋）

```
src/
├─ filesystem/            # Code Ingestion
│  └─ analyzer.ts
├─ analysis/
│  └─ dependencies/       # Dependency Analyzer
│     └─ packageManager.ts
└─ …
test/                     # bun:test によるユニットテスト
tasks.md                  # タスクと進捗
tech-stack.md             # 採用技術一覧
```

---

## 📅 ロードマップ / Next Actions
主要タスクの優先順位は **[`tasks.md`](./tasks.md#着手順タスクリスト-next-actions)** にまとめています。

---

## 🛠️ 開発環境

| ツール | バージョン | 備考 |
|--------|-----------|------|
| Bun | ≥ 1.0 | ランタイム・パッケージマネージャ |
| TypeScript | 5.x | 型チェック |
| globby | 14.x | ファイル走査 |
| zod | 3.x | スキーマ |


Docker / GitHub Actions は **保留中 (⏳)**。  
Tree‑sitter 導入タイミングで整備予定です。

---

## 🤝 Contributing

1. `fork` → `feature/<topic>` ブランチを作成  
2. `bun test` が緑になることを確認  
3. Pull Request を送ってください（小さめ歓迎）

スタイルガイド / CI は未整備ですが、Prettier 既定設定で整形するとマージがスムーズです。

---

## 📄 License

© 2025 Kotaro Ichihara. Licensed under the MIT License (see `LICENSE` for details).

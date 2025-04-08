# AIによるコードリバースエンジニアリングとリファクタリングシステム - アーキテクチャ設計

## 概要

このシステムは既存のコードベースを分析し、その構造、目的、依存関係、設計思想などを包括的に理解して、構造化されたドキュメントを生成します。生成されたドキュメントは、後続のAIによるリファクタリング作業のための詳細な設計図として活用されます。

## 全体アーキテクチャ

システムは以下の6つの主要フェーズで構成されます：

1. コード取り込みと初期解析フェーズ
2. 依存関係解析フェーズ
3. 静的コード解析フェーズ
4. 意味解析と抽象化フェーズ (AI活用)
5. ドキュメント生成フェーズ
6. 洗練・検証フェーズ

## 各フェーズの詳細

### 1. コード取り込みと初期解析フェーズ

#### 目的
- 対象コードベースの基本的な情報を収集
- 主要言語とプロジェクト構造の把握

#### 技術要素
- **ランタイム**: `Bun` (高速実行環境、TypeScriptネイティブサポート)
- **言語検出**: `guesslang` またはカスタム実装 (コンテンツベース推定も考慮)
- **ファイルシステム走査**: `fs/promises` + `globby` (非同期I/O、パターンマッチング)
- **エンコーディング検出**: `jschardet`
- **メタデータ抽出**: 基本的なファイル情報 (サイズ、更新日時など)
- **設定・無視ファイル解析**: `.gitignore` 等の考慮

#### 処理内容
1. ソースコードのディレクトリ構造を再帰的に走査
2. プロジェクト全体の言語分布を特定 (主要言語、補助言語)
3. ビルドファイル(`Makefile`, `package.json`など)を特定
4. 設定ファイル(`.env`, `config.yaml`など)を特定
5. テストディレクトリやドキュメントディレクトリを特定

### 2. 依存関係解析フェーズ

#### 目的
- 外部ライブラリ依存関係の把握
- 内部モジュール間の依存関係のマッピング

#### 技術要素
- **パッケージ依存関係**: 言語固有のパッケージマネージャ解析 (`depcheck` や `npm`, `pip` 等の解析)
  - npm: `package.json`と`package-lock.json`/`yarn.lock`/`pnpm-lock.yaml`解析
  - Python: `requirements.txt`, `pyproject.toml` (Poetry/PDM), `setup.py`, `Pipfile`解析
  - Java: `pom.xml`, `build.gradle`解析
- **コード内依存関係**: AST (`Tree-sitter` ベース) + 正規表現
  - `import`, `require`, `using`などの文の抽出
  - クラス・関数呼び出しの追跡 (限定的)
- **依存グラフ**: `graphology` (グラフデータ構造とアルゴリズム)

#### 処理内容
1. 言語に応じた適切な依存関係ファイルの解析
2. 各ファイル内のimport/require文の抽出
3. 依存関係グラフの構築（ノード：モジュール、エッジ：依存関係）
4. 循環依存や過度の依存などのアンチパターン検出

### 3. 静的コード解析フェーズ

#### 目的
- コードの構造と品質に関する客観的な情報収集
- 言語特性を活かした深い解析

#### 技術要素
- **AST生成**: `Tree-sitter` (多言語対応、堅牢性、インクリメンタル解析)
- **メトリクス計測**:
  - 複雑度: `escomplex` (JS), `radon` (Python)など言語固有ツール (サイクロマティック、認知的、Halstead)
  - コード品質: `ESLint` (API), `SonarQube`, `CodeQL` (連携可能性)
  - コードクローン検出: `jscpd`
- **パターン検出**: `Semgrep` (カスタムルールセットによるデザインパターン、アンチパターン検出)

#### 処理内容
1. ファイルごとのAST生成
2. シンボル抽出（関数、クラス、変数、定数など）
3. 複雑度メトリクス計測（サイクロマティック複雑度、Halstead複雑度など）
4. 制御フローグラフ(CFG)とデータフローグラフ(DFG)の生成
5. コーディングスタイルの分析（命名規則、インデント、行長など）
6. デザインパターンの検出（Singleton, Factory, Observer, etc）
7. アンチパターンの検出（コードの臭い、重複コードなど）

### 4. 意味解析と抽象化フェーズ (AI活用)

#### 目的
- コードの「意図」と「目的」の理解
- 人間が理解しやすい抽象概念への変換

#### 技術要素
- **大規模言語モデル (LLM)**: `OpenAI API` / `Google Gemini API` (複数プロバイダ対応、フォールバック)
- **LLM連携**: `LangChain.js` (プロンプトチェーン、コンテキスト管理), 各社SDK
- **プロンプト設計**: 特化した指示セットと少数ショット学習例 (テンプレートエンジン: `Handlebars`)
- **コンテキスト管理**: コードの関連部分 (ASTノード、依存関係) をまとめて提供する仕組み
- **バッチ処理**: レート制限を考慮したカスタムキュー実装

#### プロンプト設計詳細
- **基本構造**:
  ```
  システム: あなたは経験豊富なソフトウェアエンジニアです。以下のコードスニペットの目的と設計意図を分析してください。
  
  [コンテキスト情報]
  ファイルパス: {file_path}
  言語: {language}
  関連する依存関係: {dependencies}
  
  [コードスニペット]
  {code_snippet}
  
  [タスク]
  - このコードの主な目的を3-5文で説明してください。
  - 使用されている設計パターンや思想を特定してください。
  - 潜在的な問題点や改善可能な箇所を指摘してください。
  - このコードが解決しようとしている技術的課題は何ですか？
  
  [出力形式]
  目的: {目的の説明}
  設計: {設計パターンや思想}
  課題: {解決している技術的課題}
  問題点: {潜在的な問題のリスト}
  ```

- **精度向上策**:
  - Chain-of-Thoughtプロンプティング
  - 静的解析結果のプロンプトへの組み込み
  - 複数のコード断片を関連づけるためのコンテキスト提供

#### 処理内容
1. 各ファイル/クラス/関数に対して適切な粒度でAIに解析させる
2. ファイル全体→クラス→関数の階層的な分析
3. 関連するコード部分を集めた「機能グループ」の分析も実施
4. AIの出力を構造化された形式に変換
5. 一貫性のない回答や曖昧な回答に対してはフォローアップ質問

### 5. ドキュメント生成フェーズ

#### 目的
- 収集した情報を統合し、構造化された形式で表現
- **データモデル**: `Zod` によるスキーマ定義とランタイム検証

#### 技術要素
- **データ構造化**: `Zod` スキーマに基づいたTypeScriptオブジェクト
- **出力形式**:
  - **YAML**: `js-yaml` (主要出力形式)
  - **JSON**: スキーマに基づいた変換
  - **Markdown/HTML**: `Handlebars` テンプレートによる生成 (オプション)
- **スキーマ**: プロジェクト、ファイル、シンボル、依存関係、メトリクス等を定義した `Zod` スキーマ

#### YAML出力形式例 (Zod スキーマに基づく構造)

```yaml
project_info:
  name: "プロジェクト名"
  root_path: "/path/to/project"
  main_language: "TypeScript"
  languages:
    - name: "TypeScript"
      percentage: 85.2
    - name: "Python"
      percentage: 10.5
    - name: "Markdown"
      percentage: 4.3
  dependencies:
    # package.json などから解析された依存関係
{{ ... }}
      maintainability_index: 65
      cognitive_complexity: 8 # 例: 認知的複雑度
    structure:
      - type: "class"
        name: "クラス名"
        signature: "クラス定義シグネチャ"
        purpose: "このクラスの役割 (AIによる推定)"
        start_line: 10
        end_line: 150
        extends: ["親クラス1", "親クラス2"]
        implements: ["インターフェース1"]
        methods:
          - type: "method"
            name: "メソッド名"
            signature: "メソッド定義シグネチャ"
            purpose: "このメソッドの役割 (AIによる推定)"
            start_line: 25
            end_line: 50
            parameters:
              - name: "引数名1"
                type: "型名"
              - name: "引数名2"
                type: "型名"
            return_type: "戻り値型名"
            complexity: # メソッドレベルの複雑度
              cyclomatic: 5
            calls: ["呼び出し先関数1", "クラス名.メソッド名"]
            # ... 他のメソッド情報
        properties:
          - type: "property"
            name: "プロパティ名"
            property_type: "型名" # 'property_type' に変更 (typeは重複するため)
            access_modifier: "public/private/protected"
            start_line: 15
            end_line: 15
        # 以下、メソッドと同様の構造 (ネストされたクラス、関数など)
    patterns:
      - name: "検出されたデザインパターン名 (例: Singleton)"
        confidence: 0.85 # Semgrep/AIの確信度
        elements: ["関連する要素のパスや名前"]
    anti_patterns:
      - name: "検出されたアンチパターン名 (例: God Class)"
        severity: "high/medium/low"
        description: "問題の説明"
        location: "問題のあるコード箇所"
    ai_summary: "このファイル全体の機能や目的についてのAIによる要約"
    warnings:
      - severity: "high/medium/low"
        type: "問題の種類 (例: Lintエラー, セキュリティ脆弱性)"
{{ ... }}
### 6. 洗練・検証フェーズ

#### 目的
- 生成されたドキュメントの一貫性と正確性の確保
- `Zod` スキーマを用いたデータ整合性の検証
- 人間のフィードバックの取り込み (将来的なWeb UI経由も考慮)

#### 技術要素
- **バリデータ**: `Zod` スキーマによる自動検証 + カスタム検証ロジック
- **フィードバック**: インタラクティブなUI (`React` ベース) またはCLIインターフェース

#### 処理内容
1. 生成されたデータオブジェクトの `Zod` スキーマによるバリデーション
{{ ... }}
## モジュール設計

システムは以下の主要コンポーネント (モジュール) で構成されます (tech-stack.md の分類を参考に調整):

1.  **CodeIngestion**: コード取り込みと初期解析 (`ProjectScanner`, `LanguageDetector`, `EncodingDetector`)
2.  **DependencyAnalyzer**: 依存関係解析 (`ExternalDependencyParser`, `ImportAnalyzer`, `DependencyGraphBuilder` using `graphology`)
3.  **StaticAnalyzer**: 静的コード解析 (`ASTGenerator` using `Tree-sitter`, `SymbolExtractor`, `MetricsCalculator`, `PatternDetector` using `Semgrep`, `CloneDetector` using `jscpd`)
4.  **AIAnalyzer**: AI活用意味解析 (`PromptGenerator` using `Handlebars`, `LLMClient` (OpenAI/Gemini SDK), `ResponseParser`, `ContextManager` using `LangChain.js`)
5.  **DataModel**: コアデータ構造定義と検証 (`Zod` スキーマ)
6.  **DocumentGenerator**: ドキュメント生成 (`YAMLBuilder`, `JSONConverter`, `TemplateEngine` using `Handlebars`)
7.  **Orchestrator**: 全体処理フロー制御 (`Pipeline`, `ProgressTracker`, `ErrorHandler`, `CacheManager`)
8.  **(将来)** **WebInterface**: Web APIとフロントエンド (`APIServer` using `Hono`, `Frontend` using `React`, `CodeViewer` using `Monaco`, `GraphVisualizer` using `Cytoscape.js`)

## 運用フロー

1.  **初期設定**:
    *   対象コードベースの指定
    *   出力形式と詳細度の設定
    *   言語固有の解析設定（使用するパーサーやツール）
    *   AI APIキーなどの設定

2.  **実行 (CLI)**:
    *   コマンドラインから解析を実行 (`bun run analyze <path> [options]`)
    *   Orchestratorが各フェーズを制御
    *   フェーズごとの逐次処理（一部並列化可能: ファイル解析など）
    *   中間結果のキャッシュと再利用
    *   進捗状況のコンソール表示 (プログレスバー、ログ)

3.  **結果確認 (CLI / ファイル出力)**:
    *   指定された形式 (主にYAML) で解析結果を出力
    *   コンソールでのサマリー表示
    *   問題箇所や注意点のハイライト (将来的なCLI UIの高度化)

4.  **(将来) Web UIでの利用**:
    *   `Hono`ベースのAPIサーバーを起動
    *   `React`ベースのフロントエンドでプロジェクトを選択し解析実行
    *   解析結果をWeb UI上でインタラクティブに表示 (コードビューア、依存グラフ、メトリクス)
    *   フィードバックや再解析のトリガー

5.  **反復改善**:
    *   人間のフィードバック (CLI経由またはWeb UI経由) に基づく再解析
    *   特定のファイルや機能に焦点を当てた詳細解析
    *   ドキュメントの更新と履歴管理 (シンプルなファイルベース or DB)

## 次のステップ: リファクタリング支援

生成された構造化ドキュメント (YAML) は、AIによるリファクタリング計画の立案・実行の基盤となります:

1.  **問題箇所の特定と優先順位付け**:
    *   複雑度メトリクス (サイクロマティック、認知的) が高い箇所
    *   検出されたアンチパターンや設計パターン違反
    *   過度の依存関係 (グラフ分析)
    *   重複コード (コードクローン検出結果)
    *   AIによる潜在的な問題点の指摘

2.  **リファクタリング案のAI生成**:
    *   特定された問題箇所に対する具体的なコード改善提案 (例: 関数の抽出、クラスの分割、パターンの適用)
    *   LLMを活用し、リファクタリングの意図や手順を説明
    *   リファクタリング前後のコードスニペット比較
    *   期待される効果 (保守性向上、複雑度低下など) の説明

3.  **変更影響分析 (限定的)**:
    *   提案された変更が影響を与える可能性のある他のコード箇所を依存関係グラフから推定
    *   テストが必要となる箇所の示唆

4.  **段階的な実装支援**:
    *   テスト可能な単位でのリファクタリングの提案 (手動実行が前提)
    *   リファクタリング後の検証方法の提案 (関連テストの実行など)
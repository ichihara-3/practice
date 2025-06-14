# Gmail All Read

Gmailの未読メールを一括で既読にするPythonツールです。

## 概要

このツールはGmail APIを使用して、アカウント内のすべての未読メールを効率的に既読状態にします。大量の未読メールがある場合でも、バッチ処理により高速に処理できます。

## 機能

- Gmail APIを使用した安全な認証
- 未読メールの一括既読処理
- バッチ処理による高速処理（デフォルト100件ずつ）
- API制限を考慮した適切な待機時間
- 処理進捗の表示
- 実行前の確認プロンプト

## 必要な環境

- Python 3.11以上
- Google Cloud Platformのプロジェクト
- Gmail APIの有効化

## 初期設定

### 1. Google Cloud Consoleでのプロジェクト作成
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成または既存のプロジェクトを選択

### 2. Gmail APIの有効化
1. APIとサービス > ライブラリに移動
2. "Gmail API"を検索して有効化

### 3. OAuth 2.0クライアントの設定
1. **OAuth同意画面の設定**
   - APIとサービス > OAuth同意画面に移動
   - ユーザータイプで「外部」を選択（個人用の場合）
   - アプリ名、ユーザーサポートメール、デベロッパーの連絡先情報を入力
   - スコープの設定で `https://www.googleapis.com/auth/gmail.modify` を追加

2. **テストユーザーの追加**
   - OAuth同意画面の「テストユーザー」セクションで、使用するGmailアカウントを追加

3. **OAuth 2.0クライアントIDの作成**
   - APIとサービス > 認証情報に移動
   - 「認証情報を作成」> 「OAuth クライアント ID」を選択
   - アプリケーションの種類で「デスクトップアプリケーション」を選択
   - 作成されたクライアントIDの右側にあるダウンロードアイコンをクリック
   - ダウンロードしたJSONファイルを `credentials.json` にリネーム

### 4. credentials.jsonの配置
`credentials.json`をプロジェクトのルートディレクトリに配置

## 依存関係のインストール

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## 使用方法

```bash
python gmail_mark_read.py
```

初回実行時は認証フローが開始され、ブラウザでGoogleアカウントにログインする必要があります。認証情報は`token.pickle`ファイルに保存され、以降の実行では自動的に使用されます。

## ファイル構成

- `gmail_mark_read.py` - メインスクリプト
- `credentials.json` - Google OAuth認証情報（要配置）
- `token.pickle` - 認証トークン（自動生成）
- `pyproject.toml` - プロジェクト設定

## 注意事項

- 大量のメールを処理する場合は時間がかかる場合があります
- Gmail APIの使用制限に注意してください
- 重要なメールを既読にする前に、必要に応じてバックアップを取ることをお勧めします
- OAuth同意画面でアプリが「未確認」と表示されますが、テストユーザーとして追加したアカウントでは正常に動作します

## トラブルシューティング

### 認証エラーが発生する場合
- `token.pickle`ファイルを削除して再認証を試してください
- OAuth同意画面でテストユーザーが正しく追加されているか確認してください

### API制限エラーが発生する場合
- しばらく時間をおいてから再実行してください
- バッチサイズを小さく調整することを検討してください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
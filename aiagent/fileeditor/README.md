# File Editor

ファイル操作のための Python MCPツール

## 機能一覧

### ファイル管理機能

#### write_file
ファイルを作成または上書きします。
```python
await write_file(file_path: str, content: str, overwrite: bool = False)
```
- `file_path`: 作成/上書きするファイルのパス
- `content`: ファイルに書き込む内容
- `overwrite`: 既存ファイルを上書きするかどうか（デフォルトはFalse）

#### append_file
既存のファイルに内容を追記します。
```python
await append_file(file_path: str, content: str)
```
- `file_path`: 追記するファイルのパス
- `content`: 追記する内容

#### copy_file
ファイルをコピーします。
```python
await copy_file(source_path: str, destination_path: str, overwrite: bool = False)
```
- `source_path`: コピー元のファイルパス
- `destination_path`: コピー先のファイルパス
- `overwrite`: 既存ファイルを上書きするかどうか（デフォルトはFalse）

#### move_file
ファイルを移動またはリネームします。
```python
await move_file(source_path: str, destination_path: str, overwrite: bool = False)
```
- `source_path`: 移動元のファイルパス
- `destination_path`: 移動先のファイルパス
- `overwrite`: 既存ファイルを上書きするかどうか（デフォルトはFalse）

#### delete_file
ファイルを削除します。
```python
await delete_file(file_path: str, force: bool = False)
```
- `file_path`: 削除するファイルのパス
- `force`: 確認なしで削除するかどうか（デフォルトはFalse）

### ファイル表示・検索機能

#### read_file
ファイルの内容を読み取ります。
```python
await read_file(file_path: str)
```
- `file_path`: 読み取るファイルのパス

#### show_tree
ディレクトリのファイルツリーを表示します。
```python
await show_tree(path: str = ".")
```
- `path`: ツリーを表示するディレクトリのパス（デフォルトは現在のディレクトリ）

#### list_files
ディレクトリ内のファイルとフォルダの一覧を表示します。
```python
await list_files(path: str = ".", show_hidden: bool = False)
```
- `path`: 一覧を表示するディレクトリのパス（デフォルトは現在のディレクトリ）
- `show_hidden`: 隠しファイルを表示するかどうか（デフォルトはFalse）

#### search_files
指定したパターンに一致するファイルを検索します。
```python
await search_files(pattern: str, path: str = ".", recursive: bool = True)
```
- `pattern`: 検索パターン（ワイルドカード*や?をサポート）
- `path`: 検索を開始するディレクトリ（デフォルトは現在のディレクトリ）
- `recursive`: サブディレクトリも検索するかどうか（デフォルトはTrue）

### その他の機能

#### file_info
ファイルの詳細情報を取得します。
```python
await file_info(file_path: str)
```
- `file_path`: 情報を取得するファイルのパス

#### change_directory
作業ディレクトリを変更します。
```python
await change_directory(path: str)
```
- `path`: 移動先のディレクトリパス

#### get_current_directory
現在の作業ディレクトリを取得します。
```python
await get_current_directory()
```

#### get_absolute_path
指定されたパスの絶対パスを取得します。
```python
await get_absolute_path(path: str = ".")
```
- `path`: 絶対パスを取得したいパス（デフォルトは現在のディレクトリ）

## エラーハンドリング

各機能は以下のような状況で適切なエラーメッセージを返します：

- ファイルが存在しない場合
- パーミッションが不足している場合
- ディスク容量が不足している場合
- パスが無効な場合
- ファイル操作中にエラーが発生した場合

エラーは全てログファイルに記録され、エラーメッセージが返されます。

## 使用例

```python
# ファイルの作成
await write_file("example.txt", "Hello, World!")

# ファイルの追記
await append_file("example.txt", "\nNew line")

# ファイルのコピー
await copy_file("example.txt", "backup/example.txt")

# ファイルの移動
await move_file("old_name.txt", "new_name.txt")

# ファイルの削除（確認付き）
await delete_file("temp.txt")  # 確認メッセージが返される
await delete_file("temp.txt", force=True)  # 直接削除

# ファイル内容の表示
content = await read_file("example.txt")
print(content)

# ディレクトリ構造の表示
tree = await show_tree()
print(tree)

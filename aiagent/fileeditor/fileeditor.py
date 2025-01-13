import logging
import os
import glob
from datetime import datetime
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP

logging.basicConfig(filename='fileviewer.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

mcp = FastMCP("fileviewer")

# 現在の作業ディレクトリを保持するグローバル変数
current_directory = Path.cwd()

def format_tree(path: Path, prefix: str = "", is_last: bool = True) -> str:
    """ディレクトリツリーを整形して返す補助関数"""
    output = prefix + ("└── " if is_last else "├── ") + path.name + "\n"
    
    if path.is_dir():
        # ディレクトリ内のエントリを取得してソート
        entries = sorted(list(path.iterdir()))
        
        # 各エントリに対して再帰的にツリーを生成
        for i, entry in enumerate(entries):
            is_last_entry = i == len(entries) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")
            output += format_tree(entry, new_prefix, is_last_entry)
    
    return output

@mcp.tool()
async def read_file(file_path: str) -> str:
    """指定されたファイルの内容を読み取る

    Args:
        file_path: 読み取るファイルのパス（相対パスまたは絶対パス）
    """
    global current_directory
    try:
        # 相対パスの場合は現在のディレクトリからの相対パスとして解決
        file_path = current_directory / file_path
        
        if not file_path.is_file():
            return f"Error: File not found - {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def show_tree(path: str = ".") -> str:
    """指定されたディレクトリのファイルツリーを表示する

    Args:
        path: ツリーを表示するディレクトリのパス（デフォルトは現在のディレクトリ）
    """
    global current_directory
    try:
        # 相対パスの場合は現在のディレクトリからの相対パスとして解決
        target_path = current_directory / path
        
        if not target_path.exists():
            return f"Error: Path not found - {target_path}"
        
        if not target_path.is_dir():
            return f"Error: Not a directory - {target_path}"
        
        tree = format_tree(target_path)
        return tree
    except Exception as e:
        logger.error(f"Error showing tree: {e}")
        return f"Error showing tree: {str(e)}"

@mcp.tool()
async def get_current_directory() -> str:
    """現在のディレクトリを取得する"""
    global current_directory
    return str(current_directory)

@mcp.tool()
async def get_absolute_path(path: str = ".") -> str:
    """指定されたパスの絶対パスを取得する

    Args:
        path: 絶対パスを取得したいパス（デフォルトは現在のディレクトリ）
    """
    global current_directory
    try:
        absolute_path = (current_directory / path).resolve()
        return str(absolute_path)
    except Exception as e:
        logger.error(f"Error getting absolute path: {e}")
        return f"Error getting absolute path: {str(e)}"

@mcp.tool()
async def list_files(path: str = ".", show_hidden: bool = False) -> str:
    """指定されたディレクトリ内のファイルとフォルダの一覧を表示する

    Args:
        path: 一覧を表示するディレクトリのパス（デフォルトは現在のディレクトリ）
        show_hidden: 隠しファイルを表示するかどうか（デフォルトはFalse）

    Returns:
        str: ファイル一覧を整形した文字列
    """
    global current_directory
    try:
        # 相対パスの場合は現在のディレクトリからの相対パスとして解決
        target_path = (current_directory / path).resolve()
        
        if not target_path.exists():
            return f"Error: Path not found - {target_path}"
        
        if not target_path.is_dir():
            return f"Error: Not a directory - {target_path}"
        
        # ディレクトリ内のエントリを取得してソート
        entries = sorted(target_path.iterdir())
        
        # 結果を整形
        result = []
        for entry in entries:
            # 隠しファイルの処理
            if not show_hidden and entry.name.startswith('.'):
                continue
                
            try:
                # ファイル情報の取得
                stats = entry.stat()
                size = stats.st_size
                modified = stats.st_mtime
                
                # 日時のフォーマット
                modified_str = datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
                
                # ディレクトリの場合は末尾に/を付加
                name = entry.name + ('/' if entry.is_dir() else '')
                
                # エントリ情報の整形
                result.append(f"{name:<30} {size:>10} bytes  {modified_str}")
                
            except PermissionError:
                logger.error(f"Permission denied: {entry}")
                result.append(f"{entry.name:<30} <Permission Denied>")
            except Exception as e:
                logger.error(f"Error processing entry {entry}: {e}")
                result.append(f"{entry.name:<30} <Error>")
        
        return "\n".join(result) if result else "Directory is empty"
        
    except PermissionError:
        error_msg = f"Permission denied: {target_path}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error listing files: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def search_files(pattern: str, path: str = ".", recursive: bool = True) -> str:
    """指定されたパターンに一致するファイルやディレクトリを検索する

    Args:
        pattern: 検索パターン（ワイルドカード*や?をサポート）
        path: 検索を開始するディレクトリ（デフォルトは現在のディレクトリ）
        recursive: サブディレクトリも検索するかどうか（デフォルトはTrue）

    Returns:
        str: 検索結果を整形した文字列
    """
    global current_directory
    try:
        # 相対パスの場合は現在のディレクトリからの相対パスとして解決
        target_path = (current_directory / path).resolve()
        
        if not target_path.exists():
            return f"Error: Path not found - {target_path}"
        
        if not target_path.is_dir():
            return f"Error: Not a directory - {target_path}"
        
        # 検索パターンの構築
        if recursive:
            search_pattern = f"**/{pattern}"
        else:
            search_pattern = pattern
            
        # globを使用してファイルを検索
        matches = list(target_path.glob(search_pattern))
        
        if not matches:
            return f"No files found matching pattern: {pattern}"
        
        # 結果を整形
        result = []
        for entry in sorted(matches):
            try:
                # ファイル情報の取得
                stats = entry.stat()
                size = stats.st_size
                modified = stats.st_mtime
                
                # 日時のフォーマット
                modified_str = datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
                
                # 相対パスの取得
                rel_path = entry.relative_to(target_path)
                name = str(rel_path) + ('/' if entry.is_dir() else '')
                
                # エントリ情報の整形
                result.append(f"{name:<50} {size:>10} bytes  {modified_str}")
                
            except PermissionError:
                logger.error(f"Permission denied: {entry}")
                result.append(f"{entry.relative_to(target_path):<50} <Permission Denied>")
            except Exception as e:
                logger.error(f"Error processing entry {entry}: {e}")
                result.append(f"{entry.relative_to(target_path):<50} <Error>")
        
        return "\n".join(result)
        
    except ValueError as e:
        error_msg = f"Invalid search pattern: {pattern}"
        logger.error(f"{error_msg}: {e}")
        return error_msg
    except Exception as e:
        error_msg = f"Error searching files: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def file_info(file_path: str) -> str:
    """指定されたファイルの詳細情報を取得する

    Args:
        file_path: 情報を取得するファイルのパス（相対パスまたは絶対パス）

    Returns:
        str: ファイルの詳細情報を整形した文字列
    """
    global current_directory
    try:
        # 相対パスの場合は現在のディレクトリからの相対パスとして解決
        path = (current_directory / file_path).resolve()
        
        if not path.exists():
            return f"Error: Path not found - {path}"
        
        # ファイル情報の取得
        stats = path.stat()
        
        # ファイルタイプの判定
        file_type = "Directory" if path.is_dir() else "File"
        if path.is_symlink():
            file_type = "Symbolic Link"
        
        # パーミッションの取得（8進数表記）
        perms = oct(stats.st_mode)[-3:]
        
        # 日時情報のフォーマット
        modified_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        access_time = datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
        create_time = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        
        # 所有者情報の取得（可能な場合）
        try:
            import pwd
            owner = pwd.getpwuid(stats.st_uid).pw_name
        except (ImportError, KeyError):
            owner = str(stats.st_uid)
        
        # 情報の整形
        info = [
            f"Name: {path.name}",
            f"Type: {file_type}",
            f"Size: {stats.st_size:,} bytes",
            f"Permissions: {perms} ({path.stat().st_mode & 0o777:03o})",
            f"Owner: {owner}",
            f"Created: {create_time}",
            f"Modified: {modified_time}",
            f"Accessed: {access_time}"
        ]
        
        # シンボリックリンクの場合、リンク先を表示
        if path.is_symlink():
            info.append(f"Links to: {path.readlink()}")
        
        return "\n".join(info)
        
    except PermissionError:
        error_msg = f"Permission denied: {file_path}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error getting file info: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def change_directory(path: str) -> str:
    """作業ディレクトリを変更する

    Args:
        path: 移動先のディレクトリパス（相対パスまたは絶対パス）
    """
    global current_directory
    try:
        # 相対パスの場合は現在のディレクトリからの相対パスとして解決
        new_path = (current_directory / path).resolve()
        
        if not new_path.exists():
            return f"Error: Directory not found - {new_path}"
        
        if not new_path.is_dir():
            return f"Error: Not a directory - {new_path}"
        
        current_directory = new_path
        return f"Changed directory to: {new_path}"
    except Exception as e:
        logger.error(f"Error changing directory: {e}")
        return f"Error changing directory: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    logger.info("Starting fileviewer server...")
    mcp.run(transport='stdio')

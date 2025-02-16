import anthropic
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def read_text_file(file_path):
    """Read a text file and return its contents."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_quotes(client, text, title):
    """Extract quotes from text using Citations feature."""
    system_prompt = """
あなたは日本文学作品から印象的な一節を抽出する専門家です。
これらの作品は青空文庫で公開されている著作権切れの作品です。

以下の基準で、テキストから重要な一節を見つけ出してください。
必ず原文から直接引用し、引用符「」で囲んで提示してください。

抽出基準と出力形式:

1. 人生の真理
- 人間の本質や生き方について述べている一文を抽出
例：「人の心を疑うのは、最も恥ずべき悪徳だ」

2. 心情の転換点
- 登場人物の心境や決意が大きく変わる瞬間の一文を抽出
例：「私は走ったのだ。君を欺くつもりは、みじんも無かった」

3. 印象的な描写
- 情景や心情を鮮やかに表現している一文を抽出
例：「メロスは、黒い風のように走った」

4. 作品のテーマ
- 作品の中心的なメッセージを端的に表している一文を抽出
例：「正義とは、決して空虚な妄想ではなかった」

各引用について：
引用：「」で囲んだ原文の一文
場面：その一文が登場する場面の説明（簡潔に）
意義：なぜこの一文が重要なのか（テーマとの関連や効果）

注意：
- 必ず原文から正確に引用してください
- 一文単位で抽出してください（長すぎる引用は避ける）
- 各カテゴリから1-2個ずつ抽出してください
- 引用の前後の文脈も考慮して選んでください
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=2000,
        temperature=0,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "text",
                        "media_type": "text/plain",
                        "data": text
                    },
                    "title": title,
                    "context": "これは青空文庫で公開されている著作権切れの作品です。",
                    "citations": {"enabled": True}
                },
                {
                    "type": "text",
                    "text": "この作品から重要な一文を抽出し、各文の意味や価値を説明してください。必ず原文から正確に引用し、引用符「」で囲んで示してください。"
                }
            ]
        }]
    )
    
    return message.content

def main():
    # APIキーの設定
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # テキストファイルの読み込み
    artifacts_dir = Path(__file__).parent / "artifacts"
    
    # 走れメロスの処理
    print("=== 走れメロス の引用 ===")
    melos_path = artifacts_dir / "hashire_merosu.txt"
    melos_text = read_text_file(melos_path)
    melos_response = extract_quotes(client, melos_text, "走れメロス")
    
    # デバッグ出力
    print("Debug - Response type:", type(melos_response))
    if hasattr(melos_response, 'content'):
        print("Debug - Has content attribute")
        print("Debug - Content:", melos_response.content)
    else:
        print("Debug - Direct response:", melos_response)
    
    # 羅生門の処理
    print("\n=== 羅生門 の引用 ===")
    rashomon_path = artifacts_dir / "rashomon.txt"
    rashomon_text = read_text_file(rashomon_path)
    rashomon_response = extract_quotes(client, rashomon_text, "羅生門")
    
    # デバッグ出力
    print("Debug - Response type:", type(rashomon_response))
    if hasattr(rashomon_response, 'content'):
        print("Debug - Has content attribute")
        print("Debug - Content:", rashomon_response.content)
    else:
        print("Debug - Direct response:", rashomon_response)

if __name__ == "__main__":
    main()

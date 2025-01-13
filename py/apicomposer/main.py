from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

def main():
    client = openai.OpenAI(api_key=openai_api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": "こんにちは！"},
                {"role": "assistant", "content": "こんにちは！お手伝いできることはありますか？"},
                {"role": "user", "content": "今日の天気について教えてください"}
            ],
            temperature=0.7
        )
        
        # レスポンスから回答を取得して表示
        print(response.choices[0].message.content)
        
    except openai.OpenAIError as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()

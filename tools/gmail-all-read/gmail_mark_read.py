import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

# Gmail APIのスコープ
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    """Gmail APIの認証を行う"""
    creds = None
    
    # token.pickleファイルがあれば読み込む
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # 認証情報が無効または存在しない場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # credentials.jsonファイルが必要
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 認証情報を保存
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def mark_all_as_read(service, batch_size=100):
    """すべての未読メールを既読にする"""
    try:
        print("未読メールを取得中...")
        
        # 未読メールのIDを取得
        results = service.users().messages().list(
            userId='me', 
            q='is:unread',
            maxResults=1000  # 一度に取得する最大数
        ).execute()
        
        messages = results.get('messages', [])
        total_messages = len(messages)
        
        if not messages:
            print("未読メールはありません。")
            return
        
        print(f"未読メール数: {total_messages}件")
        
        # バッチ処理で既読にする
        processed = 0
        
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i + batch_size]
            message_ids = [msg['id'] for msg in batch]
            
            # batchModifyを使用して一括処理
            service.users().messages().batchModify(
                userId='me',
                body={
                    'ids': message_ids,
                    'removeLabelIds': ['UNREAD']
                }
            ).execute()
            
            processed += len(batch)
            print(f"処理済み: {processed}/{total_messages}件")
            
            # API制限を考慮して少し待機
            time.sleep(0.1)
        
        print("すべてのメールが既読になりました！")
        
        # 次のページがある場合の処理
        while 'nextPageToken' in results:
            results = service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=1000,
                pageToken=results['nextPageToken']
            ).execute()
            
            messages = results.get('messages', [])
            if messages:
                print(f"追加で{len(messages)}件の未読メールを処理中...")
                # 同様の処理を繰り返し
                for i in range(0, len(messages), batch_size):
                    batch = messages[i:i + batch_size]
                    message_ids = [msg['id'] for msg in batch]
                    
                    service.users().messages().batchModify(
                        userId='me',
                        body={
                            'ids': message_ids,
                            'removeLabelIds': ['UNREAD']
                        }
                    ).execute()
                    
                    processed += len(batch)
                    print(f"処理済み: {processed}件")
                    time.sleep(0.1)
        
    except HttpError as error:
        print(f'エラーが発生しました: {error}')

def main():
    """メイン処理"""
    print("Gmail API で全メールを既読にします...")
    
    # 認証
    service = authenticate_gmail()
    
    # 確認
    response = input("本当にすべての未読メールを既読にしますか？ (y/N): ")
    if response.lower() != 'y':
        print("キャンセルしました。")
        return
    
    # 実行
    mark_all_as_read(service)

if __name__ == '__main__':
    main()
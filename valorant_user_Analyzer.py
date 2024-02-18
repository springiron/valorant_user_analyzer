import requests


# ユーザー入力の受け取り
api_key = input("Riot GamesのAPIキーを入力してください: ")
game_name = input("プレイヤーのゲーム名を入力してください: ")
tag_line = input("プレイヤーのタグラインを入力してください: ")

tag_line = "8200"
region = "asia"  # Riotアカウントサービスの地域コード
val_region = "ap"  # VALORANTのマッチ情報を取得するための地域コード

# PUUIDの取得
account_url = f"https://riot.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
headers = {"X-Riot-Token": api_key}
account_response = requests.get(account_url, headers=headers)

if account_response.status_code == 200:
    puuid = account_response.json()["puuid"]
    print("PUUID:", puuid)
    
    # 最近の5マッチの履歴を取得
    matchlist_url = f"https://{val_region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}?count=5"
    matchlist_response = requests.get(matchlist_url, headers=headers)
    
    if matchlist_response.status_code == 200:
        match_ids = [match["matchId"] for match in matchlist_response.json()["history"]]
        print("取得したマッチIDのリスト:", match_ids)
        
        # 各マッチIDに対する詳細情報を取得
        for match_id in match_ids:
            match_details_url = f"https://{val_region}.api.riotgames.com/val/match/v1/matches/{match_id}"
            match_details_response = requests.get(match_details_url, headers=headers)
            
            if match_details_response.status_code == 200:
                match_details = match_details_response.json()
                print(f"マッチ {match_id} の詳細:", match_details)
            else:
                print(f"マッチ {match_id} の詳細取得に失敗しました。ステータスコード: {match_details_response.status_code}")
    else:
        print("マッチリストの取得に失敗しました。ステータスコード:", matchlist_response.status_code)
else:
    print("PUUIDの取得に失敗しました。ステータスコード:", account_response.status_code)

import requests
import pandas as pd
import datetime

def fetch_latest_data():
    # 這裡是示範的抓取邏輯，你需要替換成你真正抓資料的程式碼
    # 例如從 https://bingo.kuaishou1688.com/ 抓 JSON 或 HTML
    
    # 模擬抓到資料，建立 DataFrame
    today = datetime.date.today().strftime("%Y-%m-%d")
    data = {
        "日期": [today]*3,
        "期數": [1, 2, 3],
        "類別": ["2連號", "3連號", "2同出"],
        "組合號碼": ["01 02", "03 04 05", "06 07"],
        "出現次數": [10, 5, 8],
    }
    df = pd.DataFrame(data)
    return df

def update_csv():
    df_new = fetch_latest_data()
    try:
        df_old = pd.read_csv("bingo_daily_stats_long.csv", encoding="utf-8-sig")
        # 合併新舊資料，避免重複
        df = pd.concat([df_old, df_new]).drop_duplicates(subset=["日期","期數","類別","組合號碼"])
    except FileNotFoundError:
        df = df_new

    df.to_csv("bingo_daily_stats_long.csv", index=False, encoding="utf-8-sig")
    print(f"{datetime.datetime.now()} - CSV 更新完成，共 {len(df)} 筆資料")

if __name__ == "__main__":
    update_csv()
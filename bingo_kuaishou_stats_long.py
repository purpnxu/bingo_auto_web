import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from itertools import combinations
from datetime import datetime
import schedule
import time
import csv
import os

# --------------------- 配置 ---------------------
URL = "https://bingo.kuaishou1688.com/"
CSV_FILE = "bingo_daily_stats_long.csv"
RUN_TIME = "23:30"  # 每天抓取時間 (24h)
TOP_N = 20  # 每類統計前 N 名
# ------------------------------------------------

def fetch_data():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        print("等待頁面超時", e)
        driver.quit()
        return []

    time.sleep(3)  # 等待 JS 完成渲染

    html = driver.page_source
    driver.quit()

    lines = re.findall(r"\b([0-9]{1,2})\b", html)
    nums = [int(x) for x in lines if 1 <= int(x) <= 80]

    all_numbers = []
    group = []
    for num in nums:
        group.append(num)
        if len(group) == 20:
            all_numbers.append(sorted(group))
            group = []

    return all_numbers

def analyze_numbers(all_numbers):
    seq2 = Counter()
    seq3 = Counter()
    same2 = Counter()
    same3 = Counter()

    for numbers in all_numbers:
        unique = sorted(set(numbers))
        # 2連 / 3連
        for i in range(len(unique)-1):
            if unique[i+1] == unique[i]+1:
                seq2[(unique[i], unique[i+1])] += 1
                if i < len(unique)-2 and unique[i+2] == unique[i]+2:
                    seq3[(unique[i], unique[i+1], unique[i+2])] += 1
        # 2同 / 3同
        for c2 in combinations(unique,2):
            same2[c2] += 1
        for c3 in combinations(unique,3):
            same3[c3] += 1

    return seq2, seq3, same2, same3

def save_csv_long_format(date_str, total_periods, seq2, seq3, same2, same3):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE,"a",newline="",encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["日期","期數","類別","組合號碼","出現次數"])
        for combo, count in seq2.most_common(TOP_N):
            writer.writerow([date_str, total_periods, "2連號", " ".join(f"{n:02d}" for n in combo), count])
        for combo, count in seq3.most_common(TOP_N):
            writer.writerow([date_str, total_periods, "3連號", " ".join(f"{n:02d}" for n in combo), count])
        for combo, count in same2.most_common(TOP_N):
            writer.writerow([date_str, total_periods, "2同出", " ".join(f"{n:02d}" for n in combo), count])
        for combo, count in same3.most_common(TOP_N):
            writer.writerow([date_str, total_periods, "3同出", " ".join(f"{n:02d}" for n in combo), count])

def job():
    print("抓取資料:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    all_numbers = fetch_data()
    total_periods = len(all_numbers)

    if total_periods == 0:
        print("抓不到任何有效號碼")
        return

    seq2, seq3, same2, same3 = analyze_numbers(all_numbers)
    save_csv_long_format(datetime.now().strftime("%Y-%m-%d"), total_periods, seq2, seq3, same2, same3)

    print(f"完成更新，目前共 {total_periods} 期")
    print("前 20 名 2連號:", seq2.most_common(TOP_N))
    print("前 20 名 3連號:", seq3.most_common(TOP_N))
    print("前 20 名 2同出:", same2.most_common(TOP_N))
    print("前 20 名 3同出:", same3.most_common(TOP_N))
    print("-"*50)

if __name__=="__main__":
    print("Bingo 最終穩定自動統計系統 啟動")
    print("每日抓取時間:", RUN_TIME)
    job()  # 啟動先跑一次
    schedule.every().day.at(RUN_TIME).do(job)
    print("按 Ctrl+C 可強制關閉\n")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n已手動停止系統")
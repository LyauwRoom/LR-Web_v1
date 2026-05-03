import requests
import json
import csv
import os
from io import StringIO

CONFIG = {
    "global": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=0&single=true&output=csv",
    "static_pages": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=999625505&single=true&output=csv",
    "blog": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=1581291519&single=true&output=csv"
}

def fetch_raw_rows(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8-sig'
    f = StringIO(resp.text)
    return list(csv.reader(f))

def sync():
    cms_data = {"global": {}, "static_pages": {}, "blog": []}
    print("--- 启动位置识别同步 v2.0.03 ---")

    # 1. 处理 Global (第1列是 ID, 第2列是内容)
    rows = fetch_raw_rows(CONFIG["global"])
    if len(rows) > 1:
        for row in rows[1:]: # 跳过标题行
            if len(row) >= 2 and row[0].strip():
                cms_data["global"][row[0].strip()] = row[1].strip()

    # 2. 处理 Static_pages (第3列是 ID, 第4列是内容)
    rows = fetch_raw_rows(CONFIG["static_pages"])
    if len(rows) > 1:
        for row in rows[1:]:
            if len(row) >= 4 and row[2].strip():
                cms_data["static_pages"][row[2].strip()] = row[3].strip()

    # 3. 处理 Blog (保持原样，直接读取所有列)
    blog_rows = fetch_raw_rows(CONFIG["blog"])
    if len(blog_rows) > 0:
        headers = [h.strip() for h in blog_rows[0]]
        for row in blog_rows[1:]:
            cms_data["blog"].append(dict(zip(headers, row)))

    # 保存到 web_v1 文件夹
    os.makedirs('web_v1', exist_ok=True)
    with open('web_v1/data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    
    print("--- 同步成功！data.json 已更新 ---")

if __name__ == "__main__":
    sync()
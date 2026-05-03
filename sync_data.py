import requests
import json
import csv
import os
from io import StringIO

# 确认过的配置信息
CONFIG = {
    "global": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=0&single=true&output=csv",
    "static_pages": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=999625505&single=true&output=csv",
    "blog": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=1581291519&single=true&output=csv"
}

def fetch_csv_dicts(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.encoding = 'utf-8-sig'
        if resp.status_code != 200: return []
        
        f = StringIO(resp.text)
        reader = csv.DictReader(f)
        
        cleaned_data = []
        for row in reader:
            clean_row = {}
            for k, v in row.items():
                if k is not None:
                    key = str(k).strip()
                    # 修正点：确保 v 不为 None，否则赋予空字符串，避免 .strip() 报错
                    val = str(v).strip() if v is not None else ""
                    clean_row[key] = val
            
            # 只有当这一行不完全为空时才添加
            if any(clean_row.values()):
                cleaned_data.append(clean_row)
        return cleaned_data
    except Exception as e:
        print(f"读取出错: {e}")
        return []

def sync():
    cms_data = {"global": {}, "static_pages": {}, "blog": []}
    print("--- 启动同步 ---")

    # 1. 处理 Global
    global_rows = fetch_csv_dicts(CONFIG["global"])
    for r in global_rows:
        kid = r.get('ID') or r.get('id')
        if kid: cms_data["global"][kid] = r.get('content', '')

    # 2. 处理 Static Pages (使用你确认的 html_ID)
    static_rows = fetch_csv_dicts(CONFIG["static_pages"])
    for r in static_rows:
        hid = r.get('html_ID')
        if hid: cms_data["static_pages"][hid] = r.get('content', '')

    # 3. 处理 Blog
    cms_data["blog"] = fetch_csv_dicts(CONFIG["blog"])

    # 4. 写入文件到 web_v1/data.json
    os.makedirs('web_v1', exist_ok=True)
    with open('web_v1/data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    
    print("--- 同步成功 ---")

if __name__ == "__main__":
    sync()

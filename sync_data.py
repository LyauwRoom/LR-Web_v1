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
                    val = str(v).strip() if v is not None else ""
                    clean_row[key] = val
            
            if any(clean_row.values()):
                cleaned_data.append(clean_row)
        return cleaned_data
    except Exception as e:
        print(f"读取出错: {e}")
        return []

# 新增：自动兼容大小写列名
def get_value(row, possible_keys):
    for k in possible_keys:
        if k in row: return row[k]
    return ''

def sync():
    cms_data = {"global": {}, "static_pages": {}, "blog": []}
    print("--- 启动同步 ---")

    # 1. Global
    global_rows = fetch_csv_dicts(CONFIG["global"])
    for r in global_rows:
        kid = get_value(r, ['ID', 'id', 'Id'])
        val = get_value(r, ['content', 'Content', 'CONTENT'])
        if kid: cms_data["global"][kid] = val

    # 2. Static Pages
    static_rows = fetch_csv_dicts(CONFIG["static_pages"])
    for r in static_rows:
        hid = get_value(r, ['html_ID', 'html_id', 'HTML_ID'])
        val = get_value(r, ['content', 'Content', 'CONTENT'])
        if hid: cms_data["static_pages"][hid] = val

    # 3. Blog
    cms_data["blog"] = fetch_csv_dicts(CONFIG["blog"])

    os.makedirs('web_v1', exist_ok=True)
    with open('web_v1/data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    
    print("--- 同步成功 ---")

if __name__ == "__main__":
    sync()

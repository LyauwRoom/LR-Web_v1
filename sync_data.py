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
            # 核心修正：只有当 key 不为空且 value 不为 None 时才进行处理
            clean_row = {}
            for k, v in row.items():
                if k is not None:
                    key = str(k).strip()
                    val = str(v).strip() if v is not None else ""
                    clean_row[key] = val
            
            # 如果这一行不是全是空的，就加入结果
            if any(clean_row.values()):
                cleaned_data.append(clean_row)
        return cleaned_data
    except Exception as e:
        print(f"读取 CSV 出错: {e}")
        return []

def sync():
    cms_data = {"global": {}, "static_pages": {}, "blog": []}
    print("--- 启动 v2.0.07 终极防空同步 ---")

    # 1. Global
    global_rows = fetch_csv_dicts(CONFIG["global"])
    for r in global_rows:
        # 兼容匹配 ID 或 key
        kid = r.get('ID') or r.get('id')
        if kid: cms_data["global"][kid] = r.get('content', '')

    # 2. Static Pages (对应你的新标题 html_ID)
    static_rows = fetch_csv_dicts(CONFIG["static_pages"])
    for r in static_rows:
        hid = r.get('html_ID')
        if hid: cms_data["static_pages"][hid] = r.get('content', '')

    # 3. Blog (直接存入)
    cms_data["blog"] = fetch_csv_dicts(CONFIG["blog"])

    # 路径处理
    os.makedirs('web_v1', exist_ok=True)
    target_file = 'web_v1/data.json'
    
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    
    print(f"--- 同步圆满完成！文件位置: {target_file} ---")

if __name__ == "__main__":
    sync()
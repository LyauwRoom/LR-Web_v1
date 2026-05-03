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

def fetch_data(name, url):
    print(f"正在抓取 {name}...")
    try:
        resp = requests.get(url, timeout=10)
        resp.encoding = 'utf-8-sig'
        if resp.status_code != 200:
            print(f"❌ {name} 抓取失败，状态码: {resp.status_code}")
            return []
        
        f = StringIO(resp.text)
        reader = csv.DictReader(f)
        # 统一把标题转成小写，去掉空格和隐藏字符
        data = []
        for row in reader:
            clean_row = {str(k).strip().lower(): str(v).strip() for k, v in row.items() if k}
            data.append(clean_row)
        print(f"✅ {name} 抓取成功，共 {len(data)} 行")
        return data
    except Exception as e:
        print(f"❌ {name} 异常: {e}")
        return []

def sync():
    cms_data = {"global": {}, "static_pages": {}, "blog": []}
    
    # 1. Global
    g_data = fetch_data("Global", CONFIG["global"])
    for row in g_data:
        # 寻找包含 'id' 的键和包含 'content' 的键
        k = row.get('id') or row.get('key')
        v = row.get('content') or row.get('内容')
        if k: cms_data["global"][k] = v

    # 2. Static Pages
    s_data = fetch_data("Static_Pages", CONFIG["static_pages"])
    for row in s_data:
        k = row.get('id')
        v = row.get('content')
        if k: cms_data["static_pages"][k] = v

    # 3. Blog
    cms_data["blog"] = fetch_data("Blog", CONFIG["blog"])

    # 确保保存到 web_v1
    os.makedirs('web_v1', exist_ok=True)
    with open('web_v1/data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    print("--- 任务完成，data.json 已存入 web_v1/ ---")

if __name__ == "__main__":
    sync()
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
        resp = requests.get(url, timeout=10)
        resp.encoding = 'utf-8-sig' # 必须保留，它能解决 Google Sheets 的隐藏乱码
        if resp.status_code != 200: return []
        
        f = StringIO(resp.text)
        reader = csv.DictReader(f)
        
        # 自动清理所有标题两端的空格，防呆设计
        cleaned_data = []
        for row in reader:
            clean_row = {str(k).strip(): str(v).strip() for k, v in row.items() if k}
            cleaned_data.append(clean_row)
        return cleaned_data
    except Exception as e:
        print(f"抓取失败: {e}")
        return []

def sync():
    cms_data = {"global": {}, "static_pages": {}, "blog": []}
    print("--- 启动 v2.0.06 精准匹配版 ---")

    # 1. Global (读取 ID 和 content)
    global_rows = fetch_csv_dicts(CONFIG["global"])
    for r in global_rows:
        if r.get('ID') and r.get('content'):
            cms_data["global"][r['ID']] = r['content']
    print(f"Global 同步完成: {len(cms_data['global'])} 项")

    # 2. Static Pages (精准读取 html_ID 和 content)
    static_rows = fetch_csv_dicts(CONFIG["static_pages"])
    for r in static_rows:
        if r.get('html_ID') and r.get('content'):
            cms_data["static_pages"][r['html_ID']] = r['content']
    print(f"Static_pages 同步完成: {len(cms_data['static_pages'])} 项")

    # 3. Blog (直接整体读取)
    cms_data["blog"] = fetch_csv_dicts(CONFIG["blog"])
    print(f"Blog 同步完成: {len(cms_data['blog'])} 条")

    # 保存文件
    os.makedirs('web_v1', exist_ok=True)
    with open('web_v1/data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    print("--- 同步成功！请检查 web_

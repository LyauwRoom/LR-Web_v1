import requests
import json
import csv
from io import StringIO

CONFIG = {
    "global": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=0&single=true&output=csv",
    "static_pages": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=999625505&single=true&output=csv",
    "blog": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=1581291519&single=true&output=csv",
    "gallery": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=597998095&single=true&output=csv"
}

def fetch_csv_as_dicts(url):
    resp = requests.get(url)
    # 这里的 'utf-8-sig' 是魔法！它能自动过滤掉 Google Sheets 的隐形 BOM 字符
    resp.encoding = 'utf-8-sig'
    f = StringIO(resp.text)
    return list(csv.DictReader(f))

def sync():
    cms_data = {}
    
    print("开始同步数据...")
    
    # 1. 处理 Global
    global_rows = fetch_csv_as_dicts(CONFIG["global"])
    cms_data["global"] = {
        row.get('key (ID)', '').strip(): row.get('content (内容)', '').strip() 
        for row in global_rows if row.get('key (ID)')
    }
    
    # 2. 处理 Static_pages
    static_rows = fetch_csv_as_dicts(CONFIG["static_pages"])
    cms_data["static_pages"] = {
        row.get('id_in_html (HTML ID)', '').strip(): row.get('content (文字内容/图片路径)', '').strip() 
        for row in static_rows if row.get('id_in_html (HTML ID)')
    }
    
    # 3. 处理 Blog & Gallery
    cms_data["blog"] = fetch_csv_as_dicts(CONFIG["blog"])
    cms_data["gallery"] = fetch_csv_as_dicts(CONFIG["gallery"])
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
        
    print("太棒了！所有数据同步成功！")

if __name__ == "__main__":
    sync()
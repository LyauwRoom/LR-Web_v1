import requests
import json
import csv
from io import StringIO

# 你提供的 4 个标签页 CSV 链接
CONFIG = {
    "global": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=0&single=true&output=csv",
    "static_pages": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=999625505&single=true&output=csv",
    "blog": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=1581291519&single=true&output=csv",
    "gallery": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=597998095&single=true&output=csv"
}

def fetch_csv(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    f = StringIO(resp.text)
    return list(csv.DictReader(f))

def sync():
    cms_data = {}
    
    # 1. 处理 Global (转为键值对)
    global_rows = fetch_csv(CONFIG["global"])
    cms_data["global"] = {row['key (ID)']: row['content (内容)'] for row in global_rows if row['key (ID)']}
    
    # 2. 处理 Static Pages (转为键值对)
    static_rows = fetch_csv(CONFIG["static_pages"])
    cms_data["static_pages"] = {row['id_in_html (HTML ID)']: row['content (文字内容/图片路径)'] for row in static_rows if row['id_in_html (HTML ID)']}
    
    # 3. 处理 Blog 和 Gallery (保留列表格式)
    cms_data["blog"] = fetch_csv(CONFIG["blog"])
    cms_data["gallery"] = fetch_csv(CONFIG["gallery"])
    
    # 保存为 data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    
    print("--- 恭喜！云端数据同步成功 ---")

if __name__ == "__main__":
    sync()
  

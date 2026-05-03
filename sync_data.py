import requests
import json
import csv
import os
from io import StringIO

# 你的 CSV 链接保持不变
CONFIG = {
    "global": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=0&single=true&output=csv",
    "static_pages": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=999625505&single=true&output=csv",
    "blog": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=1581291519&single=true&output=csv"
}

def fetch_clean_csv(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8-sig' # 自动处理隐藏字符
    f = StringIO(resp.text)
    # 使用 DictReader 读取，它会自动把第一行作为 Key
    return list(csv.DictReader(f))

def sync():
    cms_data = {}
    print("--- 启动标准化同步 v2.0.02 ---")

    # 1. 处理 Global (id, content)
    global_rows = fetch_clean_csv(CONFIG["global"])
    cms_data["global"] = {row['id'].strip(): row['content'].strip() for row in global_rows if row.get('id')}

    # 2. 处理 Static_pages (id, content)
    static_rows = fetch_clean_csv(CONFIG["static_pages"])
    cms_data["static_pages"] = {row['id'].strip(): row['content'].strip() for row in static_rows if row.get('id')}

    # 3. 处理 Blog (全部保留)
    cms_data["blog"] = fetch_clean_csv(CONFIG["blog"])

    # 确保保存到 web_v1 目录下
    output_path = 'web_v1/data.json'
    
    # 检查文件夹是否存在
    os.makedirs('web_v1', exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    
    print(f"--- 同步完成！数据已存入 {output_path} ---")

if __name__ == "__main__":
    sync()
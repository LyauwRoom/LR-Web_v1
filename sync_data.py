import requests
import json
import csv
from io import StringIO

# 你的 Google Sheets CSV 链接 (保持不变)
CONFIG = {
    "global": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=0&single=true&output=csv",
    "static_pages": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=999625505&single=true&output=csv",
    "blog": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkDFCZA4hODuZPz_owlujHkHizAuSGuTAgRoZkzIkhF_e9PsJRl-2fhtxt96hOnLvjmXNNDCoydQkd/pub?gid=1581291519&single=true&output=csv"
}

def fetch_data(url):
    try:
        resp = requests.get(url)
        # 魔法点：'utf-8-sig' 会自动删除隐藏的 BOM 字符
        resp.encoding = 'utf-8-sig'
        f = StringIO(resp.text)
        reader = csv.DictReader(f)
        
        # 清理列名：去掉每个表头前后的空格，防止匹配失败
        data = []
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
            data.append(clean_row)
        return data
    except Exception as e:
        print(f"抓取失败: {url}, 错误: {e}")
        return []

def sync():
    cms_data = {}
    print("--- 正在启动 v2.0.01 同步程序 ---")

    # 1. 处理 Global (将 key (ID) 转换为 JSON 键值)
    global_raw = fetch_data(CONFIG["global"])
    cms_data["global"] = {}
    for row in global_raw:
        # 兼容匹配：寻找包含 'key' 的列
        key_col = next((k for k in row.keys() if 'key' in k.lower()), None)
        val_col = next((k for k in row.keys() if 'content' in k.lower()), None)
        if key_col and val_col:
            cms_data["global"][row[key_col]] = row[val_col]

    # 2. 处理 Static_pages (将 id_in_html 转换为 JSON 键值)
    static_raw = fetch_data(CONFIG["static_pages"])
    cms_data["static_pages"] = {}
    for row in static_raw:
        key_col = next((k for k in row.keys() if 'id_in_html' in k.lower()), None)
        val_col = next((k for k in row.keys() if 'content' in k.lower()), None)
        if key_col and val_col:
            cms_data["static_pages"][row[key_col]] = row[val_col]

    # 3. 处理 Blog (保持原样，移除 Gallery)
    cms_data["blog"] = fetch_data(CONFIG["blog"])
    
    # 4. 保存文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(cms_data, f, ensure_ascii=False, indent=4)
    
    print("--- 同步成功！已生成 data.json ---")

if __name__ == "__main__":
    sync()
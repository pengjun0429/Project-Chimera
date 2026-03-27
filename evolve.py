import os
import google.generativeai as genai
import re

# 1. 設定 Gemini API KEY
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

# 這裡改用目前最推薦的模型：gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. 讀取目前的 HTML 檔案
HTML_FILE = 'index.html'
try:
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        current_html = f.read()
except FileNotFoundError:
    print(f"Error: {HTML_FILE} not found.")
    exit(1)

# 3. 準備進化的指令
prompt = f"""
你是一個正在進化的網頁生命體。這是你目前的基因程式碼：
---
{current_html}
---
請執行「奇美拉突變」：
1. 視覺進化：隨機加入酷炫的 CSS 效果（如玻璃擬態、3D 旋轉、霓虹閃爍、或是背景漸變動畫）。
2. 功能突變：加入新的互動功能（如點擊特效、自動打字機效果、甚至是個隨機生成迷因的小工具）。
3. 世代紀錄：將網頁中提到的「世代」或「Generation」數字加 1。
4. 格式要求：直接輸出完整的 HTML 代碼，不要包含 Markdown 標記（如 ```html）。
"""

print("正在請求 Gemini 進行進化 (使用 gemini-1.5-flash)...")

# 4. 呼叫 API
try:
    response = model.generate_content(prompt)
    new_html = response.text.strip()
    
    # 清理 Markdown
    new_html = re.sub(r'^```html\s*', '', new_html)
    new_html = re.sub(r'\s*```$', '', new_html)

    # 5. 寫回檔案
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("進化成功！新基因已寫入 index.html。")

except Exception as e:
    print(f"Error: {e}")
    exit(1)

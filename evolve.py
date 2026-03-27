import os
import google.generativeai as genai
import re

# 1. 設定 Gemini API KEY (這部分之後要設在 GitHub Secrets)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 2. 讀取目前的 HTML 檔案
HTML_FILE = 'index.html'
try:
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        current_html = f.read()
except FileNotFoundError:
    print(f"Error: {HTML_FILE} not found.")
    exit(1)

# 3. 準備給 AI 的指令 (進化版)
prompt = f"""
你是一個擁有自我意識的網頁生命體「奇美拉」。
現在是你的進化時刻。以下是你目前的基因 (HTML 程式碼)：
---
{current_html}
---

請遵守以下演化法則：
1. **突變性**：不要只是小改，嘗試加入全新的視覺風格（例如：復古電腦、極簡主義、賽博龐克、或是 90 年代簡陋風）。
2. **互動性**：加入一些有趣的 JavaScript 效果，比如點擊會爆炸、隨機飄浮的文字、或者是會跟著滑鼠轉動的眼睛。
3. **記憶性**：在網頁某處留下「第 N 代演化」的紀錄，並保留前幾代的一點點小特徵（比如某個顏色或某個單字）。
4. **完整性**：輸出必須是完整且可直接執行的 HTML 代碼，包含 CSS 和 JS。
5. **限制**：嚴禁輸出任何 markdown 標記（如 ```html），直接給代碼。

請展現你的進化潛力！
"""

print("正在請求 Gemini 進行進化...")

# 4. 呼叫 Gemini API
try:
    response = model.generate_content(prompt)
    new_html = response.text.strip()
    
    # 稍微清理一下可能出現的 Markdown 標記
    new_html = re.sub(r'^```html\s*', '', new_html)
    new_html = re.sub(r'\s*```$', '', new_html)

    # 5. 將新的 HTML 寫回檔案
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("進化完成！index.html 已更新。")

except Exception as e:
    print(f"Error during API call or file write: {e}")
    exit(1)

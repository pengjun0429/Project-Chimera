import os
from google import genai
import re
import sys

# 1. 設定 API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY，請檢查 GitHub Secrets。")
    sys.exit(1)

# 建立 Client
client = genai.Client(api_key=GOOGLE_API_KEY)

# 2. 讀取目前的 HTML
HTML_FILE = 'index.html'
try:
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        current_html = f.read()
except Exception as e:
    print(f"❌ 讀檔失敗: {e}")
    sys.exit(1)

# 3. 設定進化的指令
prompt = f"""
你是一個網頁進化 AI「奇美拉」。這是你目前的 HTML 基因：
---
{current_html}
---
請執行以下進化指令：
1. 視覺突破：加入炫酷的 CSS 樣式（如動畫、漸層、或特殊的排版）。
2. 功能突變：加入新的 JavaScript 互動功能或小工具。
3. 世代紀錄：尋找網頁中的「世代」或「Generation」數字並將其加 1。
4. 輸出要求：直接輸出完整的 HTML 代碼，嚴禁包含 Markdown 標記（如 ```html）。
"""

try:
    print("🚀 正在請求 Gemini 進行進化 (使用 gemini-1.5-flash)...")
    
    # 使用新版 SDK 的正確語法
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )
    
    if not response.text:
        print("❌ AI 沒有回傳內容。")
        sys.exit(1)

    new_html = response.text.strip()
    
    # 強力清理可能的 Markdown 標記
    new_html = re.sub(r'^```html\s*', '', new_html, flags=re.IGNORECASE)
    new_html = re.sub(r'\s*```$', '', new_html)

    # 4. 寫回檔案
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("✨ 進化完成！新的 HTML 基因已寫入。")

except Exception as e:
    print(f"💥 進化失敗，錯誤訊息: {e}")
    sys.exit(1)

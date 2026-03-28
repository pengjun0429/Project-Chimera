import os
from google import genai
import re
import sys

# 1. 設定 API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY，請檢查 GitHub Secrets。")
    sys.exit(1)

# 建立 Client 並強制指定使用 v1 版本 API，避開 v1beta 的問題
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={'api_version': 'v1'}
)

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
你是一個網頁進化 AI「奇美拉」。請根據以下 HTML 基因進行突變：
---
{current_html}
---
指令：
1. 加入炫酷的 CSS 動畫、漸層或 3D 特效。
2. 加入新的 JS 互動功能。
3. 如果網頁中有「世代」或「Generation」字樣，將其數字加 1。
4. 直接輸出完整的 HTML 原始碼，不要 Markdown 標記。
"""

try:
    print("🚀 正在強制使用 v1 API 請求 Gemini 進化...")
    
    # 使用完整路徑格式的模型名稱
    response = client.models.generate_content(
        model='models/gemini-1.5-flash',
        contents=prompt
    )
    
    if not response or not response.text:
        print("❌ AI 沒有回傳內容。")
        sys.exit(1)

    new_html = response.text.strip()
    
    # 清理 Markdown
    new_html = re.sub(r'^```html\s*', '', new_html, flags=re.IGNORECASE)
    new_html = re.sub(r'\s*```$', '', new_html)

    # 4. 寫回檔案
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("✨ 進化完成！新的基因已成功寫入 index.html。")

except Exception as e:
    print(f"💥 進化失敗，詳細錯誤: {e}")
    sys.exit(1)

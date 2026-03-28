import os
from google import genai
import re
import sys

# 1. 設定 API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY。")
    sys.exit(1)

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
你是一個正在進化的網頁生命體。請針對以下 HTML 進行「2.5 世代」的大膽突變：
---
{current_html}
---
進化需求：
1. 視覺：使用 2026 年流行的設計風格（如動態流體背景、精緻的毛玻璃效果）。
2. 功能：加入一個有意義的互動元件（如情緒切換器、隨機格言產生器、或炫酷的時鐘）。
3. 紀錄：若網頁中有「第 N 代」或「Generation N」，將其數字加 1。
4. 格式：僅輸出完整 HTML，嚴禁包含 ```html 等 Markdown 標籤。
 提示：盡量跟之前的不同,可以全部改掉。
提示：不一定要把第幾代放在標題，可以把它移到別的地方，重點是一定要有
"""

try:
    print("🚀 使用 gemini-2.5-flash 啟動超次元進化...")
    
    # 使用剛才掃描到的精確名稱
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    if not response.text:
        print("❌ AI 沒有回傳基因內容。")
        sys.exit(1)

    new_html = response.text.strip()
    
    # 強力清理 Markdown 殘留
    new_html = re.sub(r'^```html\s*', '', new_html, flags=re.IGNORECASE)
    new_html = re.sub(r'\s*```$', '', new_html)

    # 4. 寫回檔案
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("✨ 進化成功！第 1 代奇美拉已誕生。")

except Exception as e:
    print(f"💥 進化崩潰: {e}")
    sys.exit(1)

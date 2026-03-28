import os
from google import genai
import re
import sys

# 1. 設定 API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY。")
    sys.exit(1)

# 改用全新的 Client 語法
client = genai.Client(api_key=GOOGLE_API_KEY)

# 2. 診斷：列出可用模型 (如果失敗可以看原因)
try:
    print("🔍 正在檢查可用模型...")
    for m in client.models.list():
        if 'generateContent' in m.supported_methods:
            print(f"可用模型: {m.name}")
except Exception as e:
    print(f"❌ 無法列出模型，API Key 可能有問題: {e}")
    sys.exit(1)

# 3. 讀取並進化
HTML_FILE = 'index.html'
try:
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        current_html = f.read()
except Exception as e:
    print(f"❌ 讀檔失敗: {e}")
    sys.exit(1)

prompt = f"你是一個網頁進化 AI。請將以下 HTML 加入炫酷的 CSS 動畫或 JS 功能並回傳完整代碼：\n{current_html}"

try:
    print("🚀 正在嘗試進化...")
    # 使用最新的模型名稱格式
    response = client.models.generate_content(
        model='gemini-1.5-flash', 
        contents=prompt
    )
    
    new_html = response.text.strip()
    new_html = re.sub(r'^```html\s*', '', new_html)
    new_html = re.sub(r'\s*```$', '', new_html)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("✨ 進化完成！基因已更新。")
except Exception as e:
    print(f"💥 進化失敗: {e}")
    sys.exit(1)

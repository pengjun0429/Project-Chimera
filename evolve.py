import os
import google.generativeai as genai
import re
import sys

# 1. 設定 API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY。")
    sys.exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

# 2. 自動嘗試不同的模型名稱格式 (解決 404 問題)
model_names = [
    'gemini-1.5-flash',
    'models/gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'models/gemini-pro'
]

model = None
for name in model_names:
    try:
        print(f"正在嘗試模型: {name}...")
        test_model = genai.GenerativeModel(name)
        # 進行一個超微型測試，確認模型是否可用
        test_model.generate_content("Hi", generation_config={"max_output_tokens": 1})
        model = test_model
        print(f"✅ 成功連線至模型: {name}")
        break
    except Exception as e:
        print(f"⚠️ 模型 {name} 無法使用: {e}")

if not model:
    print("❌ 錯誤：所有模型嘗試都失敗了。請檢查 API Key 是否正確。")
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
    response = model.generate_content(prompt)
    new_html = response.text.strip()
    new_html = re.sub(r'^```html\s*', '', new_html)
    new_html = re.sub(r'\s*```$', '', new_html)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("✨ 進化完成！基因已更新。")
except Exception as e:
    print(f"💥 進化過程發生錯誤: {e}")
    sys.exit(1)

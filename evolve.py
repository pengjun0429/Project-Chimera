import os
from google import genai
import sys

# 1. 設定 API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY。")
    sys.exit(1)

client = genai.Client(api_key=GOOGLE_API_KEY)

print("🔍 正在掃描你的 API Key 可用的模型清單...")

try:
    # 這裡直接呼叫清單功能
    models_found = []
    for m in client.models.list():
        # 檢查是否支援生成內容
        if 'generateContent' in m.supported_methods:
            models_found.append(m.name)
            print(f"✅ 發現可用模型: {m.name}")

    if not models_found:
        print("⚠️ 警告：這組 API Key 找不到任何可用的生成模型。")
        print("請檢查：1. API Key 是否複製完整 2. 是否在 Google AI Studio 啟用了 Gemini API。")
    else:
        print("\n💡 診斷建議：")
        print(f"請在 evolve.py 中將 model 設定為上面清單中的其中一個（例如 '{models_found[0]}'）。")

except Exception as e:
    print(f"💥 偵察失敗，詳細錯誤: {e}")
    sys.exit(1)

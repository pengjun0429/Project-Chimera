import os
from google import genai
import sys

# 1. 設定 API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY。")
    sys.exit(1)

client = genai.Client(api_key=GOOGLE_API_KEY)

print("🔍 正在嘗試列出所有模型資訊...")

try:
    # 獲取模型清單
    models = list(client.models.list())
    
    if not models:
        print("⚠️ 警告：這組 API Key 沒看到任何模型。")
    else:
        print(f"✅ 成功找到 {len(models)} 個模型！")
        for i, m in enumerate(models):
            # 印出模型名稱和它擁有的屬性，讓我們檢查
            print(f"--- 模型 {i+1} ---")
            print(f"名稱 (Name): {m.name}")
            # 如果是第一筆，印出它的所有欄位名稱供偵錯
            if i == 0:
                print(f"可用欄位: {dir(m)}")
                
except Exception as e:
    print(f"💥 診斷再次失敗，詳細錯誤: {e}")
    sys.exit(1)

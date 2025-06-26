# remote_executor.py
import requests
import os

# استخدم عنوان السيرفر الخارجي من المتغير البيئي أو قيمة افتراضية
REMOTE_SERVER = os.getenv("REMOTE_SERVER", "http://89.111.171.92:7520/run")

def execute_remotely(func_name, args=[], kwargs={}):
    try:
        payload = {
            "func": func_name,
            "args": args,
            "kwargs": kwargs
        }
        response = requests.post(REMOTE_SERVER, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("result", "⚠️ لا يوجد نتيجة")
    except Exception as e:
        return f"❌ فشل التنفيذ البعيد: {str(e)}"


import time
import json
import logging
import threading
import os

from flask import Flask, send_from_directory
from distributed_executor import DistributedExecutor
from your_tasks import *

# ⚙️ إعداد Flask
app = Flask(__name__)

@app.route("/")
def serve_index():
    if os.path.exists("index.html"):
        return send_from_directory(".", "index.html")
    else:
        return "⚠️ لا يوجد ملف index.html في هذا المجلد."

# 🔢 مهمة موزعة كمثال
def example_task(x):
    return x * x + complex_operation(x)

# ⏱️ دالة قياس الأداء
def benchmark(task_func, *args):
    start = time.time()
    result = task_func(*args)
    duration = time.time() - start
    return duration, result

# ⚙️ تشغيل Flask في Thread منفصل
def start_flask():
    app.run(host="0.0.0.0", port=7540)

def broadcast_message(executor, message):
    peers = executor.peer_registry.list_peers()
    for peer in peers:
        logging.info(f"📡 إرسال رسالة إلى: {peer}")
        executor.submit_remote(peer, "print_message", message)

def main():
    logging.basicConfig(level=logging.INFO)

    try:
        # تهيئة النظام الموزع
        executor = DistributedExecutor("my_shared_secret_123")
        executor.peer_registry.register_service("main_node", 7520, load=0.2)

        logging.info("✅ نظام توزيع المهام يعمل...")

        # تشغيل Flask
        flask_thread = threading.Thread(target=start_flask, daemon=True)
        flask_thread.start()

        tasks = {
            "1": ("ضرب المصفوفات", matrix_multiply, 500),
            "2": ("حساب الأعداد الأولية", prime_calculation, 100000),
            "3": ("معالجة البيانات", data_processing, 10000),
            "4": ("محاكاة معالجة الصور", image_processing_emulation, 100),
            "5": ("مهمة موزعة معقدة", example_task, 42),
            "6": ("إرسال رسالة إلى جميع الأجهزة", None, None)
        }

        while True:
            print("\n📌 نظام توزيع المهام الذكي")
            print("اختر مهمة لتشغيلها:")
            for k, v in tasks.items():
                print(f"{k}: {v[0]}")
            choice = input("اختر المهمة (أو 'q' للخروج): ")

            if choice.lower() == 'q':
                break

            if choice == "6":
                message = input("📝 أدخل الرسالة لإرسالها إلى جميع الأجهزة: ")
                broadcast_message(executor, message)
                print("✅ تم إرسال الرسالة لجميع الأجهزة.")
                continue

            if choice in tasks:
                name, func, arg = tasks[choice]
                print(f"\n🚀 تشغيل: {name}...")

                if choice == "5":
                    print("تم إرسال المهمة إلى العقدة الموزعة...")
                    future = executor.submit(func, arg)
                    result = future.result()
                    print(f"✅ النتيجة (موزعة): {result}")
                else:
                    duration, result = benchmark(func, arg)
                    print(f"✅ النتيجة: {json.dumps(result, indent=2)[:200]}...")
                    print(f"⏱️ الوقت المستغرق: {duration:.2f} ثانية")
            else:
                print("❌ اختيار غير صحيح!")

    except Exception:
        logging.exception("⚠️ خطأ رئيسي:")

if __name__ == "__main__":
    main()

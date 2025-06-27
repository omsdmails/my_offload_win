# main.py

from flask import Flask, send_from_directory
import threading
import time
import json
import logging
from distributed_executor import DistributedExecutor
from your_tasks import *  # تأكد أن المهام معرفة هنا

# إعداد Flask
app = Flask(__name__)

@app.route("/")
def serve_index():
    return send_from_directory('.', 'index.html')

def run_flask():
    app.run(host='0.0.0.0', port=8000)

# منطق التوزيع
def distributed_logic():
    logging.basicConfig(level=logging.INFO)
    executor = DistributedExecutor("my_shared_secret_123")
    executor.peer_registry.register_service("node1", 7520, load=0.2)
    logging.info("🚀 نظام توزيع المهام يعمل...")

    tasks = {
        "1": ("ضرب المصفوفات", matrix_multiply, 500),
        "2": ("حساب الأعداد الأولية", prime_calculation, 100000),
        "3": ("معالجة البيانات", data_processing, 10000),
        "4": ("محاكاة معالجة الصور", image_processing_emulation, 100),
        "5": ("مهمة موزعة معقدة", example_task, 42)
    }

    while True:
        print("\n🚦 نظام توزيع المهام الذكي")
        print("اختر مهمة لتشغيلها:")
        for k, v in tasks.items():
            print(f"{k}: {v[0]}")
        choice = input("اختر المهمة (أو 'q' للخروج): ")

        if choice.lower() == 'q':
            break

        if choice in tasks:
            name, func, arg = tasks[choice]
            print(f"\nتشغيل: {name}...")

            if choice == "5":
                print("تم إرسال المهمة إلى العقدة الموزعة...")
                future = executor.submit(func, arg)
                result = future.result()
                print(f"💡 النتيجة (موزعة): {result}")
            else:
                duration, result = benchmark(func, arg)
                print(f"💡 النتيجة: {json.dumps(result, indent=2)[:200]}...")
                print(f"⏱️ الوقت المستغرق: {duration:.2f} ثانية")
        else:
            print("🚫 اختيار غير صحيح!")

# دالة قياس الأداء
def benchmark(task_func, *args):
    start = time.time()
    result = task_func(*args)
    duration = time.time() - start
    return duration, result

# دالة مهمة معقدة
def example_task(x):
    return x * x + complex_operation(x)

# تشغيل الكل
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    distributed_logic()

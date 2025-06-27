# main.py

import time
import json
from distributed_executor import DistributedExecutor
from your_tasks import *
# main.py
from distributed_executor import DistributedExecutor
import logging

from flask import Flask
from distributed_executor import DistributedExecutor

app = Flask(__name__)
executor = DistributedExecutor("my_shared_secret_123")

@app.route("/")
def index():
    return "نظام توزيع المهام جاهز للعمل!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

def main():
    logging.basicConfig(level=logging.INFO)
    
    try:
        # تهيئة النظام
        executor = DistributedExecutor("my_shared_secret_123")
        executor.peer_registry.register_service("main_node", 7520)
        
        logging.info("نظام توزيع المهام يعمل...")
        
        # يمكنك هنا إضافة مهام للتنفيذ
        while True:
            time.sleep(1)
            
    except Exception as e:
        logging.error(f"خطأ رئيسي: {str(e)}")

if __name__ == "__main__":
    main()
def example_task(x):
    # مهمة معقدة قابلة للتوزيع
    return x * x + complex_operation(x)

def benchmark(task_func, *args):
    """قياس أداء المهمة"""
    start = time.time()
    result = task_func(*args)
    duration = time.time() - start
    return duration, result

def main():
    executor = DistributedExecutor("my_shared_secret_123")
    executor.peer_registry.register_service("node1", 7520, load=0.2)

    tasks = {
        "1": ("ضرب المصفوفات", matrix_multiply, 500),
        "2": ("حساب الأعداد الأولية", prime_calculation, 100000),
        "3": ("معالجة البيانات", data_processing, 10000),
        "4": ("محاكاة معالجة الصور", image_processing_emulation, 100),
        "5": ("مهمة موزعة معقدة", example_task, 42)
    }

    while True:
        print("\nنظام توزيع المهام الذكي")
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
                print(f"النتيجة (موزعة): {result}")
            else:
                duration, result = benchmark(func, arg)
                print(f"النتيجة: {json.dumps(result, indent=2)[:200]}...")
                print(f"الوقت المستغرق: {duration:.2f} ثانية")
        else:
            print("اختيار غير صحيح!")

if __name__ == "__main__":
    main()


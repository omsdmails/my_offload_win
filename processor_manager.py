# processor_manager.py
import psutil
from collections import deque

cpu_load = psutil.cpu_percent(interval=1)  # نسبة استخدام CPU خلال ثانية
mem_available = psutil.virtual_memory().available / (1024**2)  # الذاكرة المتاحة بالميجابايت

if cpu_load > 70 or mem_available < 500:  # إذا تجاوز CPU 70% أو الذاكرة أقل من 500MB
    trigger_offload()  # تشغيل عملية التوزيع

class ResourceMonitor:
    def __init__(self):
        self.cpu_history = deque(maxlen=10)
        self.mem_history = deque(maxlen=10)

    def current_load(self):
        # قياس الحمل الحالي
        cpu = psutil.cpu_percent(interval=0.5) / 100.0
        mem = psutil.virtual_memory().available / (1024**2)

        # حفظ في التاريخ
        self.cpu_history.append(cpu)
        self.mem_history.append(mem)

        # حساب المتوسطات
        avg_cpu = sum(self.cpu_history) / len(self.cpu_history)
        avg_mem = sum(self.mem_history) / len(self.mem_history)

        return {
            "instant": {"cpu": cpu, "mem": mem},
            "average": {"cpu": avg_cpu, "mem": avg_mem},
            "recommendation": "offload" if avg_cpu > 0.7 or avg_mem < 500 else "local"
        }

def should_offload(task_complexity=0):
    monitor = ResourceMonitor()
    status = monitor.current_load()

    # قرار التوزيع يعتمد على:
    if (
        status['average']['cpu'] > 0.6 or
        status['average']['mem'] < 500 or
        task_complexity > 75
    ):
        return True
    return False


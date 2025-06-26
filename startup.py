from autostart_config import AutoStartManager
from distributed_executor import DistributedExecutor
import logging
import sys

def main():
    # إعداد السجل
    logging.basicConfig(
        filename='autostart.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        # تحميل الإعدادات
        autostart = AutoStartManager()
        if not autostart.config['enabled']:
            logging.info("التشغيل التلقائي معطل في الإعدادات")
            return
        
        # بدء النظام الرئيسي
        logging.info("بدء تشغيل النظام الموزع تلقائياً")
        executor = DistributedExecutor("my_shared_secret_123")
        executor.peer_registry.register_service("auto_node", 7520)
        
        # هنا يمكنك إضافة أي مهام تريد تشغيلها تلقائياً
        # executor.submit(...)
        
        # البقاء نشطاً
        while True:
            time.sleep(60)
            
    except Exception as e:
        logging.error(f"خطأ في التشغيل التلقائي: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

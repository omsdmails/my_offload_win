# distributed_executor.py
import threading
import queue
import time
import json
from typing import Callable, Dict, List
import socket
from zeroconf import Zeroconf, ServiceBrowser, ServiceInfo
import logging

class PeerRegistry:
    def __init__(self):
        self._peers = {}
        self._zeroconf = Zeroconf()
        self.local_node_id = socket.gethostname()
    
    def register_service(self, name: str, port: int, load: float = 0.0):
        service_info = ServiceInfo(
            "_tasknode._tcp.local.",
            f"{name}._tasknode._tcp.local.",
            addresses=[socket.inet_aton(self._get_local_ip())],
            port=port,
            properties={'load': str(load), 'node_id': self.local_node_id},
            server=f"{name}.local."
        )
        self._zeroconf.register_service(service_info)
    
    def discover_peers(self, timeout: int = 3) -> List[Dict]:
        class Listener:
            def __init__(self):
                self.peers = []
            
            def add_service(self, zc, type_, name):
                info = zc.get_service_info(type_, name)
                if info:
                    ip = socket.inet_ntoa(info.addresses[0])
                    self.peers.append({
                        'ip': ip,
                        'port': info.port,
                        'load': float(info.properties[b'load']),
                        'node_id': info.properties[b'node_id'].decode(),
                        'last_seen': time.time()
                    })
        
        listener = Listener()
        browser = ServiceBrowser(self._zeroconf, "_tasknode._tcp.local.", listener)
        time.sleep(timeout)
        return sorted(listener.peers, key=lambda x: x['load'])
    
    def _get_local_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

class DistributedExecutor:
    def __init__(self, shared_secret: str):
        self.peer_registry = PeerRegistry()
        self.shared_secret = shared_secret
        self.task_queue = queue.PriorityQueue()
        self.result_cache = {}
        self._init_peer_discovery()
        logging.basicConfig(level=logging.INFO)
    
    def _init_peer_discovery(self):
        def discovery_loop():
            while True:
                self.available_peers = self.peer_registry.discover_peers()
                time.sleep(10)
        
        threading.Thread(target=discovery_loop, daemon=True).start()
    
    def submit(self, task_func: Callable, *args, **kwargs):
        """إرسال مهمة جديدة للنظام"""
        task_id = f"{task_func.__name__}_{time.time()}"
        
        # تجهيز المهمة
        task = {
            'task_id': task_id,
            'function': task_func.__name__,
            'args': args,
            'kwargs': kwargs,
            'sender_id': self.peer_registry.local_node_id
        }
        
        # إرسال المهمة (تبسيط الإرسال في هذا المثال)
        if self.available_peers:
            peer = min(self.available_peers, key=lambda x: x['load'])
            self._send_to_peer(peer, task)
        else:
            logging.warning("لا توجد أجهزة متاحة - سيتم تنفيذ المهمة محلياً")
    
    def _send_to_peer(self, peer: Dict, task: Dict):
        """إرسال مهمة إلى جهاز آخر"""
        try:
            url = f"http://{peer['ip']}:{peer['port']}/run"
            response = requests.post(
                url,
                json=task,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"فشل إرسال المهمة لـ {peer['node_id']}: {str(e)}")
            return None

# نموذج استخدام مبسط
if __name__ == "__main__":
    executor = DistributedExecutor("my_secret_key")
    executor.peer_registry.register_service("node1", 7520, load=0.1)
    print("نظام توزيع المهام جاهز...")

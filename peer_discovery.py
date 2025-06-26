# peer_discovery.py
from zeroconf import Zeroconf, ServiceBrowser, ServiceInfo
import socket
import json
from typing import Dict, List
import time

class PeerRegistry:
    def __init__(self):
        self._peers: Dict[str, Dict] = {}
        self._zeroconf = Zeroconf()
    
    def register_service(self, name: str, port: int, load: float = 0.0):
        service_info = ServiceInfo(
            "_tasknode._tcp.local.",
            f"{name}._tasknode._tcp.local.",
            addresses=[socket.inet_aton(self._get_local_ip())],
            port=port,
            properties={'load': str(load)},
            server=f"{name}.local."
        )
        self._zeroconf.register_service(service_info)
    
    def discover_peers(self, timeout: int = 3) -> List[Dict]:
        browser = ServiceBrowser(self._zeroconf, "_tasknode._tcp.local.", self)
        time.sleep(timeout)
        return sorted(self._peers.values(), key=lambda x: x['load'])
    
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            ip = socket.inet_ntoa(info.addresses[0])
            self._peers[name] = {
                'ip': ip,
                'port': info.port,
                'load': float(info.properties[b'load']),
                'last_seen': time.time()
            }
    
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

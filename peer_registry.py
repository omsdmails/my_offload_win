# peer_registry.py
import socket
import time
from zeroconf import Zeroconf, ServiceBrowser

class Listener:
    def __init__(self):
        self.peers = []

    def add_service(self, zc, type, name):
        info = zc.get_service_info(type, name)
        if info:
            ip = socket.inet_ntoa(info.addresses[0])
            port = info.port
            self.peers.append(f"{ip}:{port}")

def discover_peers(timeout=2):
    zc = Zeroconf()
    listener = Listener()
    ServiceBrowser(zc, "_http._tcp.local.", listener)
    time.sleep(timeout)
    zc.close()
    return listener.peers

# استخدام Zeroconf لاكتشاف الأقران
zeroconf = Zeroconf()
listener = Listener()
browser = ServiceBrowser(zeroconf, "_taskdist._tcp.local.", listener)
time.sleep(2)  # انتظار لاكتشاف الأقران
available_peers = listener.peers  # ["192.168.1.2:7520", "10.0.0.5:7520"]


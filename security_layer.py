# security_layer.py
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import os
import base64

class SecurityManager:
    def __init__(self, shared_secret: str):
        self._key = self._derive_key(shared_secret)
        self._cipher = Fernet(self._key)
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self._peer_keys = {}
    
    def encrypt_data(self, data: bytes) -> bytes:
        """تشفير البيانات بالمفتاح المتماثل"""
        return self._cipher.encrypt(data)
    
    def decrypt_data(self, encrypted: bytes) -> bytes:
        """فك تشفير البيانات"""
        return self._cipher.decrypt(encrypted)
    
    def sign_task(self, task: Dict) -> Dict:
        """توقيع المهمة رقميًا"""
        signature = self._private_key.sign(
            json.dumps(task).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return {**task, '_signature': base64.b64encode(signature).decode()}
    
    def verify_task(self, signed_task: Dict) -> bool:
        """التحقق من صحة التوقيع"""
        if '_signature' not in signed_task:
            return False
        
        signature = base64.b64decode(signed_task['_signature'])
        task_copy = {k: v for k, v in signed_task.items() if k != '_signature'}
        
        try:
            self._peer_keys[signed_task['sender_id']].verify(
                signature,
                json.dumps(task_copy).encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False
    
    def _derive_key(self, password: str) -> bytes:
        """اشتقاق مفتاح تشفير من كلمة المرور"""
        salt = b'salt_placeholder'  # يجب تغييره في الإنتاج
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

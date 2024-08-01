import hashlib
import hmac
from datetime import datetime

from rabbitx.util import hex2bytes

PAYLOAD_KEY_METHOD = 'method'
PAYLOAD_KEY_PATH = 'path'

REQUIRED_KEYS = [PAYLOAD_KEY_METHOD, PAYLOAD_KEY_PATH]


class Payload:

    timestamp: int
    data: dict[str, str]

    def __init__(self, timestamp: int, data: dict[str, str]):
        self.timestamp = timestamp
        self.data = data

        for k in REQUIRED_KEYS:
            if k in data:
                continue

            raise KeyError

    @property
    def hash_old(self) -> bytes:
        keys = list(self.data.keys())
        keys.sort()
        message = [f'{k}={str(self.data[k]).lower()}' if type(self.data[k]) == bool else f'{k}={self.data[k]}' for k in keys]
        message.append(str(self.timestamp))
        message = ''.join(message)

        h = hashlib.sha256()
        h.update(message.encode())

        return h.digest()
    
    @property
    def hash(self) -> bytes:
        keys = sorted(self.data.keys())
        message_parts = []
        
        for key in keys:
            value = self.data[key]
            if isinstance(value, bool):
                value_str = str(value).lower()
            elif isinstance(value, list):
                value_str = str(value)  # Convert list to string
                value_str = value_str.replace('\'', '"')  # Convert single quotes to double quotes
            else:
                value_str = str(value)
            message_parts.append(f'{key}={value_str}')
        
        message_parts.append(str(self.timestamp))
        message = ''.join(message_parts)
        
        h = hashlib.sha256()
        h.update(message.encode('utf-8'))
        
        return h.digest()

    def sign(self, secret: str) -> str:
        secret_bytes = hex2bytes(secret)

        return '0x' + hmac.new(secret_bytes, self.hash, hashlib.sha256).hexdigest()

    def verify(self, signature: str, secret: str) -> bool:
        expected_signature = self.sign(secret)

        if expected_signature != signature:
            return False

        current_timestamp = int(datetime.now().timestamp())

        if current_timestamp >= self.timestamp:
            return False

        return True

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Vault:
    def __init__(self, key: str = None):
        # In production, key should come from a secure KMS or Env Var
        self.key = key or os.environ.get("OPAQUE_MASTER_KEY")
        if not self.key:
            # Fallback for demo/dev if no key provided (NOT SECURE for prod)
            # We generate a temporary key but warn
            self.fernet = None
        else:
            self._setup_fernet(self.key)

    def _setup_fernet(self, key_str: str):
        # Derive a 32-byte URL-safe base64-encoded key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'opaque_static_salt', # In real vault, salt should be managed
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key_str.encode()))
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        if not self.fernet:
            return "[VAULT-NO-KEY-CONFIGURED]"
        
        encrypted = self.fernet.encrypt(data.encode())
        # Return a short snippet + full payload? 
        # For logs, we want something identifiable but maybe not the HUGE string if possible.
        # But to be reversible, we need the full string.
        # We format it as [VAULT:<b64_data>]
        return f"[VAULT:{encrypted.decode()}]"

    def decrypt(self, token: str) -> str:
        if not self.fernet:
            raise ValueError("No Master Key configured.")
        
        # Strip prefix/suffix if present
        if token.startswith("[VAULT:") and token.endswith("]"):
            token = token[7:-1]
            
        try:
            decrypted = self.fernet.decrypt(token.encode())
            return decrypted.decode()
        except Exception as e:
            return f"Error decrypting: {str(e)}"

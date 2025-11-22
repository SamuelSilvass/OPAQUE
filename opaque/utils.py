import hashlib
import os

class Fingerprinter:
    def __init__(self, salt: str = None):
        self.salt = salt or os.environ.get("OPAQUE_SALT", "default_insecure_salt_change_me")
    
    def hash(self, data: str) -> str:
        """
        Creates a deterministic hash of the data + salt.
        Returns a short hash (first 8 chars) for readability in logs, 
        or full hash if needed.
        """
        combined = f"{data}{self.salt}".encode('utf-8')
        full_hash = hashlib.sha256(combined).hexdigest()
        # Returning a short version like [HASH-XF92] as per example
        short_hash = full_hash[:4].upper()
        return f"[HASH-{short_hash}]"

"""
Advanced Examples: Custom Callbacks for Enterprise Deployments

This demonstrates how to inject custom implementations for:
- Hash functions
- Vault/tokenization systems
- Honeytoken handlers
- Anonymization strategies

These examples address the Reddit feedback about needing customizable
implementations for large-scale deployments (50M+ users).
"""

import logging
from opaque import OpaqueLogger, Validators
from opaque.callbacks import (
    VaultInterface, HoneytokenHandler, AnonymizationStrategy,
    DeterministicPseudonymizer, IrreversibleAnonymizer
)


# Example 1: Custom Hash Function with HMAC-SHA512
def custom_hash_function(data: str) -> str:
    """
    Custom hash using HMAC-SHA512 instead of SHA256.
    
    This allows you to use your own hashing algorithm that meets
    your specific compliance requirements.
    """
    import hmac
    import hashlib
    import os
    
    secret = os.environ.get("MY_SECRET_KEY", "change_me")
    h = hmac.new(secret.encode(), data.encode(), hashlib.sha512)
    return f"[CUSTOM-{h.hexdigest()[:12].upper()}]"


# Example 2: External Tokenization Service
class ExternalTokenizationVault(VaultInterface):
    """
    Integration with an external tokenization service.
    
    This could be:
    - HashiCorp Vault
    - AWS Secrets Manager
    - Azure Key Vault
    - Your own tokenization API
    """
    
    def __init__(self, api_endpoint: str, api_key: str):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        # In real implementation, initialize your API client here
        self.token_cache = {}  # Simple cache for demo
    
    def encrypt(self, data: str) -> str:
        """
        Send data to external tokenization service.
        """
        # In real implementation:
        # response = requests.post(
        #     f"{self.api_endpoint}/tokenize",
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        #     json={"data": data}
        # )
        # token = response.json()["token"]
        
        # For demo, use a simple hash
        import hashlib
        token = hashlib.sha256(data.encode()).hexdigest()[:16]
        self.token_cache[token] = data  # Store for decryption
        return f"[TOKEN:{token}]"
    
    def decrypt(self, encrypted: str) -> str:
        """
        Retrieve original data from tokenization service.
        """
        token = encrypted.replace("[TOKEN:", "").replace("]", "")
        
        # In real implementation:
        # response = requests.post(
        #     f"{self.api_endpoint}/detokenize",
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        #     json={"token": token}
        # )
        # return response.json()["data"]
        
        return self.token_cache.get(token, "[UNKNOWN]")


# Example 3: Database-Backed Honeytoken Handler
class DatabaseHoneytokenHandler(HoneytokenHandler):
    """
    Honeytoken handler that checks against a database.
    
    For 50M+ users, you'd use:
    - Redis for fast lookups
    - PostgreSQL with indexes
    - Elasticsearch for pattern matching
    """
    
    def __init__(self, db_connection, siem_webhook: str = None):
        self.db = db_connection
        self.siem_webhook = siem_webhook
        # In real implementation, this would be a Redis client or similar
        self.honeytokens_cache = set()  # Cache for performance
    
    def is_honeytoken(self, data: str) -> bool:
        """
        Check if data is a honeytoken using database lookup.
        """
        # Check cache first (fast path)
        if data in self.honeytokens_cache:
            return True
        
        # In real implementation:
        # result = self.db.execute(
        #     "SELECT 1 FROM honeytokens WHERE value = ? LIMIT 1",
        #     (data,)
        # )
        # if result:
        #     self.honeytokens_cache.add(data)
        #     return True
        
        # For demo, check against a hardcoded list
        demo_honeytokens = {"999.888.777-66", "000.000.000-00"}
        if data in demo_honeytokens:
            self.honeytokens_cache.add(data)
            return True
        
        return False
    
    def on_detected(self, data: str, context: dict = None):
        """
        Alert SIEM when honeytoken is detected.
        """
        import sys
        import json
        from datetime import datetime
        
        alert = {
            "severity": "CRITICAL",
            "type": "HONEYTOKEN_ACCESS",
            "honeytoken": data,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {}
        }
        
        # Print to stderr
        print(f"🚨 CRITICAL ALERT: Honeytoken accessed: {data}", file=sys.stderr)
        
        # In real implementation, send to SIEM:
        # if self.siem_webhook:
        #     requests.post(self.siem_webhook, json=alert)
        
        # Log to security log
        logging.getLogger("opaque.security").critical(
            f"HONEYTOKEN_DETECTED: {json.dumps(alert)}"
        )


# Example 4: LGPD/GDPR Compliant Anonymization
class LGPDCompliantAnonymizer(AnonymizationStrategy):
    """
    True anonymization for LGPD/GDPR compliance.
    
    This uses random UUIDs, ensuring that:
    - Data cannot be reversed
    - Same input produces different outputs
    - No correlation is possible
    - Meets "right to be forgotten" requirements
    
    WARNING: You cannot correlate logs with this method.
    Use only when compliance requires true anonymization.
    """
    
    def anonymize(self, data: str, data_type: str) -> str:
        import uuid
        # Each call generates a new random UUID
        random_id = uuid.uuid4().hex[:12].upper()
        return f"[ANON-{data_type[:3].upper()}-{random_id}]"
    
    def can_reverse(self) -> bool:
        return False


# Example 5: Format-Preserving Encryption
class FormatPreservingVault(VaultInterface):
    """
    Format-preserving encryption (FPE) for specific use cases.
    
    This maintains the format of the original data:
    - CPF 123.456.789-00 -> CPF 987.654.321-99
    - Useful when downstream systems expect specific formats
    
    Note: Requires specialized FPE libraries like pyffx or ff3
    """
    
    def __init__(self, key: str):
        self.key = key
        # In real implementation, initialize FPE cipher here
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt while preserving format.
        """
        # In real implementation, use FPE library:
        # from ff3 import FF3Cipher
        # cipher = FF3Cipher(self.key, tweak)
        # encrypted = cipher.encrypt(data)
        
        # For demo, just reverse the digits
        import re
        digits = re.sub(r'\D', '', data)
        encrypted_digits = digits[::-1]
        
        # Reconstruct with original format
        result = data
        for original, encrypted in zip(digits, encrypted_digits):
            result = result.replace(original, encrypted, 1)
        
        return result
    
    def decrypt(self, encrypted: str) -> str:
        """
        Decrypt FPE data.
        """
        # Same as encrypt for this demo (reversing is symmetric)
        return self.encrypt(encrypted)


# Usage Examples

def example_custom_hash():
    """Example: Using a custom hash function"""
    print("\n=== Example 1: Custom Hash Function ===")
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="HASH",
        hash_function=custom_hash_function
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("custom_hash_demo")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    
    logger.info("User CPF: 529.982.247-25")
    print("✅ CPF masked with custom HMAC-SHA512 hash\n")


def example_external_vault():
    """Example: Using external tokenization service"""
    print("\n=== Example 2: External Tokenization ===")
    
    vault = ExternalTokenizationVault(
        api_endpoint="https://tokenization.example.com",
        api_key="your-api-key"
    )
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="VAULT",
        vault_implementation=vault
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("vault_demo")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    
    logger.info("Processing CPF: 529.982.247-25")
    print("✅ CPF tokenized using external service\n")


def example_database_honeytokens():
    """Example: Database-backed honeytoken detection"""
    print("\n=== Example 3: Database Honeytokens ===")
    
    # Simulate database connection
    db_connection = None  # In real app: psycopg2.connect(...)
    
    honeytoken_handler = DatabaseHoneytokenHandler(
        db_connection=db_connection,
        siem_webhook="https://siem.example.com/alerts"
    )
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        honeytoken_handler=honeytoken_handler
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("honeytoken_demo")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    
    logger.info("Access attempt with CPF: 999.888.777-66")
    print("✅ Honeytoken detected and SIEM alerted\n")


def example_lgpd_compliance():
    """Example: LGPD/GDPR compliant anonymization"""
    print("\n=== Example 4: LGPD/GDPR Compliance ===")
    
    anonymizer = LGPDCompliantAnonymizer()
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="ANONYMIZE",
        anonymization_strategy=anonymizer
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("lgpd_demo")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    
    # Same CPF will produce different outputs each time
    logger.info("User 1 CPF: 529.982.247-25")
    logger.info("User 2 CPF: 529.982.247-25")  # Different output!
    print("✅ True anonymization - cannot correlate or reverse\n")


def example_format_preserving():
    """Example: Format-preserving encryption"""
    print("\n=== Example 5: Format-Preserving Encryption ===")
    
    fpe_vault = FormatPreservingVault(key="your-fpe-key")
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="VAULT",
        vault_implementation=fpe_vault
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("fpe_demo")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    
    logger.info("CPF: 529.982.247-25")
    print("✅ CPF encrypted while maintaining format\n")


if __name__ == "__main__":
    print("=" * 60)
    print("OPAQUE: Advanced Custom Callbacks Examples")
    print("Addressing Reddit Feedback for Enterprise Deployments")
    print("=" * 60)
    
    example_custom_hash()
    example_external_vault()
    example_database_honeytokens()
    example_lgpd_compliance()
    example_format_preserving()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)

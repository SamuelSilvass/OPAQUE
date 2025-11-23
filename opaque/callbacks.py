"""
Custom Callback System for OPAQUE

This module provides interfaces for injecting custom implementations of:
- Hash functions (for custom anonymization strategies)
- Vault implementations (for custom encryption/tokenization)
- Honeytoken handlers (for custom intrusion detection)

This addresses the need for enterprise-scale customization where
different organizations may have specific compliance requirements.
"""

from typing import Protocol, Callable, Optional, Any
from abc import ABC, abstractmethod


class HashFunction(Protocol):
    """
    Protocol for custom hash functions.
    
    Users can inject their own hash implementation to meet specific
    compliance requirements (LGPD, GDPR, etc.)
    
    Example:
        def my_custom_hash(data: str) -> str:
            # Your custom hashing logic
            # Could use HMAC, custom salt rotation, etc.
            return f"[CUSTOM-{hash(data)}]"
        
        OpaqueLogger.setup_defaults(
            rules=[...],
            hash_function=my_custom_hash
        )
    """
    def __call__(self, data: str) -> str:
        """
        Hash the input data and return a string representation.
        
        Args:
            data: The sensitive data to hash
            
        Returns:
            A string representation of the hash (e.g., "[HASH-ABC123]")
        """
        ...


class VaultInterface(ABC):
    """
    Abstract interface for custom vault implementations.
    
    This allows users to inject their own encryption/tokenization
    systems instead of using the built-in AES-256 vault.
    
    Use cases:
    - Integration with existing tokenization services
    - Custom key management systems (HSM, KMS, etc.)
    - Format-preserving encryption
    - External vault services (HashiCorp Vault, AWS Secrets Manager, etc.)
    
    Example:
        class MyVault(VaultInterface):
            def encrypt(self, data: str) -> str:
                # Call your tokenization service
                token = my_service.tokenize(data)
                return f"[TOKEN:{token}]"
            
            def decrypt(self, encrypted: str) -> str:
                # Detokenize
                token = encrypted.replace("[TOKEN:", "").replace("]", "")
                return my_service.detokenize(token)
    """
    
    @abstractmethod
    def encrypt(self, data: str) -> str:
        """
        Encrypt or tokenize the sensitive data.
        
        Args:
            data: The sensitive data to protect
            
        Returns:
            An encrypted or tokenized representation
        """
        pass
    
    @abstractmethod
    def decrypt(self, encrypted: str) -> str:
        """
        Decrypt or detokenize the protected data.
        
        Args:
            encrypted: The encrypted/tokenized data
            
        Returns:
            The original sensitive data
        """
        pass


class HoneytokenHandler(ABC):
    """
    Abstract interface for custom honeytoken detection handlers.
    
    Instead of passing a static list of honeytokens, users can inject
    a handler that checks against a database, API, or other dynamic source.
    
    This is critical for large-scale deployments where:
    - Honeytokens are generated dynamically
    - Detection needs to trigger complex workflows
    - Integration with SIEM/SOC systems is required
    
    Example:
        class MyHoneytokenHandler(HoneytokenHandler):
            def __init__(self):
                self.redis_client = redis.Redis(...)
            
            def is_honeytoken(self, data: str) -> bool:
                # Check against Redis cache
                return self.redis_client.sismember("honeytokens", data)
            
            def on_detected(self, data: str, context: dict):
                # Send alert to SIEM
                siem.send_alert({
                    "severity": "CRITICAL",
                    "type": "honeytoken_access",
                    "data": data,
                    "context": context
                })
    """
    
    @abstractmethod
    def is_honeytoken(self, data: str) -> bool:
        """
        Check if the given data is a honeytoken.
        
        Args:
            data: The data to check
            
        Returns:
            True if it's a honeytoken, False otherwise
        """
        pass
    
    @abstractmethod
    def on_detected(self, data: str, context: Optional[dict] = None):
        """
        Called when a honeytoken is detected.
        
        Args:
            data: The honeytoken that was detected
            context: Optional context information (timestamp, logger name, etc.)
        """
        pass


class AnonymizationStrategy(ABC):
    """
    Abstract interface for custom anonymization strategies.
    
    This addresses the LGPD/GDPR compliance concerns raised in Reddit feedback.
    Different strategies provide different levels of anonymization:
    
    - IRREVERSIBLE: True anonymization (cannot be reversed)
    - PSEUDONYMIZATION: Can be reversed with additional information
    - TOKENIZATION: External token vault
    
    Example:
        class IrreversibleAnonymizer(AnonymizationStrategy):
            def anonymize(self, data: str, data_type: str) -> str:
                # Use random UUID - no way to reverse
                import uuid
                return f"[ANON-{uuid.uuid4().hex[:8]}]"
            
            def can_reverse(self) -> bool:
                return False
    """
    
    @abstractmethod
    def anonymize(self, data: str, data_type: str) -> str:
        """
        Anonymize the sensitive data.
        
        Args:
            data: The sensitive data
            data_type: Type of data (CPF, CNPJ, etc.) for context
            
        Returns:
            Anonymized representation
        """
        pass
    
    @abstractmethod
    def can_reverse(self) -> bool:
        """
        Indicates if this anonymization can be reversed.
        
        Returns:
            True if reversible (pseudonymization), False if truly anonymous
        """
        pass


# Built-in implementations

class DefaultHashFunction:
    """
    Default deterministic hash function using SHA-256.
    
    Note: This is PSEUDONYMIZATION, not true anonymization.
    The same input always produces the same output, which means
    if someone has access to the original data, they can verify
    if a hash matches by computing the hash themselves.
    
    For true anonymization, use IrreversibleAnonymizer instead.
    """
    
    def __init__(self, salt: Optional[str] = None):
        import os
        self.salt = salt or os.environ.get("OPAQUE_SALT", "default_insecure_salt_change_me")
    
    def __call__(self, data: str) -> str:
        import hashlib
        combined = f"{data}{self.salt}".encode('utf-8')
        full_hash = hashlib.sha256(combined).hexdigest()
        short_hash = full_hash[:4].upper()
        return f"[HASH-{short_hash}]"


class IrreversibleAnonymizer(AnonymizationStrategy):
    """
    True anonymization using random UUIDs.
    
    This provides REAL anonymization as required by LGPD/GDPR.
    Each occurrence gets a unique random identifier with no way
    to reverse it or correlate it with the original data.
    
    Use this when:
    - You don't need to correlate logs
    - Compliance requires true anonymization
    - You're logging for debugging only, not audit trails
    """
    
    def anonymize(self, data: str, data_type: str) -> str:
        import uuid
        return f"[ANON-{uuid.uuid4().hex[:8].upper()}]"
    
    def can_reverse(self) -> bool:
        return False


class DeterministicPseudonymizer(AnonymizationStrategy):
    """
    Deterministic pseudonymization using HMAC-SHA256.
    
    This is PSEUDONYMIZATION, not anonymization.
    Same input = same output, allowing log correlation.
    
    COMPLIANCE WARNING:
    - This does NOT provide true anonymization
    - Logs containing these hashes are still subject to LGPD/GDPR
    - You must protect the salt/key as sensitive data
    - Consider this as "obscured" data, not anonymous data
    
    Use this when:
    - You need to correlate logs (same CPF = same hash)
    - You have proper data protection policies in place
    - You understand the compliance implications
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        import os
        self.secret_key = secret_key or os.environ.get("OPAQUE_SECRET_KEY", "change_me_insecure_default")
    
    def anonymize(self, data: str, data_type: str) -> str:
        import hmac
        import hashlib
        
        # Use HMAC for cryptographically secure hashing
        h = hmac.new(
            self.secret_key.encode('utf-8'),
            f"{data_type}:{data}".encode('utf-8'),
            hashlib.sha256
        )
        short_hash = h.hexdigest()[:8].upper()
        return f"[PSEUDO-{short_hash}]"
    
    def can_reverse(self) -> bool:
        return False  # Cannot reverse HMAC, but can verify


class SimpleHoneytokenHandler(HoneytokenHandler):
    """
    Simple in-memory honeytoken handler.
    
    For production use, extend this to check against:
    - Redis/Memcached
    - Database
    - External API
    """
    
    def __init__(self, honeytokens: list[str], alert_callback: Optional[Callable] = None):
        self.honeytokens = set(honeytokens)
        self.alert_callback = alert_callback
    
    def is_honeytoken(self, data: str) -> bool:
        return data in self.honeytokens
    
    def on_detected(self, data: str, context: Optional[dict] = None):
        import sys
        print(f"🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: {data}", file=sys.stderr)
        
        if self.alert_callback:
            self.alert_callback(data, context)

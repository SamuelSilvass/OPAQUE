import pytest
import logging
from unittest.mock import MagicMock
from opaque import OpaqueLogger, Validators
from opaque.callbacks import (
    HashFunction, VaultInterface, HoneytokenHandler, 
    AnonymizationStrategy, IrreversibleAnonymizer, DeterministicPseudonymizer
)

# --- Custom Implementations for Testing ---

class CustomHash:
    def __call__(self, data: str) -> str:
        return f"[CUSTOM-HASH:{data[::-1]}]"  # Simple reverse for testing

class CustomVault(VaultInterface):
    def encrypt(self, data: str) -> str:
        return f"{{VAULTED:{data}}}"
    
    def decrypt(self, encrypted: str) -> str:
        return encrypted.replace("{VAULTED:", "").replace("}", "")

class CustomHoneytokenHandler(HoneytokenHandler):
    def __init__(self):
        self.detected = []
        self.db = {"999.888.777-66"} # Mock DB

    def is_honeytoken(self, data: str) -> bool:
        return data in self.db

    def on_detected(self, data: str, context: dict = None):
        self.detected.append((data, context))

class CustomAnonymizer(AnonymizationStrategy):
    def anonymize(self, data: str, data_type: str) -> str:
        return f"ANON-{data_type}-{len(data)}"
    
    def can_reverse(self) -> bool:
        return False

# --- Tests ---

def test_custom_hash_injection():
    custom_hash = CustomHash()
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="HASH",
        hash_function=custom_hash
    )
    
    logger = OpaqueLogger("test_hash")
    scanner = logger.scanner
    # Using valid CPF
    result = scanner.sanitize("CPF 529.982.247-25")
    # Expecting the CPF to be reversed in the hash
    assert "[CUSTOM-HASH:52-742.289.925]" in result

def test_custom_vault_injection():
    custom_vault = CustomVault()
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="VAULT",
        vault_implementation=custom_vault
    )
    
    logger = OpaqueLogger("test_vault")
    scanner = logger.scanner
    result = scanner.sanitize("CPF 529.982.247-25")
    assert "{VAULTED:529.982.247-25}" in result

def test_custom_honeytoken_handler():
    handler = CustomHoneytokenHandler()
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        honeytoken_handler=handler
    )
    
    logger = OpaqueLogger("test_honey")
    scanner = logger.scanner
    
    # Test detection
    msg = "Access with 999.888.777-66"
    result = scanner.sanitize(msg)
    
    assert "[HONEYTOKEN TRIGGERED]" in result
    assert len(handler.detected) == 1
    assert handler.detected[0][0] == "999.888.777-66"
    
    # Test non-detection
    msg2 = "Access with 529.982.247-25"
    result2 = scanner.sanitize(msg2)
    # Should be sanitized by validator (default HASH) because it's a valid CPF
    assert "529.982.247-25" not in result2 
    assert "[HASH-" in result2
    # Should NOT be flagged as honeytoken
    assert len(handler.detected) == 1

def test_irreversible_anonymization():
    anonymizer = IrreversibleAnonymizer()
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="ANONYMIZE",
        anonymization_strategy=anonymizer
    )
    
    logger = OpaqueLogger("test_anon")
    scanner = logger.scanner
    
    cpf = "529.982.247-25"
    res1 = scanner.sanitize(f"CPF {cpf}")
    res2 = scanner.sanitize(f"CPF {cpf}")
    
    # Extract the anonymized parts
    # Format: [ANON-UUID]
    
    assert "ANON-" in res1
    assert "ANON-" in res2
    assert res1 != res2 # Should be different (random UUID)

def test_deterministic_pseudonymization():
    pseudo = DeterministicPseudonymizer(secret_key="test-key")
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="ANONYMIZE",
        anonymization_strategy=pseudo
    )
    
    logger = OpaqueLogger("test_pseudo")
    scanner = logger.scanner
    
    cpf = "529.982.247-25"
    res1 = scanner.sanitize(f"CPF {cpf}")
    res2 = scanner.sanitize(f"CPF {cpf}")
    
    assert "PSEUDO-" in res1
    assert res1 == res2 # Should be identical (deterministic)

def test_custom_anonymization_strategy():
    custom_anon = CustomAnonymizer()
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="ANONYMIZE",
        anonymization_strategy=custom_anon
    )
    
    logger = OpaqueLogger("test_custom_anon")
    scanner = logger.scanner
    
    cpf = "529.982.247-25"
    result = scanner.sanitize(f"CPF {cpf}")
    
    assert "ANON-CPFValidator-14" in result # 14 chars in CPF

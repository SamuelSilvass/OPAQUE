"""
Tests for custom callback system.

This tests the new functionality added based on Reddit feedback:
- Custom hash functions
- Custom vault implementations
- Custom honeytoken handlers
- Anonymization strategies (LGPD/GDPR compliance)
"""

import pytest
import logging
from opaque import (
    OpaqueLogger, OpaqueScanner, Validators,
    VaultInterface, HoneytokenHandler, AnonymizationStrategy,
    IrreversibleAnonymizer, DeterministicPseudonymizer
)


class TestCustomHashFunction:
    """Test custom hash function injection"""
    
    def test_custom_hash_function(self):
        """Test that custom hash function is used"""
        def my_hash(data: str) -> str:
            return f"[CUSTOM-{len(data)}]"
        
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="HASH",
            hash_function=my_hash
        )
        
        result = scanner.sanitize("CPF: 529.982.247-25")
        assert "[CUSTOM-14]" in result  # Length of "529.982.247-25"
    
    def test_default_hash_function(self):
        """Test that default hash function works when none provided"""
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="HASH"
        )
        
        result = scanner.sanitize("CPF: 529.982.247-25")
        assert "[HASH-" in result


class TestCustomVault:
    """Test custom vault implementation injection"""
    
    def test_custom_vault_implementation(self):
        """Test that custom vault is used"""
        class MockVault(VaultInterface):
            def encrypt(self, data: str) -> str:
                return f"[MOCK-VAULT:{data[:3]}]"
            
            def decrypt(self, encrypted: str) -> str:
                return "decrypted"
        
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="VAULT",
            vault_implementation=MockVault()
        )
        
        result = scanner.sanitize("CPF: 529.982.247-25")
        assert "[MOCK-VAULT:529]" in result


class TestCustomHoneytokenHandler:
    """Test custom honeytoken handler injection"""
    
    def test_custom_honeytoken_handler(self):
        """Test that custom honeytoken handler is called"""
        detected_tokens = []
        
        class MockHoneytokenHandler(HoneytokenHandler):
            def is_honeytoken(self, data: str) -> bool:
                return data == "999.888.777-66"
            
            def on_detected(self, data: str, context: dict = None):
                detected_tokens.append(data)
        
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            honeytoken_handler=MockHoneytokenHandler()
        )
        
        result = scanner.sanitize("CPF: 999.888.777-66")
        assert len(detected_tokens) == 1
        assert detected_tokens[0] == "999.888.777-66"
        assert "[HONEYTOKEN TRIGGERED]" in result
    
    def test_backward_compatibility_honeytokens_list(self):
        """Test that old-style honeytoken list still works"""
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            honeytokens=["999.888.777-66"]
        )
        
        result = scanner.sanitize("CPF: 999.888.777-66")
        assert "[HONEYTOKEN TRIGGERED]" in result


class TestAnonymizationStrategies:
    """Test anonymization strategies for LGPD/GDPR compliance"""
    
    def test_irreversible_anonymizer(self):
        """Test that irreversible anonymizer produces different outputs"""
        anonymizer = IrreversibleAnonymizer()
        
        result1 = anonymizer.anonymize("529.982.247-25", "CPF")
        result2 = anonymizer.anonymize("529.982.247-25", "CPF")
        
        # Same input should produce DIFFERENT outputs (true anonymization)
        assert result1 != result2
        assert result1.startswith("[ANON-")
        assert result2.startswith("[ANON-")
        assert not anonymizer.can_reverse()
    
    def test_deterministic_pseudonymizer(self):
        """Test that deterministic pseudonymizer produces same outputs"""
        pseudonymizer = DeterministicPseudonymizer(secret_key="test-key")
        
        result1 = pseudonymizer.anonymize("529.982.247-25", "CPF")
        result2 = pseudonymizer.anonymize("529.982.247-25", "CPF")
        
        # Same input should produce SAME output (pseudonymization)
        assert result1 == result2
        assert result1.startswith("[PSEUDO-")
        assert not pseudonymizer.can_reverse()  # Cannot reverse HMAC
    
    def test_anonymize_obfuscation_method(self):
        """Test ANONYMIZE obfuscation method"""
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="ANONYMIZE"
        )
        
        result1 = scanner.sanitize("CPF: 529.982.247-25")
        result2 = scanner.sanitize("CPF: 529.982.247-25")
        
        # Should use IrreversibleAnonymizer by default
        assert "[ANON-" in result1
        assert "[ANON-" in result2
        # Different outputs each time
        assert result1 != result2
    
    def test_custom_anonymization_strategy(self):
        """Test custom anonymization strategy"""
        class CustomAnonymizer(AnonymizationStrategy):
            def anonymize(self, data: str, data_type: str) -> str:
                return f"[CUSTOM-{data_type}-ANON]"
            
            def can_reverse(self) -> bool:
                return False
        
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="ANONYMIZE",
            anonymization_strategy=CustomAnonymizer()
        )
        
        result = scanner.sanitize("CPF: 529.982.247-25")
        # Validator class name includes "Validator" suffix
        assert "[CUSTOM-CPFValidator-ANON]" in result


class TestLoggerIntegrationWithCallbacks:
    """Test OpaqueLogger with custom callbacks"""
    
    def test_logger_with_custom_hash(self):
        """Test logger integration with custom hash function"""
        def my_hash(data: str) -> str:
            return f"[LOGGER-HASH-{len(data)}]"
        
        # Setup logger with custom hash
        from opaque.core import OpaqueScanner
        
        logger = OpaqueLogger("test_logger")
        logger.scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            hash_function=my_hash
        )
        
        # Test that sanitization works with custom hash
        result = logger.scanner.sanitize("User CPF: 529.982.247-25")
        assert "[LOGGER-HASH-14]" in result
    
    def test_logger_with_anonymization(self):
        """Test logger with true anonymization"""
        logger = OpaqueLogger("test_anon_logger")
        logger.scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="ANONYMIZE"
        )
        
        # Test that anonymization works
        result = logger.scanner.sanitize("User CPF: 529.982.247-25")
        assert "[ANON-" in result


class TestComplianceScenarios:
    """Test real-world compliance scenarios"""
    
    def test_lgpd_compliant_logging(self):
        """Test LGPD-compliant logging (true anonymization)"""
        # For LGPD compliance, use irreversible anonymization
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF, Validators.BR.CNPJ],
            obfuscation_method="ANONYMIZE",
            anonymization_strategy=IrreversibleAnonymizer()
        )
        
        # Use valid CNPJ: 11.222.333/0001-81
        log_entry = "Transaction: CPF 529.982.247-25 paid CNPJ 11.222.333/0001-81"
        result = scanner.sanitize(log_entry)
        
        # Both should be anonymized
        assert "[ANON-" in result
        # Original data should not be present
        assert "529.982.247-25" not in result
        assert "11.222.333/0001-81" not in result
    
    def test_audit_trail_with_pseudonymization(self):
        """Test audit trail scenario (needs correlation)"""
        # For audit trails, use deterministic pseudonymization
        pseudonymizer = DeterministicPseudonymizer(secret_key="audit-key")
        
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="ANONYMIZE",
            anonymization_strategy=pseudonymizer
        )
        
        # Same CPF should produce same hash for correlation
        log1 = scanner.sanitize("User 529.982.247-25 logged in")
        log2 = scanner.sanitize("User 529.982.247-25 made purchase")
        
        # Extract the hashes
        import re
        hash1 = re.search(r'\[PSEUDO-[A-F0-9]+\]', log1).group()
        hash2 = re.search(r'\[PSEUDO-[A-F0-9]+\]', log2).group()
        
        # Should be the same hash (allows correlation)
        assert hash1 == hash2
    
    def test_enterprise_scale_honeytoken_detection(self):
        """Test enterprise-scale honeytoken detection"""
        # Simulate database-backed honeytoken system
        honeytokens_db = {"999.888.777-66", "000.000.000-00", "111.111.111-11"}
        detected_alerts = []
        
        class EnterpriseHoneytokenHandler(HoneytokenHandler):
            def is_honeytoken(self, data: str) -> bool:
                # In real implementation, this would be a Redis/DB lookup
                return data in honeytokens_db
            
            def on_detected(self, data: str, context: dict = None):
                # In real implementation, send to SIEM
                detected_alerts.append({
                    "token": data,
                    "context": context
                })
        
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            honeytoken_handler=EnterpriseHoneytokenHandler()
        )
        
        # Test multiple logs
        scanner.sanitize("Access: 529.982.247-25")  # Normal
        scanner.sanitize("Access: 999.888.777-66")  # Honeytoken!
        scanner.sanitize("Access: 000.000.000-00")  # Honeytoken!
        
        # Should have detected 2 honeytokens
        assert len(detected_alerts) == 2
        assert detected_alerts[0]["token"] == "999.888.777-66"
        assert detected_alerts[1]["token"] == "000.000.000-00"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

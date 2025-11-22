import pytest
from opaque.vault import Vault
from opaque.core import OpaqueScanner
from opaque.validators import Validators

class TestVault:
    def test_encrypt_decrypt(self):
        key = "my-secret-master-key"
        vault = Vault(key=key)
        
        data = "123.456.789-00"
        encrypted = vault.encrypt(data)
        
        assert encrypted.startswith("[VAULT:")
        assert data not in encrypted
        
        decrypted = vault.decrypt(encrypted)
        assert decrypted == data

    def test_different_keys_fail(self):
        vault1 = Vault(key="key1")
        vault2 = Vault(key="key2")
        
        data = "secret"
        encrypted = vault1.encrypt(data)
        
        # Decrypting with wrong key returns error string in my implementation
        result = vault2.decrypt(encrypted)
        assert "Error decrypting" in result

class TestAdvancedFeatures:
    def test_honeytoken_trigger(self, capsys):
        honeytoken = "999.888.777-66"
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            honeytokens=[honeytoken]
        )
        
        text = f"User tried to access {honeytoken}"
        sanitized = scanner.sanitize(text)
        
        assert "[HONEYTOKEN TRIGGERED]" in sanitized
        assert honeytoken not in sanitized
        
        # Check stderr for alert
        captured = capsys.readouterr()
        assert f"HONEYTOKEN DETECTED: {honeytoken}" in captured.err

    def test_circuit_breaker(self):
        scanner = OpaqueScanner(rules=[Validators.BR.CPF])
        scanner.CIRCUIT_THRESHOLD = 5 # Low threshold for test
        
        # Trigger flood
        # Each call processes 1 match if we pass a CPF
        cpf = "529.982.247-25"
        
        # We need to simulate multiple matches quickly.
        # The counter increments by number of matches found.
        
        # 1. Normal operation
        assert "HASH" in scanner.sanitize(cpf)
        assert not scanner.circuit_open
        
        # 2. Flood
        # Code checks if len(matches) > 10. So we need 11 matches to increment error_count.
        flood_text = (cpf + " ") * 12 
        scanner.sanitize(flood_text)
        
        # Now error_count should be > 5
        assert scanner.error_count > 5
        
        # 3. Next call should trigger breaker
        result = scanner.sanitize(cpf)
        assert result == "[OPAQUE: LOG FLOOD PROTECTION ACTIVATED - DATA DISCARDED]"
        assert scanner.circuit_open

class TestCrashHandler:
    def test_sanitize_traceback(self, capsys):
        from opaque.crash_handler import CrashHandler
        from opaque.core import OpaqueScanner
        
        scanner = OpaqueScanner(rules=[Validators.BR.CPF])
        handler = CrashHandler(scanner)
        
        # Simulate a crash
        try:
            password = "super_secret_password"
            cpf = "529.982.247-25"
            raise ValueError("Crash with 529.982.247-25")
        except ValueError:
            # Manually invoke handler
            import sys
            handler.handle_exception(*sys.exc_info())
            
        captured = capsys.readouterr()
        stderr = captured.err
        
        # Check redaction in locals
        assert "super_secret_password" not in stderr
        assert "[REDACTED_SECRET_KEY]" in stderr
        
        # Check redaction in exception message
        assert "529.982.247-25" not in stderr
        assert "[HASH-" in stderr

import pytest
import logging
from opaque.core import OpaqueScanner, OpaqueLogger
from opaque.validators import Validators
from opaque.utils import Fingerprinter

class TestOpaqueScanner:
    def test_sanitize_cpf_hash(self):
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="HASH"
        )
        # Valid CPF
        text = "O CPF do cliente é 529.982.247-25."
        sanitized = scanner.sanitize(text)
        assert "529.982.247-25" not in sanitized
        assert "[HASH-" in sanitized
        
    def test_sanitize_cpf_mask(self):
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="MASK"
        )
        text = "CPF: 529.982.247-25"
        sanitized = scanner.sanitize(text)
        assert "***" in sanitized
        assert "529.982.247-25" not in sanitized

    def test_ignore_invalid_cpf(self):
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="HASH"
        )
        # Invalid CPF should NOT be censored
        text = "Erro no CPF 111.222.333-44"
        sanitized = scanner.sanitize(text)
        assert "111.222.333-44" in sanitized

    def test_mixed_content(self):
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="HASH"
        )
        text = "Valid: 529.982.247-25, Invalid: 111.222.333-44"
        sanitized = scanner.sanitize(text)
        assert "[HASH-" in sanitized
        assert "111.222.333-44" in sanitized

    def test_json_structure(self):
        scanner = OpaqueScanner(
            rules=[Validators.BR.CPF],
            obfuscation_method="HASH"
        )
        data = {
            "user": {
                "cpf": "529.982.247-25",
                "id": 123
            },
            "list": ["529.982.247-25", "safe"]
        }
        processed = scanner.process_structure(data)
        assert "[HASH-" in processed["user"]["cpf"]
        assert processed["user"]["id"] == 123
        assert "[HASH-" in processed["list"][0]
        assert processed["list"][1] == "safe"

class TestFingerprinter:
    def test_deterministic_hash(self):
        fp1 = Fingerprinter(salt="salty")
        fp2 = Fingerprinter(salt="salty")
        fp3 = Fingerprinter(salt="pepper")
        
        data = "secret"
        assert fp1.hash(data) == fp2.hash(data)
        assert fp1.hash(data) != fp3.hash(data)

class TestLoggerIntegration:
    def test_logger_sanitization(self, caplog):
        OpaqueLogger.setup_defaults(
            rules=[Validators.BR.CPF],
            obfuscation_method="MASK"
        )
        
        # Correct usage: Register the class and get logger via factory
        # This ensures the logger is attached to the Manager and has the Root logger as parent
        original_class = logging.getLoggerClass()
        logging.setLoggerClass(OpaqueLogger)
        try:
            logger = logging.getLogger("test_logger_integration")
            
            with caplog.at_level(logging.INFO):
                logger.info("User CPF 529.982.247-25 logged in")
                
            assert "***" in caplog.text
            assert "529.982.247-25" not in caplog.text
        finally:
            logging.setLoggerClass(original_class)
        assert "529.982.247-25" not in caplog.text

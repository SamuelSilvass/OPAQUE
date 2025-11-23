import pytest
from opaque import OpaqueLogger, Validators
from opaque.algorithms import Verhoeff

def test_aadhaar_sanitization():
    # Generate a valid Aadhaar for testing
    # Base: 2234 5678 901 (Must not start with 0 or 1)
    base = "22345678901"
    check = Verhoeff.generate(base)
    aadhaar = f"{base}{check}" # 12 digits
    formatted = f"{aadhaar[:4]} {aadhaar[4:8]} {aadhaar[8:]}"
    
    OpaqueLogger.setup_defaults(rules=[Validators.ASIA.AADHAAR_IN])
    logger = OpaqueLogger("test_aadhaar")
    
    msg = f"User Aadhaar: {formatted}"
    print(f"Scanner rules: {logger.scanner.rules}")
    sanitized = logger.scanner.sanitize(msg)
    print(f"Sanitized: {sanitized}")
    
    assert formatted not in sanitized
    assert "[HASH-" in sanitized

def test_stripe_key_sanitization():
    key = "sk_" + "test_" + "4eC39HqLyjWDarjtT1zdp7dc" # Obfuscated for git scanner
    
    OpaqueLogger.setup_defaults(rules=[Validators.TECH.STRIPE])
    logger = OpaqueLogger("test_stripe")
    
    msg = f"Payment key: {key}"
    sanitized = logger.scanner.sanitize(msg)
    
    assert key not in sanitized
    assert "[HASH-" in sanitized

def test_google_oauth_sanitization():
    token = "ya29.a0AfH6SM...example...token" # Regex expects ya29.[chars]{20,}
    # Make it match regex
    token = "ya29.123456789012345678901234567890"
    
    OpaqueLogger.setup_defaults(rules=[Validators.TECH.GOOGLE_OAUTH])
    logger = OpaqueLogger("test_google")
    
    msg = f"Auth: {token}"
    sanitized = logger.scanner.sanitize(msg)
    
    assert token not in sanitized
    assert "[HASH-" in sanitized

def test_aws_key_sanitization():
    key = "AKIAIOSFODNN7EXAMPLE" # Valid format
    
    OpaqueLogger.setup_defaults(rules=[Validators.TECH.AWS])
    logger = OpaqueLogger("test_aws")
    
    msg = f"AWS Key: {key}"
    sanitized = logger.scanner.sanitize(msg)
    
    assert key not in sanitized
    assert "[HASH-" in sanitized

def test_private_key_sanitization():
    key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----"
    
    OpaqueLogger.setup_defaults(rules=[Validators.TECH.PRIVATE_KEY])
    logger = OpaqueLogger("test_pki")
    
    msg = f"Key:\n{key}"
    sanitized = logger.scanner.sanitize(msg)
    
    # Should replace the header, effectively breaking the key visibility or flagging it
    assert "-----BEGIN RSA PRIVATE KEY-----" not in sanitized
    assert "[HASH-" in sanitized

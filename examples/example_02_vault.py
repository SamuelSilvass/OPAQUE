"""
Example 2: Vault Mode - Reversible Encryption
==============================================

This example demonstrates OPAQUE's Vault Mode:
- AES-256 encryption of sensitive data
- Reversible encryption for authorized debugging
- CLI tool for decryption
"""

import logging
import sys
import os
from opaque import OpaqueLogger, Validators, Vault

def setup_vault_logging():
    """Configure OPAQUE with Vault Mode."""
    # Set master key (in production, use environment variable or KMS)
    master_key = "demo-master-key-change-in-production"
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF, Validators.BR.CNPJ],
        obfuscation_method="VAULT",
        vault_key=master_key
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("example_vault")
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger, master_key

def main():
    logger, master_key = setup_vault_logging()
    
    print("=" * 60)
    print("OPAQUE Example 2: Vault Mode")
    print("=" * 60)
    
    # Test Case 1: Encrypt CPF
    print("\n1. Logging with Vault encryption:")
    logger.info("User CPF: 529.982.247-25")
    print("   ✓ CPF encrypted with AES-256")
    
    # Test Case 2: Manual encryption/decryption
    print("\n2. Manual Vault operations:")
    vault = Vault(key=master_key)
    
    sensitive_data = "123.456.789-09"
    encrypted = vault.encrypt(sensitive_data)
    print(f"   Original: {sensitive_data}")
    print(f"   Encrypted: {encrypted}")
    
    decrypted = vault.decrypt(encrypted)
    print(f"   Decrypted: {decrypted}")
    print(f"   ✓ Match: {decrypted == sensitive_data}")
    
    # Test Case 3: CLI usage example
    print("\n3. CLI Decryption Example:")
    print(f"   To decrypt in production, use:")
    print(f'   python -m opaque.cli reveal "{encrypted}" --key={master_key}')
    
    # Test Case 4: Security demonstration
    print("\n4. Security Test - Wrong Key:")
    wrong_vault = Vault(key="wrong-key")
    try:
        wrong_vault.decrypt(encrypted)
    except Exception:
        result = wrong_vault.decrypt(encrypted)
        print(f"   Result with wrong key: {result}")
        print("   ✓ Decryption failed as expected")
    
    print("\n" + "=" * 60)
    print("Vault Mode example completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

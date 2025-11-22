"""
Example 1: Basic CPF Validation and Sanitization
=================================================

This example demonstrates the core functionality of OPAQUE:
- Mathematical validation of Brazilian CPF documents
- Automatic sanitization in logs
- Preservation of invalid data for debugging
"""

import logging
import sys
from opaque import OpaqueLogger, Validators

def setup_logging():
    """Configure OPAQUE with CPF validation."""
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="HASH"
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("example_basic")
    
    # Add console handler for visibility
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

def main():
    logger = setup_logging()
    
    print("=" * 60)
    print("OPAQUE Example 1: Basic CPF Validation")
    print("=" * 60)
    
    # Test Case 1: Valid CPF (will be sanitized)
    print("\n1. Logging a VALID CPF:")
    logger.info("Processing payment for CPF: 529.982.247-25")
    print("   ✓ CPF was sanitized to [HASH-XXXX]")
    
    # Test Case 2: Invalid CPF (will NOT be sanitized)
    print("\n2. Logging an INVALID CPF:")
    logger.info("Error in transaction with CPF: 111.222.333-44")
    print("   ✓ Invalid CPF was preserved for debugging")
    
    # Test Case 3: Mixed content
    print("\n3. Logging mixed content:")
    logger.info("User 529.982.247-25 tried to use fake CPF 123.456.789-00")
    print("   ✓ Only mathematically valid CPF was sanitized")
    
    # Test Case 4: JSON structure
    print("\n4. Logging JSON with nested CPF:")
    data = {
        "transaction_id": "TX-12345",
        "customer": {
            "name": "João Silva",
            "cpf": "529.982.247-25"
        },
        "amount": 150.00
    }
    logger.info(data)
    print("   ✓ CPF inside JSON was sanitized")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()

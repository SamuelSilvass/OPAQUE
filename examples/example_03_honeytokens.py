"""
Example 3: Honeytokens - Intrusion Detection
=============================================

This example demonstrates OPAQUE's Honeytoken feature:
- Detection of bait data usage
- Automatic alerts on suspicious access
- Integration with security monitoring
"""

import logging
import sys
from opaque import OpaqueLogger, Validators

def setup_honeytoken_logging():
    """Configure OPAQUE with Honeytokens."""
    # Define bait CPFs that should never appear in production
    honeytokens = [
        "999.888.777-66",  # Test CPF 1
        "000.000.000-00",  # Test CPF 2 (also invalid)
        "123.456.789-09",  # Common test CPF
    ]
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF],
        obfuscation_method="HASH",
        honeytokens=honeytokens
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("example_honeytoken")
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

def main():
    logger = setup_honeytoken_logging()
    
    print("=" * 60)
    print("OPAQUE Example 3: Honeytokens")
    print("=" * 60)
    
    # Test Case 1: Normal operation (no honeytoken)
    print("\n1. Normal operation - Real CPF:")
    logger.info("Processing CPF: 529.982.247-25")
    print("   ✓ No alert triggered")
    
    # Test Case 2: Honeytoken detected
    print("\n2. SECURITY TEST - Honeytoken detected:")
    print("   (Check stderr for RED ALERT)")
    logger.info("Suspicious access with CPF: 999.888.777-66")
    print("   ✓ Alert should appear in stderr above")
    
    # Test Case 3: Multiple honeytokens
    print("\n3. Multiple honeytokens in one message:")
    logger.info("Testing with 123.456.789-09 and 999.888.777-66")
    print("   ✓ Multiple alerts triggered")
    
    # Test Case 4: Real-world scenario
    print("\n4. Real-world scenario simulation:")
    print("   Simulating login attempt with test credentials...")
    
    login_data = {
        "username": "admin",
        "cpf": "999.888.777-66",
        "ip": "192.168.1.100",
        "timestamp": "2024-01-15 14:30:00"
    }
    
    logger.warning(f"Login attempt: {login_data}")
    print("   ✓ Security team should be notified")
    
    print("\n" + "=" * 60)
    print("Honeytoken example completed!")
    print("In production, integrate with:")
    print("  - Slack/Discord webhooks")
    print("  - PagerDuty alerts")
    print("  - SIEM systems")
    print("=" * 60)

if __name__ == "__main__":
    main()

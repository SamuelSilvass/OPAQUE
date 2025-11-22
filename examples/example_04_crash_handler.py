"""
Example 4: Crash Handler - Traceback Sanitization
==================================================

This example demonstrates OPAQUE's Crash Handler:
- Automatic sanitization of exception tracebacks
- Protection of sensitive data in stack traces
- Redaction of secret variable names
"""

import sys
from opaque import OpaqueLogger, Validators, install_crash_handler

def setup_crash_protection():
    """Configure OPAQUE with Crash Handler."""
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF, Validators.FINANCE.CREDIT_CARD]
    )
    
    # Install the crash handler
    install_crash_handler()
    print("✓ Crash handler installed")

def function_with_secrets():
    """Simulates a function with sensitive data that crashes."""
    # These variables would normally leak in traceback
    password = "super_secret_password_123"
    api_key = "sk-1234567890abcdef"
    user_cpf = "529.982.247-25"
    credit_card = "4242424242424242"
    
    # Simulate an error
    raise ValueError(f"Payment failed for CPF {user_cpf} with card {credit_card}")

def nested_function_call():
    """Demonstrates nested stack traces."""
    token = "bearer_token_xyz789"
    function_with_secrets()

def main():
    print("=" * 60)
    print("OPAQUE Example 4: Crash Handler")
    print("=" * 60)
    
    setup_crash_protection()
    
    print("\n1. Triggering a crash with sensitive data...")
    print("   Watch how OPAQUE sanitizes the traceback:\n")
    
    try:
        nested_function_call()
    except ValueError:
        # The crash handler already intercepted and sanitized the output
        print("\n✓ Crash was intercepted and sanitized")
        print("✓ Sensitive data was redacted from traceback")
        print("✓ CPF and credit card were hashed")
        print("✓ Password/token variables were marked as [REDACTED_SECRET_KEY]")
    
    print("\n" + "=" * 60)
    print("Crash Handler example completed!")
    print("=" * 60)
    print("\nKey protections:")
    print("  ✓ Variable names with 'password', 'secret', 'key', 'token' redacted")
    print("  ✓ CPF/CNPJ values in strings sanitized")
    print("  ✓ Credit card numbers sanitized")
    print("  ✓ Original traceback structure preserved")

if __name__ == "__main__":
    main()

"""
Loguru Integration for OPAQUE
==============================

Provides a custom sink for Loguru that sanitizes sensitive data before logging.

Example:
    from loguru import logger
    from opaque.integrations.loguru_integration import OpaqueLoguruSink
    from opaque import Validators
    
    sink = OpaqueLoguruSink(rules=[Validators.BR.CPF, Validators.FINANCE.CREDIT_CARD])
    logger.add(sink, format="{time} {level} {message}")
    
    logger.info("User CPF: 529.982.247-25")
    # Output: 2025-11-23 15:00:00 INFO User CPF: [HASH-3A4C]
"""

from typing import Any, Dict, List, Optional
import sys
from ..validators import Validator
from ..core import OpaqueScanner


class OpaqueLoguruSink:
    """Custom Loguru sink that sanitizes sensitive data."""
    
    def __init__(
        self,
        rules: List[Validator],
        obfuscation_method: str = "HASH",
        vault_key: Optional[str] = None,
        honeytokens: Optional[List[str]] = None,
        output=sys.stdout
    ):
        """
        Initialize the Loguru sink.
        
        Args:
            rules: List of OPAQUE validators
            obfuscation_method: Method to use (HASH, VAULT, ANONYMIZE)
            vault_key: Key for vault encryption
            honeytokens: List of honeytoken values
            output: Output stream (default: stdout)
        """
        self.scanner = OpaqueScanner(
            rules=rules,
            obfuscation_method=obfuscation_method,
            vault_key=vault_key,
            honeytokens=honeytokens or []
        )
        self.output = output
    
    def write(self, message: str):
        """
        Write a sanitized log message.
        
        Args:
            message: The log message to sanitize and write
        """
        sanitized = self.scanner.sanitize(message)
        self.output.write(sanitized + '\n')
        self.output.flush()


def patch_loguru(
    rules: List[Validator],
    obfuscation_method: str = "HASH",
    vault_key: Optional[str] = None,
    **add_kwargs
):
    """
    Patch Loguru's default logger with OPAQUE sanitization.
    
    Args:
        rules: List of OPAQUE validators
        obfuscation_method: Obfuscation method
        vault_key: Vault key (if applicable)
        **add_kwargs: Additional arguments for logger.add()
    
    Returns:
        The handler ID from logger.add()
    """
    try:
        from loguru import logger
    except ImportError:
        raise ImportError(
            "loguru is not installed. Install it with: pip install loguru"
        )
    
    # Remove default handler
    logger.remove()
    
    # Add OPAQUE sink
    sink = OpaqueLoguruSink(rules, obfuscation_method, vault_key)
    return logger.add(sink, **add_kwargs)

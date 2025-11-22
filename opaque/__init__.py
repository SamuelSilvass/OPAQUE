"""
OPAQUE - Deterministic Data Masking Engine
===========================================

A high-performance, context-aware data sanitization library designed for 
enterprise environments where data integrity and performance are critical.

Unlike AI-based solutions that guess, OPAQUE validates using mathematical 
algorithms (Mod 11, Luhn) to ensure precision and eliminate false positives.

Key Features:
- Mathematical validation (CPF, CNPJ, Credit Cards, Pix)
- Vault Mode for reversible encryption
- Honeytokens for intrusion detection
- Circuit breaker for resilience
- Crash dump sanitization
- Compliance auditing

Example:
    >>> from opaque import OpaqueLogger, Validators
    >>> OpaqueLogger.setup_defaults(
    ...     rules=[Validators.BR.CPF, Validators.BR.CNPJ],
    ...     obfuscation_method="HASH"
    ... )
    >>> import logging
    >>> logging.setLoggerClass(OpaqueLogger)
    >>> logger = logging.getLogger("app")
    >>> logger.info("User CPF: 529.982.247-25")
    # Output: User CPF: [HASH-3A4C]
"""

__version__ = "0.1.0"
__author__ = "OPAQUE Security Team"
__license__ = "MIT"

from .core import OpaqueLogger, OpaqueScanner
from .validators import Validators
from .vault import Vault
from .crash_handler import install_crash_handler
from .audit import AuditScanner

__all__ = [
    "OpaqueLogger",
    "OpaqueScanner", 
    "Validators",
    "Vault",
    "install_crash_handler",
    "AuditScanner",
]

"""
Structlog Integration for OPAQUE
=================================

Provides a processor for structlog that automatically sanitizes sensitive data.

Example:
    import structlog
    from opaque.integrations.structlog_integration import OpaqueStructlogProcessor
    from opaque import Validators
    
    structlog.configure(
        processors=[
            OpaqueStructlogProcessor(rules=[Validators.BR.CPF, Validators.FINANCE.CREDIT_CARD]),
            structlog.processors.JSONRenderer()
        ]
    )
    
    logger = structlog.get_logger()
    logger.info("payment", cpf="529.982.247-25", amount=100.0)
    # Output: {"event": "payment", "cpf": "[HASH-3A4C]", "amount": 100.0}
"""

from typing import Any, Dict, List, Optional
from ..validators import Validator
from ..core import OpaqueScanner


class OpaqueStructlogProcessor:
    """Structlog processor that sanitizes sensitive data using OPAQUE."""
    
    def __init__(
        self,
        rules: List[Validator],
        obfuscation_method: str = "HASH",
        vault_key: Optional[str] = None,
        honeytokens: Optional[List[str]] = None
    ):
        """
        Initialize the Structlog processor.
        
        Args:
            rules: List of OPAQUE validators to apply
            obfuscation_method: Method to use (HASH, VAULT, ANONYMIZE)
            vault_key: Key for vault encryption (if using VAULT mode)
            honeytokens: List of honeytoken values to detect
        """
        self.scanner = OpaqueScanner(
            rules=rules,
            obfuscation_method=obfuscation_method,
            vault_key=vault_key,
            honeytokens=honeytokens or []
        )
    
    def __call__(self, logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a log event, sanitizing all string values.
        
        Args:
            logger: The logger instance
            method_name: The name of the method called
            event_dict: The event dictionary
            
        Returns:
            Sanitized event dictionary
        """
        return self.scanner.process_structure(event_dict)


def configure_structlog(
    rules: List[Validator],
    obfuscation_method: str = "HASH",
    vault_key: Optional[str] = None,
    **kwargs
):
    """
    Helper function to configure structlog with OPAQUE.
    
    Args:
        rules: List of OPAQUE validators
        obfuscation_method: Obfuscation method
        vault_key: Vault key (if applicable)
        **kwargs: Additional structlog configuration
    """
    try:
        import structlog
    except ImportError:
        raise ImportError(
            "structlog is not installed. Install it with: pip install structlog"
        )
    
    processors = kwargs.get('processors', [])
    processors.insert(0, OpaqueStructlogProcessor(rules, obfuscation_method, vault_key))
    kwargs['processors'] = processors
    
    structlog.configure(**kwargs)

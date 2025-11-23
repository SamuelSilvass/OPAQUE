"""
Sentry Integration for OPAQUE
==============================

Provides integration with Sentry to automatically sanitize sensitive data in error reports.

Example:
    import sentry_sdk
    from opaque.integrations.sentry_integration import OpaqueSentryIntegration
    from opaque import Validators
    
    sentry_sdk.init(
        dsn="your-dsn",
        integrations=[
            OpaqueSentryIntegration(
                rules=[Validators.BR.CPF, Validators.FINANCE.CREDIT_CARD]
            )
        ]
    )
    
    # Now all errors sent to Sentry will have PII sanitized
    cpf = "529.982.247-25"
    raise ValueError(f"Error with CPF: {cpf}")
    # Sentry receives: ValueError: Error with CPF: [HASH-3A4C]
"""

from typing import Any, Dict, List, Optional
from ..validators import Validator
from ..core import OpaqueScanner


class OpaqueSentryIntegration:
    """Sentry integration that sanitizes sensitive data in error reports."""
    
    identifier = "opaque"
    
    def __init__(
        self,
        rules: List[Validator],
        obfuscation_method: str = "HASH",
        vault_key: Optional[str] = None,
        honeytokens: Optional[List[str]] = None
    ):
        """
        Initialize the Sentry integration.
        
        Args:
            rules: List of OPAQUE validators
            obfuscation_method: Method to use (HASH, VAULT, ANONYMIZE)
            vault_key: Key for vault encryption
            honeytokens: List of honeytoken values
        """
        self.scanner = OpaqueScanner(
            rules=rules,
            obfuscation_method=obfuscation_method,
            vault_key=vault_key,
            honeytokens=honeytokens or []
        )
    
    @staticmethod
    def setup_once():
        """Called once when Sentry SDK is initialized."""
        pass
    
    def __call__(self, event: Dict[str, Any], hint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a Sentry event before sending.
        
        Args:
            event: The Sentry event dictionary
            hint: Additional context
            
        Returns:
            Sanitized event dictionary
        """
        # Sanitize exception messages
        if 'exception' in event and 'values' in event['exception']:
            for exc in event['exception']['values']:
                if 'value' in exc:
                    exc['value'] = self.scanner.sanitize(exc['value'])
        
        # Sanitize breadcrumbs
        if 'breadcrumbs' in event and 'values' in event['breadcrumbs']:
            for crumb in event['breadcrumbs']['values']:
                if 'message' in crumb:
                    crumb['message'] = self.scanner.sanitize(crumb['message'])
                if 'data' in crumb:
                    crumb['data'] = self.scanner.process_structure(crumb['data'])
        
        # Sanitize extra context
        if 'extra' in event:
            event['extra'] = self.scanner.process_structure(event['extra'])
        
        # Sanitize request data
        if 'request' in event:
            if 'data' in event['request']:
                event['request']['data'] = self.scanner.process_structure(event['request']['data'])
            if 'query_string' in event['request']:
                event['request']['query_string'] = self.scanner.sanitize(event['request']['query_string'])
        
        return event


def configure_sentry(
    dsn: str,
    rules: List[Validator],
    obfuscation_method: str = "HASH",
    vault_key: Optional[str] = None,
    **sentry_kwargs
):
    """
    Helper function to configure Sentry with OPAQUE.
    
    Args:
        dsn: Sentry DSN
        rules: List of OPAQUE validators
        obfuscation_method: Obfuscation method
        vault_key: Vault key (if applicable)
        **sentry_kwargs: Additional Sentry configuration
    """
    try:
        import sentry_sdk
    except ImportError:
        raise ImportError(
            "sentry-sdk is not installed. Install it with: pip install sentry-sdk"
        )
    
    integrations = sentry_kwargs.get('integrations', [])
    integrations.append(OpaqueSentryIntegration(rules, obfuscation_method, vault_key))
    sentry_kwargs['integrations'] = integrations
    
    sentry_sdk.init(dsn=dsn, before_send=integrations[-1], **sentry_kwargs)

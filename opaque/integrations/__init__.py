"""
OPAQUE Integrations Module
===========================

This module provides seamless integration with popular Python libraries for logging,
security, compliance, and data validation.

Available Integrations:
- Structlog: Structured logging with OPAQUE sanitization
- Loguru: Modern logging with automatic PII detection
- Pydantic: Data validation with built-in OPAQUE validators
- Sentry: Error tracking with sanitized tracebacks
- OpenTelemetry: Observability with PII protection
- Presidio: Microsoft's PII detection (bridge mode)
"""

from typing import TYPE_CHECKING

# Lazy imports to avoid hard dependencies
if TYPE_CHECKING:
    from .structlog_integration import OpaqueStructlogProcessor
    from .loguru_integration import OpaqueLoguruSink
    from .pydantic_integration import OpaqueValidator
    from .sentry_integration import OpaqueSentryIntegration
    from .presidio_integration import OpaquePresidioAnalyzer

__all__ = [
    'OpaqueStructlogProcessor',
    'OpaqueLoguruSink',
    'OpaqueValidator',
    'OpaqueSentryIntegration',
    'OpaquePresidioAnalyzer',
]

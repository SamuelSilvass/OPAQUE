"""
Integration Tests for OPAQUE v1.1.3
====================================

Tests all integrations with popular libraries to ensure seamless communication.
"""

import pytest
from opaque import Validators


# ==================== STRUCTLOG TESTS ====================

def test_structlog_processor():
    """Test Structlog integration with OPAQUE sanitization."""
    try:
        import structlog
        from opaque.integrations.structlog_integration import OpaqueStructlogProcessor
    except ImportError:
        pytest.skip("structlog not installed")
    
    processor = OpaqueStructlogProcessor(rules=[Validators.BR.CPF])
    
    event_dict = {
        "event": "user_login",
        "cpf": "529.982.247-25",
        "username": "joao"
    }
    
    result = processor(None, "info", event_dict)
    
    assert "529.982.247-25" not in str(result)
    assert result["username"] == "joao"  # Non-sensitive data preserved
    assert "[HASH-" in result["cpf"]


def test_structlog_configure_helper():
    """Test the configure_structlog helper function."""
    try:
        from opaque.integrations.structlog_integration import configure_structlog
        import structlog
    except ImportError:
        pytest.skip("structlog not installed")
    
    configure_structlog(
        rules=[Validators.BR.CPF],
        processors=[structlog.processors.JSONRenderer()]
    )
    
    # Verify configuration was applied
    assert structlog.is_configured()


# ==================== LOGURU TESTS ====================

def test_loguru_sink():
    """Test Loguru sink with OPAQUE sanitization."""
    try:
        from opaque.integrations.loguru_integration import OpaqueLoguruSink
        from io import StringIO
    except ImportError:
        pytest.skip("loguru not installed")
    
    output = StringIO()
    sink = OpaqueLoguruSink(
        rules=[Validators.BR.CPF],
        output=output
    )
    
    sink.write("User CPF: 529.982.247-25")
    
    result = output.getvalue()
    assert "529.982.247-25" not in result
    assert "[HASH-" in result


# ==================== PYDANTIC TESTS ====================

def test_pydantic_validator():
    """Test Pydantic integration with OPAQUE validators."""
    try:
        from pydantic import BaseModel, field_validator, ValidationError
        from opaque.integrations.pydantic_integration import opaque_validator
    except ImportError:
        pytest.skip("pydantic not installed")
    
    class User(BaseModel):
        name: str
        cpf: str
        
        @field_validator('cpf')
        @classmethod
        def validate_cpf(cls, v):
            return opaque_validator(v, Validators.BR.CPF)
    
    # Valid CPF
    user = User(name="João", cpf="529.982.247-25")
    assert user.cpf == "529.982.247-25"
    
    # Invalid CPF
    with pytest.raises(ValidationError):
        User(name="João", cpf="111.222.333-44")


def test_pydantic_mixin():
    """Test OpaqueValidatorMixin for Pydantic models."""
    try:
        from pydantic import BaseModel, field_validator
        from opaque.integrations.pydantic_integration import OpaqueValidatorMixin
    except ImportError:
        pytest.skip("pydantic not installed")
    
    class User(BaseModel, OpaqueValidatorMixin):
        cpf: str
        
        @field_validator('cpf')
        @classmethod
        def validate_cpf(cls, v):
            return cls.opaque_validate(v, Validators.BR.CPF)
    
    user = User(cpf="529.982.247-25")
    assert user.cpf == "529.982.247-25"


# ==================== SENTRY TESTS ====================

def test_sentry_integration():
    """Test Sentry integration sanitizes error data."""
    from opaque.integrations.sentry_integration import OpaqueSentryIntegration
    
    integration = OpaqueSentryIntegration(rules=[Validators.BR.CPF])
    
    event = {
        "exception": {
            "values": [{
                "value": "Error with CPF: 529.982.247-25"
            }]
        },
        "extra": {
            "user_cpf": "529.982.247-25"
        }
    }
    
    sanitized = integration(event, {})
    
    assert "529.982.247-25" not in str(sanitized)
    assert "[HASH-" in sanitized["exception"]["values"][0]["value"]


# ==================== PRESIDIO TESTS ====================

def test_presidio_analyzer():
    """Test Presidio integration with OPAQUE validators."""
    from opaque.integrations.presidio_integration import OpaquePresidioAnalyzer
    
    analyzer = OpaquePresidioAnalyzer(
        opaque_rules=[Validators.BR.CPF],
        use_presidio=False  # Don't require Presidio installation
    )
    
    text = "User CPF: 529.982.247-25"
    results = analyzer.analyze(text)
    
    assert len(results) > 0
    assert results[0]["entity_type"] == "CPF"
    assert results[0]["score"] == 1.0  # Mathematical validation = 100% confidence


def test_presidio_anonymize():
    """Test Presidio-style anonymization using OPAQUE."""
    from opaque.integrations.presidio_integration import OpaquePresidioAnalyzer
    
    analyzer = OpaquePresidioAnalyzer(
        opaque_rules=[Validators.BR.CPF],
        use_presidio=False
    )
    
    text = "User CPF: 529.982.247-25"
    anonymized = analyzer.anonymize(text)
    
    assert "529.982.247-25" not in anonymized
    assert "[HASH-" in anonymized


# ==================== CROSS-INTEGRATION TESTS ====================

def test_multiple_integrations_together():
    """Test that multiple integrations can work together."""
    from opaque.integrations.sentry_integration import OpaqueSentryIntegration
    from opaque.integrations.presidio_integration import OpaquePresidioAnalyzer
    
    # Both should use the same validators
    rules = [Validators.BR.CPF]
    
    sentry_int = OpaqueSentryIntegration(rules=rules)
    presidio_analyzer = OpaquePresidioAnalyzer(opaque_rules=rules, use_presidio=False)
    
    text = "CPF: 529.982.247-25"
    
    # Presidio should detect CPF
    results = presidio_analyzer.analyze(text)
    assert len(results) >= 1
    
    # Sentry should sanitize CPF
    event = {"exception": {"values": [{"value": text}]}}
    sanitized = sentry_int(event, {})
    assert "529.982.247-25" not in str(sanitized)

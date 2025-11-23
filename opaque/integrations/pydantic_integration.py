"""
Pydantic Integration for OPAQUE
================================

Provides custom validators for Pydantic models using OPAQUE's mathematical validation.

Example:
    from pydantic import BaseModel, field_validator
    from opaque.integrations.pydantic_integration import opaque_validator
    from opaque import Validators
    
    class User(BaseModel):
        name: str
        cpf: str
        
        @field_validator('cpf')
        @classmethod
        def validate_cpf(cls, v):
            return opaque_validator(v, Validators.BR.CPF)
    
    user = User(name="João", cpf="529.982.247-25")  # Valid
    user = User(name="João", cpf="111.222.333-44")  # Raises ValidationError
"""

from typing import Any, Type
from ..validators import Validator


def opaque_validator(value: Any, validator_class: Type[Validator]) -> Any:
    """
    Validate a value using an OPAQUE validator.
    
    Args:
        value: The value to validate
        validator_class: The OPAQUE validator class to use
        
    Returns:
        The original value if valid
        
    Raises:
        ValueError: If validation fails
    """
    if not isinstance(value, str):
        value = str(value)
    
    if not validator_class.validate(value):
        raise ValueError(
            f"Invalid {validator_class.__name__.replace('Validator', '')}: {value}"
        )
    
    return value


class OpaqueValidatorMixin:
    """
    Mixin for Pydantic models to add OPAQUE validation helpers.
    
    Example:
        class User(BaseModel, OpaqueValidatorMixin):
            cpf: str
            
            @field_validator('cpf')
            @classmethod
            def validate_cpf(cls, v):
                return cls.opaque_validate(v, Validators.BR.CPF)
    """
    
    @classmethod
    def opaque_validate(cls, value: Any, validator_class: Type[Validator]) -> Any:
        """Validate using OPAQUE validator."""
        return opaque_validator(value, validator_class)


def create_opaque_field_validator(validator_class: Type[Validator]):
    """
    Factory function to create a Pydantic field validator from an OPAQUE validator.
    
    Args:
        validator_class: The OPAQUE validator class
        
    Returns:
        A function that can be used as a Pydantic field_validator
        
    Example:
        from pydantic import BaseModel, field_validator
        from opaque import Validators
        from opaque.integrations.pydantic_integration import create_opaque_field_validator
        
        cpf_validator = create_opaque_field_validator(Validators.BR.CPF)
        
        class User(BaseModel):
            cpf: str
            
            validate_cpf = field_validator('cpf')(cpf_validator)
    """
    def validator_func(cls, v):
        return opaque_validator(v, validator_class)
    
    validator_func.__name__ = f"validate_{validator_class.__name__.lower()}"
    return classmethod(validator_func)

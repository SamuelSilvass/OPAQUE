# 🎓 OPAQUE Complete Tutorial - From Zero to Hero

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Concepts](#basic-concepts)
4. [Hands-On Examples](#hands-on-examples)
5. [Advanced Features](#advanced-features)
6. [Real-World Use Cases](#real-world-use-cases)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

Welcome to the complete OPAQUE tutorial! This guide will take you from absolute beginner to advanced user, teaching you everything you need to know about data validation and masking.

### What is OPAQUE?

OPAQUE is a **deterministic data masking engine** that uses **mathematical validation** instead of AI guessing. This means:

- ✅ **Zero false positives** - Every match is mathematically proven
- ✅ **Ultra-fast** - Pure mathematics, no GPU needed
- ✅ **Reversible** - Debug production issues safely
- ✅ **Comprehensive** - 77+ validators for global coverage

### Why Mathematical Validation?

Traditional AI-based solutions **guess** if something is sensitive data. OPAQUE **proves** it mathematically.

**Example: Brazilian CPF Validation**

```
CPF: 529.982.247-25

Step 1: Extract digits → [5,2,9,9,8,2,2,4,7,2,5]
Step 2: Calculate first check digit using Mod 11
Step 3: Calculate second check digit using Mod 11
Step 4: Compare with provided digits
Result: ✓ VALID (mathematically proven)
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

```bash
pip install opaque-logger
```

### Development Install

```bash
# Clone the repository
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev]"
```

### Verify Installation

```bash
python -c "from opaque import Validators; print('OPAQUE installed successfully!')"
```

---

## Basic Concepts

### 1. Validators

Validators are classes that check if data is valid according to mathematical rules.

```python
from opaque import Validators

# Check if a CPF is valid
is_valid = Validators.BR.CPF.validate("529.982.247-25")
print(is_valid)  # True

# Check if an email is valid
is_valid = Validators.INTERNATIONAL.EMAIL.validate("user@example.com")
print(is_valid)  # True
```

### 2. OpaqueLogger

OpaqueLogger automatically sanitizes sensitive data in your logs.

```python
import logging
from opaque import OpaqueLogger, Validators

# Configure OPAQUE
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="HASH"
)

# Use it like normal logging
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("myapp")

logger.info("User CPF: 529.982.247-25")
# Output: User CPF: [HASH-3A4C]
```

### 3. Obfuscation Methods

OPAQUE offers three ways to hide sensitive data:

| Method | Description | Use Case |
|--------|-------------|----------|
| **HASH** | One-way hash (default) | Production logs |
| **MASK** | Replace with asterisks | User interfaces |
| **VAULT** | Reversible encryption | Debugging |

---

## Hands-On Examples

### Example 1: Basic CPF Validation

```python
from opaque import Validators

# Valid CPF
cpf = "529.982.247-25"
if Validators.BR.CPF.validate(cpf):
    print(f"✓ {cpf} is valid!")
else:
    print(f"✗ {cpf} is invalid!")

# Invalid CPF
cpf = "111.222.333-44"
if Validators.BR.CPF.validate(cpf):
    print(f"✓ {cpf} is valid!")
else:
    print(f"✗ {cpf} is invalid!")
```

**Output:**
```
✓ 529.982.247-25 is valid!
✗ 111.222.333-44 is invalid!
```

### Example 2: Logging with Auto-Sanitization

```python
import logging
from opaque import OpaqueLogger, Validators

# Setup
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,
        Validators.FINANCE.CREDIT_CARD
    ],
    obfuscation_method="HASH"
)

logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("payment")

# Log sensitive data
logger.info("Processing payment for CPF 529.982.247-25")
logger.info("Card number: 4532-1488-0343-6467")

# Invalid data is preserved for debugging
logger.info("Invalid CPF: 111.222.333-44")
```

**Output:**
```
INFO - Processing payment for CPF [HASH-3A4C]
INFO - Card number: [HASH-7B9E]
INFO - Invalid CPF: 111.222.333-44
```

### Example 3: Vault Mode (Reversible)

```python
import os
from opaque import OpaqueLogger, Validators

# Set master key
os.environ["OPAQUE_MASTER_KEY"] = "my-secret-key-2024"

# Configure Vault mode
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="my-secret-key-2024"
)

logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("secure")

logger.info("User CPF: 529.982.247-25")
# Output: User CPF: [VAULT:gAAAAABl...]

# Later, decrypt using CLI:
# python -m opaque.cli reveal "[VAULT:gAAAAABl...]" --key=my-secret-key-2024
```

### Example 4: Multi-Country Validation

```python
from opaque import OpaqueLogger, Validators

# Configure for multiple countries
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,      # Brazil
        Validators.AR.DNI,      # Argentina
        Validators.CL.RUT,      # Chile
        Validators.CO.CEDULA,   # Colombia
        Validators.PE.DNI,      # Peru
    ]
)

logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("latam")

# All will be sanitized
logger.info("BR CPF: 529.982.247-25")
logger.info("AR DNI: 12345678")
logger.info("CL RUT: 12.345.678-5")
```

### Example 5: Honeytokens (Intrusion Detection)

```python
from opaque import OpaqueLogger, Validators

# Configure with honeytoken
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # Fake CPF as bait
)

logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("security")

# Normal CPF - sanitized
logger.info("User CPF: 529.982.247-25")

# Honeytoken - ALERT!
logger.info("Accessing CPF: 999.888.777-66")
# Stderr: 🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED
```

---

## Advanced Features

### 1. Custom Validators

Create your own validators:

```python
from opaque.validators import Validator
import re

class MyCustomValidator(Validator):
    @staticmethod
    def validate(value: str) -> bool:
        # Your custom logic
        return bool(re.match(r'^CUSTOM-\d{6}$', value))

# Use it
is_valid = MyCustomValidator.validate("CUSTOM-123456")
print(is_valid)  # True
```

### 2. CLI Tools

OPAQUE includes powerful command-line tools:

```bash
# Validate a document
python -m opaque.cli validate BR.CPF "529.982.247-25"

# Interactive mode
python -m opaque.cli interactive

# Analyze files for secrets
python -m opaque.cli analyze config.json

# Visual demo
python -m opaque.cli demo

# Performance benchmark
python -m opaque.cli benchmark
```

### 3. FastAPI Integration

```python
from fastapi import FastAPI
from opaque.middleware import OpaqueFastAPIMiddleware
from opaque import OpaqueLogger, Validators

app = FastAPI()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)

app.add_middleware(OpaqueFastAPIMiddleware, logger=OpaqueLogger("api"))

@app.post("/payment")
async def process_payment(cpf: str, amount: float):
    # CPF automatically sanitized in logs
    return {"status": "success"}
```

---

## Real-World Use Cases

### Use Case 1: E-commerce Platform

**Challenge:** Protect customer data in logs while maintaining debuggability.

**Solution:**
```python
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,
        Validators.FINANCE.CREDIT_CARD,
        Validators.INTERNATIONAL.EMAIL
    ],
    obfuscation_method="VAULT",  # Reversible for debugging
    vault_key=os.environ["VAULT_KEY"]
)
```

### Use Case 2: Healthcare System

**Challenge:** HIPAA/LGPD compliance for patient data.

**Solution:**
```python
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,
        Validators.BR.CNS,  # Health card
        Validators.INTERNATIONAL.EMAIL
    ],
    obfuscation_method="HASH",  # Irreversible for security
    honeytokens=["000.000.000-00"]  # Detect data breaches
)
```

### Use Case 3: Financial Institution

**Challenge:** PCI-DSS compliance for credit card data.

**Solution:**
```python
OpaqueLogger.setup_defaults(
    rules=[
        Validators.FINANCE.CREDIT_CARD,
        Validators.FINANCE.IBAN,
        Validators.BR.CPF,
        Validators.BR.CNPJ
    ],
    obfuscation_method="HASH",
    circuit_breaker_threshold=1000  # Prevent log flooding
)
```

---

## Best Practices

### 1. Always Use Vault Mode in Development

```python
import os

# Development
if os.environ.get("ENV") == "development":
    obfuscation_method = "VAULT"
    vault_key = "dev-key-123"
# Production
else:
    obfuscation_method = "HASH"
    vault_key = None
```

### 2. Use Honeytokens for Security

```python
# Add fake data as honeytokens
honeytokens = [
    "999.999.999-99",  # Fake CPF
    "0000-0000-0000-0000",  # Fake card
    "admin@honeypot.com"  # Fake email
]
```

### 3. Test Your Validators

```python
# Always test before deploying
assert Validators.BR.CPF.validate("529.982.247-25") == True
assert Validators.BR.CPF.validate("111.222.333-44") == False
```

### 4. Use Multiple Validators

```python
# Protect all sensitive data types
rules = [
    Validators.BR.CPF,
    Validators.BR.CNPJ,
    Validators.FINANCE.CREDIT_CARD,
    Validators.INTERNATIONAL.EMAIL,
    Validators.INTERNATIONAL.PHONE
]
```

---

## Troubleshooting

### Problem: "No module named 'opaque'"

**Solution:**
```bash
pip install opaque-logger
```

### Problem: "Validator not found"

**Solution:** Check available validators:
```bash
python -m opaque.cli list-validators
```

### Problem: "Vault decryption failed"

**Solution:** Ensure you're using the correct master key:
```bash
python -m opaque.cli reveal "[VAULT:...]" --key=correct-key
```

### Problem: "Performance is slow"

**Solution:** Check circuit breaker settings:
```python
OpaqueLogger.setup_defaults(
    rules=[...],
    circuit_breaker_threshold=5000  # Increase threshold
)
```

---

## Next Steps

1. **Try the Visual Tester:**
   ```bash
   python examples/visual_tester.py
   ```

2. **Run the Examples:**
   ```bash
   python examples/example_01_basic.py
   python examples/example_02_vault.py
   ```

3. **Read the API Reference:**
   - [Complete API Documentation](../docs/API_REFERENCE.md)

4. **Join the Community:**
   - [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
   - [Contributing Guide](../CONTRIBUTING.md)

---

## Conclusion

You now have everything you need to use OPAQUE effectively! Remember:

- ✅ Use **mathematical validation** for zero false positives
- ✅ Choose the right **obfuscation method** for your use case
- ✅ Add **honeytokens** for security monitoring
- ✅ Test everything before deploying to production

**Happy validating!** 🛡️

---

*Built with precision by Samuel Silva*  
*Protecting data with mathematics, not magic* ✨

# OPAQUE 🛡️

**The Deterministic Data Masking Engine for High-Stakes Engineering.**

> "Don't guess if it's a CPF. Prove it mathematically."

[![Tests](https://img.shields.io/badge/tests-24%20passed-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

OPAQUE is a high-performance, context-aware sanitization library designed for enterprise environments where data integrity and performance are non-negotiable. Unlike AI-based solutions that guess, OPAQUE validates.

## 🚀 Why OPAQUE?

*   **Rust-Powered Core**: Built for speed. Process gigabytes of logs without slowing down your application.
*   **Deterministic Validation**: We calculate the Check Digit (Mod 11, Luhn). If the math doesn't add up, we don't touch your data. No more false positives.
*   **Secure Fingerprinting**: Instead of `***`, we use salted SHA256 hashes (e.g., `[HASH-XF92]`). Track errors across logs without revealing user identity.
*   **Zero-Config Integration**: Drop-in replacement for Python's standard `logging`.
*   **Vault Mode**: Reversible AES-256 encryption for debugging without exposing data.
*   **Honeytokens**: Detect intrusion attempts with bait data.
*   **Circuit Breaker**: Prevents log flooding from crashing your server.

## 🧪 Testing

OPAQUE comes with a comprehensive test suite ensuring mathematical precision.

```bash
pip install pytest
pytest
```

**Test Coverage:**
- ✅ 24 test cases covering all validators
- ✅ Vault encryption/decryption
- ✅ Honeytoken detection
- ✅ Circuit breaker activation
- ✅ Crash handler sanitization

## 📦 Installation

```bash
pip install opaque-logger
```

*(Requires Rust toolchain for high-performance extensions, falls back to pure Python if unavailable)*

## ⚡ Quick Start

### Basic Usage

```python
import logging
from opaque import OpaqueLogger, Validators

# 1. Configure
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ, Validators.FINANCE.CREDIT_CARD],
    obfuscation_method="HASH"
)

# 2. Integrate
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("payments")

# 3. Log Securely
payload = {
    "user": "Alice",
    "cpf": "529.982.247-25",  # Valid -> [HASH-3A4C]
    "note": "Typo in 111.222.333-44" # Invalid -> Kept as is
}

logger.error(payload)
```

**Output:**
```json
{
  "user": "Alice",
  "cpf": "[HASH-3A4C]",
  "note": "Typo in 111.222.333-44"
}
```

### Vault Mode (Reversible Encryption)

```python
import os
os.environ["OPAQUE_MASTER_KEY"] = "your-secret-key-here"

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="your-secret-key-here"
)

logger = logging.getLogger("secure")
logger.info("Processing CPF 529.982.247-25")
# Output: Processing CPF [VAULT:gAAAAABl...]
```

**Reveal encrypted data:**
```bash
python -m opaque.cli reveal "[VAULT:gAAAAABl...]" --key=your-secret-key-here
# Output: 🔓 REVEALED DATA: 529.982.247-25
```

### Honeytokens (Intrusion Detection)

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # Bait CPF
)

logger = logging.getLogger("security")
logger.info("Access attempt with CPF 999.888.777-66")
# Stderr: 🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: 999.888.777-66
# Output: Access attempt with CPF [HONEYTOKEN TRIGGERED]
```

### Crash Dump Sanitization

```python
from opaque import install_crash_handler, OpaqueLogger, Validators

# Setup
OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
install_crash_handler()

# Now all crashes will have sanitized tracebacks
password = "super_secret"
cpf = "529.982.247-25"
raise ValueError(f"Error processing {cpf}")
# Traceback will show: ValueError: Error processing [HASH-3A4C]
# Locals will show: password = [REDACTED_SECRET_KEY]
```

### Compliance Scanning

```bash
python -m opaque.cli scan ./src --output=compliance_report.html
```

**Output:**
```
🔍 Scanning directory: ./src...
✅ Report generated: compliance_report.html
🛡️ Security Score: 98%
```

## 🛠️ Architecture

OPAQUE follows the **Architecture of Elite**:

1.  **Core**: Rust + PyO3 for bare-metal performance (falls back to optimized Python).
2.  **C.A.R.E.**: Context-Aware Regex Engine with Sliding Window analysis.
3.  **Fingerprinting**: Deterministic hashing for debuggability.
4.  **Vault**: Military-grade AES-256 encryption.
5.  **Circuit Breaker**: Resilience against log flooding.

## 🇧🇷 Supported Validators

### Brazil
*   **CPF**: Validates using Mod 11 algorithm
*   **CNPJ**: Validates using weighted Mod 11
*   **Pix**: Email, Phone (+55), UUID formats

### Finance
*   **Credit Cards**: Validates using Luhn algorithm (Visa, Mastercard, Amex, etc.)

### Coming Soon
*   CNH (Driver's License)
*   Renavam (Vehicle Registration)
*   Mercosul License Plates

## 📚 Advanced Examples

### Custom Validator

```python
from opaque.validators import Validator
import re

class EmailValidator(Validator):
    @staticmethod
    def validate(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

# Use it
OpaqueLogger.setup_defaults(
    rules=[EmailValidator]
)
```

### FastAPI Middleware

```python
from fastapi import FastAPI
from opaque.middleware import OpaqueFastAPIMiddleware
from opaque import OpaqueLogger, Validators

app = FastAPI()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)

# Middleware will sanitize all request/response data
app.add_middleware(OpaqueFastAPIMiddleware, logger=OpaqueLogger("api"))
```

### Django Integration

```python
# settings.py
MIDDLEWARE = [
    'opaque.middleware.OpaqueDjangoMiddleware',
    # ... other middleware
]

# Configure in apps.py or __init__.py
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)
```

## 🔧 Configuration Options

### OpaqueLogger.setup_defaults()

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rules` | `List[Validator]` | `[]` | List of validator classes to use |
| `obfuscation_method` | `str` | `"HASH"` | `"HASH"`, `"MASK"` (***), or `"VAULT"` |
| `vault_key` | `str` | `None` | Master key for Vault mode encryption |
| `honeytokens` | `List[str]` | `[]` | List of bait values to detect intrusion |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPAQUE_MASTER_KEY` | Default master key for Vault mode |
| `OPAQUE_SALT` | Salt for hash fingerprinting |

## 🧪 Testing Your Integration

### Test 1: Basic Sanitization

```python
import logging
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("test")

# Test valid CPF
logger.info("CPF: 529.982.247-25")
# Expected: CPF: [HASH-XXXX]

# Test invalid CPF
logger.info("CPF: 111.222.333-44")
# Expected: CPF: 111.222.333-44 (unchanged)
```

### Test 2: Vault Encryption

```python
from opaque import Vault

vault = Vault(key="test-key-123")
encrypted = vault.encrypt("sensitive-data")
print(encrypted)  # [VAULT:gAAAA...]

decrypted = vault.decrypt(encrypted)
assert decrypted == "sensitive-data"
```

### Test 3: Honeytoken Detection

```python
import sys
from io import StringIO
from opaque import OpaqueLogger, Validators

# Capture stderr
old_stderr = sys.stderr
sys.stderr = StringIO()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]
)

logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("test")
logger.info("Access: 999.888.777-66")

stderr_output = sys.stderr.getvalue()
sys.stderr = old_stderr

assert "HONEYTOKEN DETECTED" in stderr_output
```

## 🐛 Troubleshooting

### Issue: "No module named 'opaque'"
**Solution:** Ensure installation completed successfully:
```bash
pip install --upgrade opaque-logger
```

### Issue: Vault decryption fails
**Solution:** Ensure you're using the same key for encryption and decryption:
```python
# Wrong
vault1 = Vault(key="key1")
encrypted = vault1.encrypt("data")
vault2 = Vault(key="key2")
vault2.decrypt(encrypted)  # Will fail

# Correct
vault = Vault(key="key1")
encrypted = vault.encrypt("data")
decrypted = vault.decrypt(encrypted)  # Works
```

### Issue: Circuit breaker activating too often
**Solution:** Adjust threshold in scanner:
```python
from opaque.core import OpaqueScanner
scanner = OpaqueScanner(rules=[...])
scanner.CIRCUIT_THRESHOLD = 5000  # Increase from default 1000
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

*   **Documentation**: [Full Docs](https://github.com/SamuelSilvass/OPAQUE)
*   **Issues**: [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
*   **PyPI**: [opaque-logger](https://pypi.org/project/opaque-logger)

---

*Built with precision by the OPAQUE Security Team.*

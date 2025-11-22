# OPAQUE 🛡️

**The Deterministic Data Masking Engine for High-Stakes Engineering.**

> "Don't guess if it's a CPF. Prove it mathematically."

[![Tests](https://img.shields.io/badge/tests-24%20passed-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

[English](docs/README_EN.md) | [Português](docs/README_PT.md) | [Español](docs/README_ES.md)

OPAQUE is a high-performance, context-aware sanitization library designed for enterprise environments where data integrity and performance are non-negotiable. Unlike AI-based solutions that guess, OPAQUE validates mathematically.

## 🚀 Key Features

*   **Rust-Powered Core**: Process gigabytes of logs without slowing down your application
*   **Deterministic Validation**: Mathematical validation (Mod 11, Luhn) - no false positives
*   **Secure Fingerprinting**: SHA256 hashes instead of `***` for debuggability
*   **Vault Mode**: Reversible AES-256 encryption for authorized debugging
*   **Honeytokens**: Detect intrusion attempts with bait data
*   **Circuit Breaker**: Prevents log flooding from crashing your server
*   **Crash Handler**: Sanitizes tracebacks and local variables
*   **Compliance Auditing**: Static analysis and HTML reports

## 📦 Quick Install

```bash
pip install opaque-logger
```

## ⚡ Quick Start

```python
import logging
from opaque import OpaqueLogger, Validators

# Configure
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ],
    obfuscation_method="HASH"
)

# Integrate
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("app")

# Log securely
logger.info("User CPF: 529.982.247-25")
# Output: User CPF: [HASH-3A4C]
```

## 📚 Documentation

*   **[English Documentation](docs/README_EN.md)** - Complete guide with all features
*   **[Documentação em Português](docs/README_PT.md)** - Guia completo em português
*   **[Documentación en Español](docs/README_ES.md)** - Guía completa en español

## 🧪 Examples

Run the included examples to see OPAQUE in action:

```bash
# Set Python path
export PYTHONPATH="$(pwd)"  # Linux/Mac
$env:PYTHONPATH = "$(pwd)"  # Windows PowerShell

# Run examples
python examples/example_01_basic.py          # Basic usage
python examples/example_02_vault.py          # Vault mode
python examples/example_03_honeytokens.py    # Intrusion detection
python examples/example_04_crash_handler.py  # Traceback sanitization
python examples/example_05_audit.py          # Compliance scanning
```

## 🧪 Testing

```bash
pip install pytest
pytest -v
```

**Test Results:** ✅ 24/24 tests passed

## 🇧🇷 Supported Validators

*   **CPF** - Brazilian individual taxpayer ID (Mod 11)
*   **CNPJ** - Brazilian company taxpayer ID (Weighted Mod 11)
*   **Pix** - Brazilian instant payment keys (Email, Phone, UUID)
*   **Credit Cards** - International cards (Luhn algorithm)

## 🛠️ Advanced Features

### Vault Mode
```python
OpaqueLogger.setup_defaults(
    obfuscation_method="VAULT",
    vault_key="your-master-key"
)
```

### Honeytokens
```python
OpaqueLogger.setup_defaults(
    honeytokens=["999.888.777-66"]
)
```

### Compliance Scanning
```bash
python -m opaque.cli scan ./src --output=report.html
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🔗 Links

*   **Issues**: [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
*   **PyPI**: [opaque-logger](https://pypi.org/project/opaque-logger)

---

*Built with precision by the OPAQUE Security Team.*

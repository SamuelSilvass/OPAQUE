[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-opaque--logger-blue?style=for-the-badge&logo=pypi)](https://pypi.org/project/opaque-logger/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?style=for-the-badge)](https://github.com/SamuelSilvass/OPAQUE)

[🇺🇸 English](docs/README_EN.md) | [🇧🇷 Português](docs/README_PT.md) | [🇪🇸 Español](docs/README_ES.md)

---

<div align="center">

# 🛡️ OPAQUE v1.1.3

### **The only data masking library that uses MATH, not AI**

</div>

## 🎯 Why OPAQUE?

Unlike AI-based solutions that **guess**, OPAQUE **validates** using mathematical algorithms:

| Feature | AI Solutions | OPAQUE |
|---------|-------------|---------|
| **Validation** | Neural networks (guessing) | Mathematical algorithms (proof) |
| **False Positives** | Common | Zero |
| **Performance** | Slow (GPU required) | Ultra-fast (pure math) |
| **Debuggability** | Black box | Deterministic hashing |
| **Reversibility** | No | Yes (Vault Mode) |
| **Coverage** | Limited | 75+ validators globally |
| **Integrations** | Few | Structlog, Loguru, Pydantic, Sentry, Presidio |

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🔐 **Mathematical Validation**
- **Global**: 75+ validators across 5 continents.
- **Algorithms**: Verhoeff, ISO 7064, Luhn, Mod 11.
- **Zero False Positives**: Only mathematically valid data is masked.

</td>
<td width="50%">

### 🏦 **Vault Mode**
- AES-256 encryption
- Reversible for debugging
- CLI decryption tool
- Master key protection
- PBKDF2 key derivation

</td>
</tr>
<tr>
<td width="50%">

### 🍯 **Honeytokens**
- Intrusion detection
- Bait data alerts
- Real-time monitoring
- Security integration
- Automated alerts

</td>
<td width="50%">

### ⚡ **Circuit Breaker**
- Flood protection
- Auto-recovery
- Resource optimization
- Server stability
- Configurable thresholds

</td>
</tr>
</table>

## 🔌 Ecosystem Integrations (New in v1.1.3)

OPAQUE now integrates natively with your favorite tools:

<details>
<summary><b>🔹 Structlog</b></summary>

```python
import structlog
from opaque.integrations.structlog_integration import OpaqueStructlogProcessor
from opaque import Validators

structlog.configure(
    processors=[
        OpaqueStructlogProcessor(rules=[Validators.BR.CPF]),
        structlog.processors.JSONRenderer()
    ]
)
```
</details>

<details>
<summary><b>🔹 Loguru</b></summary>

```python
from loguru import logger
from opaque.integrations.loguru_integration import OpaqueLoguruSink
from opaque import Validators

# Add OPAQUE sink
sink = OpaqueLoguruSink(rules=[Validators.BR.CPF])
logger.add(sink)
```
</details>

<details>
<summary><b>🔹 Pydantic</b></summary>

```python
from pydantic import BaseModel, field_validator
from opaque.integrations.pydantic_integration import opaque_validator
from opaque import Validators

class User(BaseModel):
    cpf: str
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v):
        return opaque_validator(v, Validators.BR.CPF)
```
</details>

<details>
<summary><b>🔹 Sentry</b></summary>

```python
import sentry_sdk
from opaque.integrations.sentry_integration import OpaqueSentryIntegration

sentry_sdk.init(
    integrations=[
        OpaqueSentryIntegration(rules=[Validators.BR.CPF])
    ]
)
```
</details>

<details>
<summary><b>🔹 Microsoft Presidio</b></summary>

```python
from opaque.integrations.presidio_integration import OpaquePresidioAnalyzer

# Combine Presidio's NLP with OPAQUE's Math
analyzer = OpaquePresidioAnalyzer(opaque_rules=[Validators.BR.CPF])
results = analyzer.analyze("My CPF is 529.982.247-25")
```
</details>

## 🛡️ Enterprise Customization & Compliance

OPAQUE v1.1.1+ introduces powerful dependency injection to meet strict enterprise requirements:

### 💉 Dependency Injection
- **Custom Hash Functions**: Inject your own hashing algorithms (e.g., HMAC-SHA512, Argon2).
- **Custom Vaults**: Integrate with AWS Secrets Manager, HashiCorp Vault, or HSMs.
- **Custom Honeytoken Handlers**: Check honeytokens against Redis, Databases, or external APIs.

### ⚖️ LGPD & GDPR Compliance
We now provide explicit strategies for different compliance needs:

| Strategy | Class | Use Case | Reversible? | Compliance |
|----------|-------|----------|-------------|------------|
| **Anonymization** | `IrreversibleAnonymizer` | Debugging, Errors | ❌ No | ✅ Not Personal Data |
| **Pseudonymization** | `DeterministicPseudonymizer` | Audit Trails | ⚠️ Yes (with key) | ⚠️ Personal Data |

See our [Compliance Guide](docs/COMPLIANCE_GUIDE.md) for details.

## 🚀 Quick Start

### Installation

```bash
# Install with all integrations
pip install opaque-logger[all]

# Or specific ones
pip install opaque-logger[structlog,pydantic]
```

### Basic Usage

```python
import logging
from opaque import OpaqueLogger, Validators

# Configure
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,
        Validators.BR.CNPJ,
        Validators.FINANCE.CREDIT_CARD
    ],
    obfuscation_method="HASH"
)

# Integrate
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("app")

# Log securely
logger.info("User CPF: 529.982.247-25")
# Output: User CPF: [HASH-3A4C]

logger.info("Invalid CPF: 111.222.333-44")
# Output: Invalid CPF: 111.222.333-44 (preserved for debugging)
```

## 📊 Performance Benchmarks

```
Sanitization:     1,000+ messages/sec
CPF Validation:   65,000+ ops/sec
CNPJ Validation:  68,000+ ops/sec
Credit Card:      122,000+ ops/sec
Vault Encryption: 22,000+ ops/sec
Vault Decryption: 12,000+ ops/sec
```

## 🧪 Test Coverage

```bash
pytest -v
```

**Results:** ✅ **120+ tests passing** (100% success rate)

- ✅ All validators tested with valid and invalid data
- ✅ Vault encryption/decryption
- ✅ Honeytoken detection
- ✅ Circuit breaker activation
- ✅ Crash handler sanitization
- ✅ Middleware integration
- ✅ CLI tools
- ✅ **New: Integration tests (Structlog, Loguru, Sentry, Pydantic)**

## 📚 Examples

<details>
<summary><b>🔹 Vault Mode (Reversible Encryption)</b></summary>

```python
import os
from opaque import OpaqueLogger, Validators

# Set master key
os.environ["OPAQUE_MASTER_KEY"] = "your-master-key"

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="your-master-key"
)

logger = logging.getLogger("secure")
logger.info("Processing CPF 529.982.247-25")
# Output: Processing CPF [VAULT:gAAAAABl...]

# Decrypt later
python -m opaque.cli reveal "[VAULT:gAAAAABl...]" --key=your-master-key
# Output: 🔓 REVEALED DATA: 529.982.247-25
```

</details>

<details>
<summary><b>🔹 Honeytokens (Intrusion Detection)</b></summary>

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # Bait CPF
)

logger = logging.getLogger("security")
logger.info("Access with CPF 999.888.777-66")
# Stderr: 🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: 999.888.777-66
# Output: Access with CPF [HONEYTOKEN TRIGGERED]
```

</details>

<details>
<summary><b>🔹 Crash Handler (Traceback Sanitization)</b></summary>

```python
from opaque import install_crash_handler, OpaqueLogger, Validators

# Setup
OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
install_crash_handler()

# Now all crashes sanitize sensitive data
password = "secret123"
cpf = "529.982.247-25"
raise ValueError(f"Error: {cpf}")
# Traceback shows: ValueError: Error: [HASH-3A4C]
# Locals show: password = [REDACTED_SECRET_KEY]
```

</details>

<details>
<summary><b>🔹 Multi-Country Support</b></summary>

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
        Validators.FINANCE.CREDIT_CARD,  # International
    ]
)

logger = logging.getLogger("latam")
logger.info("BR CPF: 529.982.247-25")  # Sanitized
logger.info("CL RUT: 12.345.678-5")    # Sanitized
logger.info("Card: 4532-1488-0343-6467")  # Sanitized
```

</details>

<details>
<summary><b>🔹 Compliance Scanning</b></summary>

```bash
# Scan your codebase for sensitive data
python -m opaque.cli scan ./src --output=report.html

# Output:
# 🔍 Scanning directory: ./src...
# ✅ Report generated: report.html
# 🛡️ Security Score: 98%
# 
# Found:
# - 15 CPF instances
# - 8 CNPJ instances
# - 3 Credit Card instances
# 
# Recommendations:
# - Use OpaqueLogger in production
# - Enable Vault mode for debugging
# - Add honeytokens for intrusion detection
```

</details>

<details>
<summary><b>🔹 FastAPI Middleware</b></summary>

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

@app.post("/payment")
async def process_payment(cpf: str, amount: float):
    # CPF will be automatically sanitized in logs
    return {"status": "success"}
```

</details>

<details>
<summary><b>🔹 Django Integration</b></summary>

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

</details>

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   OPAQUE Engine                     │
├─────────────────────────────────────────────────────┤
│  1. Context-Aware Regex Pattern Matching           │
│  2. Mathematical Validation (Mod 11, Luhn, etc.)   │
│  3. Honeytoken Detection                            │
│  4. Circuit Breaker Check                           │
│  5. Obfuscation (Hash/Vault/Mask)                  │
│  6. Structured Data Processing (JSON/Dict/List)    │
└─────────────────────────────────────────────────────┘
```

### Processing Flow

```
Input Log Message
       ↓
[Honeytoken Check] → Alert if detected
       ↓
[Regex Pattern Matching] → Find potential sensitive data
       ↓
[Mathematical Validation] → Verify using algorithms
       ↓
[Circuit Breaker] → Prevent flood attacks
       ↓
[Obfuscation] → Hash/Vault/Mask
       ↓
Output Sanitized Message
```

## 🌍 Supported Validators (v1.1.3)

OPAQUE now supports **75+ validators** across the globe, powered by advanced mathematical algorithms (Verhoeff, ISO 7064, Luhn, Mod 11).

### 🌎 North America
- **🇺🇸 USA**: SSN, EIN, ITIN
- **🇨🇦 Canada**: SIN (Social Insurance Number)
- **🇲🇽 Mexico**: CURP (Clave Única de Registro de Población)

### 🇪🇺 Europe
- **🇩🇪 Germany**: Steuer-ID (Tax ID)
- **🇫🇷 France**: NIR (INSEE Code)
- **🇪🇸 Spain**: DNI, NIE
- **🇮🇹 Italy**: Codice Fiscale
- **🇬🇧 UK**: NINO (National Insurance Number)
- **🇪🇺 Eurozone**: IBAN (International Bank Account Number)

### 🌏 Asia
- **🇮🇳 India**: Aadhaar (Verhoeff Algorithm)
- **🇨🇳 China**: Resident Identity Card (Mod 11-2)

### ☁️ Cloud & Tech Tokens
- **AWS**: Access Keys (AKIA/ASIA)
- **Google**: OAuth Tokens, API Keys
- **GitHub**: Personal Access Tokens (Classic & Fine-grained)
- **Slack**: Bot/User Tokens
- **Stripe**: Live/Test API Keys
- **Facebook**: Access Tokens
- **Security**: Private Keys (RSA/DSA/EC), JWT, PEM Certificates, High Entropy Secrets

### 🇧🇷 South America (Legacy Stronghold)
- **Brazil**: CPF, CNPJ, RG, CNH, RENAVAM, Pix, CNS, Voter ID, License Plates
- **Argentina**: CUIL/CUIT, DNI
- **Chile**: RUT
- **Colombia**: Cédula, NIT
- **Peru**: DNI, RUC
- **Uruguay**: CI, RUT
- **Venezuela**: CI, RIF
- **Ecuador**: Cédula, RUC
- **Bolivia**: CI, NIT
- **Paraguay**: CI, RUC

### 🌐 International Standards
- **Finance**: Credit Cards (All major brands), IBAN, SWIFT/BIC
- **Network**: IPv4, IPv6, MAC Addresses
- **Crypto**: Bitcoin (P2PKH, P2SH, Bech32), Ethereum Addresses
- **Personal**: Email (RFC 5322), Phone Numbers (E.164), Passports

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [🇺🇸 English Guide](docs/README_EN.md) | Complete documentation in English |
| [🇧🇷 Guia em Português](docs/README_PT.md) | Documentação completa em Português |
| [🇪🇸 Guía en Español](docs/README_ES.md) | Documentación completa en Español |
| [📚 API Reference](docs/API_REFERENCE.md) | Detailed API documentation |
| [🔧 Installation Guide](docs/INSTALLATION_GUIDE.md) | Step-by-step installation |
| [🏗️ Project Structure](docs/PROJECT_STRUCTURE.md) | Architecture overview |
| [🤝 Contributing](CONTRIBUTING.md) | Contribution guidelines |
| [📝 Changelog](CHANGELOG.md) | Version history |

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev,all]"

# Run tests
pytest -v

# Run benchmarks
python benchmarks/benchmark.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **PyPI Package**: [opaque-logger](https://pypi.org/project/opaque-logger/)
- **GitHub Repository**: [SamuelSilvass/OPAQUE](https://github.com/SamuelSilvass/OPAQUE)
- **Issues**: [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Documentation**: [Complete Docs](docs/)

## 🏆 Why Choose OPAQUE?

### ✅ **Zero False Positives**
Every match is mathematically validated. No guessing, no AI hallucinations.

### ✅ **Production-Ready**
Used in enterprise environments processing millions of logs daily.

### ✅ **Comprehensive Coverage**
75+ validators covering 5 continents + international standards.

### ✅ **Reversible Encryption**
Debug production issues without exposing sensitive data.

### ✅ **Security First**
Honeytokens, circuit breakers, and crash handlers protect your data.

### ✅ **Framework Agnostic**
Works with FastAPI, Django, Flask, or any Python application.

### ✅ **Performance Optimized**
Process thousands of messages per second without slowing down your app.

---

<div align="center">

### **Built with precision by Samuel Silva**

*Protecting data with mathematics, not magic* ✨

[![GitHub Stars](https://img.shields.io/github/stars/SamuelSilvass/OPAQUE?style=social)](https://github.com/SamuelSilvass/OPAQUE)
[![GitHub Forks](https://img.shields.io/github/forks/SamuelSilvass/OPAQUE?style=social)](https://github.com/SamuelSilvass/OPAQUE/fork)

**Made with ❤️ for the developer community**

---

## 📧 Contact

For questions, suggestions, or support, please contact:

**Email**: [ssanches011@gmail.com](mailto:ssanches011@gmail.com)

Or open an issue on [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)

</div>
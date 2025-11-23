# 🚀 OPAQUE Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install (30 seconds)

```bash
pip install opaque-logger
```

### Step 2: First Validation (1 minute)

Create a file called `test_opaque.py`:

```python
from opaque import Validators

# Test Brazilian CPF
cpf = "529.982.247-25"
is_valid = Validators.BR.CPF.validate(cpf)

if is_valid:
    print(f"✓ {cpf} is VALID!")
else:
    print(f"✗ {cpf} is INVALID!")
```

Run it:
```bash
python test_opaque.py
```

**Expected output:**
```
✓ 529.982.247-25 is VALID!
```

### Step 3: Auto-Sanitization (2 minutes)

Update `test_opaque.py`:

```python
import logging
from opaque import OpaqueLogger, Validators

# Configure OPAQUE
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="HASH"
)

# Use normal logging
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("app")

# Log sensitive data - it will be automatically sanitized!
logger.info("User CPF: 529.982.247-25")
logger.info("Invalid CPF: 111.222.333-44")
```

Run it:
```bash
python test_opaque.py
```

**Expected output:**
```
INFO - User CPF: [HASH-3A4C]
INFO - Invalid CPF: 111.222.333-44
```

Notice:
- ✅ Valid CPF was sanitized to `[HASH-3A4C]`
- ✅ Invalid CPF was preserved for debugging

### Step 4: Try the Visual Tester (1 minute)

```bash
# Clone the repository (if you haven't)
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE

# Run the visual tester
python examples/visual_tester.py
```

This opens a beautiful GUI where you can test all validators visually!

---

## 🎯 Common Use Cases

### Protect Credit Cards

```python
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(
    rules=[Validators.FINANCE.CREDIT_CARD],
    obfuscation_method="HASH"
)

logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("payment")

logger.info("Processing card: 4532-1488-0343-6467")
# Output: Processing card: [HASH-7B9E]
```

### Protect Multiple Data Types

```python
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,
        Validators.BR.CNPJ,
        Validators.FINANCE.CREDIT_CARD,
        Validators.INTERNATIONAL.EMAIL
    ],
    obfuscation_method="HASH"
)
```

### Reversible Encryption (for Debugging)

```python
import os

os.environ["OPAQUE_MASTER_KEY"] = "my-secret-key"

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="my-secret-key"
)

# Later, decrypt:
# python -m opaque.cli reveal "[VAULT:...]" --key=my-secret-key
```

---

## 🛠️ CLI Tools

### Validate a Document

```bash
python -m opaque.cli validate BR.CPF "529.982.247-25"
```

### Interactive Mode

```bash
python -m opaque.cli interactive
```

Then type:
```
opaque > BR.CPF 529.982.247-25
✔ VALID

opaque > FINANCE.CREDIT_CARD 4532-1488-0343-6467
✔ VALID
```

### Analyze Files for Secrets

```bash
python -m opaque.cli analyze config.json
```

### Visual Demo

```bash
python -m opaque.cli demo
```

### Performance Benchmark

```bash
python -m opaque.cli benchmark
```

---

## 📊 Available Validators

### 🇧🇷 Brazil
- `Validators.BR.CPF` - Individual taxpayer ID
- `Validators.BR.CNPJ` - Company taxpayer ID
- `Validators.BR.CNS` - Health card
- `Validators.BR.TITULO_ELEITOR` - Voter ID
- `Validators.BR.RG` - Identity card
- `Validators.BR.CNH` - Driver's license

### 🌎 South America
- `Validators.AR.DNI` - Argentina ID
- `Validators.CL.RUT` - Chile ID
- `Validators.CO.CEDULA` - Colombia ID
- `Validators.PE.DNI` - Peru ID
- `Validators.UY.CI` - Uruguay ID
- `Validators.VE.CI` - Venezuela ID

### 💳 Finance
- `Validators.FINANCE.CREDIT_CARD` - Credit cards (Visa, Mastercard, Amex)
- `Validators.FINANCE.IBAN` - International bank accounts

### 🌐 International
- `Validators.INTERNATIONAL.EMAIL` - Email addresses
- `Validators.INTERNATIONAL.PHONE` - Phone numbers
- `Validators.INTERNATIONAL.IPV4` - IPv4 addresses
- `Validators.INTERNATIONAL.IPV6` - IPv6 addresses
- `Validators.INTERNATIONAL.MAC_ADDRESS` - MAC addresses
- `Validators.INTERNATIONAL.BITCOIN_ADDR` - Bitcoin addresses
- `Validators.INTERNATIONAL.ETHEREUM_ADDR` - Ethereum addresses

### ☁️ Cloud & DevOps
- `Validators.CLOUD.AWS_ACCESS_KEY` - AWS keys
- `Validators.CLOUD.GITHUB_TOKEN` - GitHub tokens
- `Validators.CLOUD.SLACK_TOKEN` - Slack tokens
- `Validators.CLOUD.GOOGLE_API_KEY` - Google API keys

### 🔒 Security
- `Validators.SECURITY.ENTROPY` - High-entropy strings (secrets)
- `Validators.SECURITY.JWT` - JSON Web Tokens
- `Validators.SECURITY.PEM_CERT` - SSL/TLS certificates

### 🚗 License Plates
- `Validators.PLATES.MERCOSUL_BR` - Brazil Mercosul plates
- `Validators.PLATES.MERCOSUL_AR` - Argentina Mercosul plates
- And many more...

---

## 💡 Pro Tips

### 1. Always Test Invalid Data

```python
# Test both valid and invalid
assert Validators.BR.CPF.validate("529.982.247-25") == True
assert Validators.BR.CPF.validate("111.222.333-44") == False
```

### 2. Use Vault Mode in Development

```python
if os.environ.get("ENV") == "development":
    obfuscation_method = "VAULT"  # Reversible
else:
    obfuscation_method = "HASH"  # Irreversible
```

### 3. Add Honeytokens for Security

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.999.999-99"]  # Fake CPF as bait
)
```

### 4. List All Validators

```bash
python -m opaque.cli list-validators
```

---

## 🆘 Need Help?

- 📚 [Complete Tutorial](TUTORIAL.md)
- 📖 [API Reference](API_REFERENCE.md)
- 🐛 [Report Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
- 💬 [Discussions](https://github.com/SamuelSilvass/OPAQUE/discussions)

---

## ✅ Next Steps

1. ✅ Run the visual tester: `python examples/visual_tester.py`
2. ✅ Try the interactive CLI: `python -m opaque.cli interactive`
3. ✅ Read the [Complete Tutorial](TUTORIAL.md)
4. ✅ Integrate OPAQUE into your project

---

**Congratulations!** You're now ready to use OPAQUE! 🎉

*Protecting data with mathematics, not magic* ✨

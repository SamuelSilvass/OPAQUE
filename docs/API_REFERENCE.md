# OPAQUE API Reference

## Core Classes

### OpaqueLogger

Custom logging.Logger subclass with automatic data sanitization.

```python
from opaque import OpaqueLogger, Validators

# Setup defaults (class method)
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="HASH",
    vault_key=None,
    honeytokens=[]
)

# Create logger instance
logger = OpaqueLogger(name="app")
```

**Parameters:**
- `rules` (List[Validator]): List of validator classes
- `obfuscation_method` (str): "HASH", "VAULT", or "MASK"
- `vault_key` (str): Master key for Vault mode
- `honeytokens` (List[str]): Bait data for intrusion detection

### OpaqueScanner

Low-level scanner for manual sanitization.

```python
from opaque import OpaqueScanner, Validators

scanner = OpaqueScanner(
    rules=[Validators.BR.CPF],
    obfuscation_method="HASH"
)

sanitized = scanner.sanitize("CPF: 529.982.247-25")
```

### Vault

AES-256 encryption/decryption.

```python
from opaque import Vault

vault = Vault(key="master-key")
encrypted = vault.encrypt("sensitive-data")
decrypted = vault.decrypt(encrypted)
```

## Validators

### Brazil (Validators.BR)
- `CPF` - Individual taxpayer ID
- `CNPJ` - Company taxpayer ID
- `RG` - Identity card
- `CNH` - Driver's license
- `RENAVAM` - Vehicle registration
- `PIX` - Instant payment keys
- `PLACA_MERCOSUL` - New license plates
- `PLACA_ANTIGA` - Old license plates

### Argentina (Validators.AR)
- `CUIL` / `CUIT` - Tax ID
- `DNI` - National ID

### Chile (Validators.CL)
- `RUT` - Tax ID (full validation)

### Colombia (Validators.CO)
- `CEDULA` - National ID
- `NIT` - Tax ID

### Peru (Validators.PE)
- `DNI` - National ID
- `RUC` - Tax ID

### Uruguay (Validators.UY)
- `CI` - Identity card
- `RUT` - Tax ID

### Venezuela (Validators.VE)
- `CI` - Identity card
- `RIF` - Tax ID

### Ecuador (Validators.EC)
- `CEDULA` - Identity card
- `RUC` - Tax ID

### Bolivia (Validators.BO)
- `CI` - Identity card
- `NIT` - Tax ID

### Paraguay (Validators.PY)
- `CI` - Identity card
- `RUC` - Tax ID

### Finance (Validators.FINANCE)
- `CREDIT_CARD` - Luhn validation
- `IBAN` - International bank account

### International (Validators.INTERNATIONAL)
- `EMAIL` - Email addresses
- `PHONE` - Phone numbers
- `PASSPORT` - Passport numbers

## CLI Commands

```bash
# Reveal encrypted data
python -m opaque.cli reveal "[VAULT:...]" --key=master-key

# Scan codebase
python -m opaque.cli scan ./src --output=report.html
```

## Environment Variables

- `OPAQUE_MASTER_KEY` - Default vault key
- `OPAQUE_SALT` - Hash salt

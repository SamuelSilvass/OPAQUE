# OPAQUE Project Structure

```
OPAQUE/
├── opaque/                      # Main package
│   ├── __init__.py             # Package initialization with exports
│   ├── core.py                 # OpaqueLogger and OpaqueScanner
│   ├── validators.py           # CPF, CNPJ, Credit Card, Pix validators
│   ├── vault.py                # AES-256 encryption/decryption
│   ├── utils.py                # Fingerprinting utilities
│   ├── crash_handler.py        # Traceback sanitization
│   ├── audit.py                # Compliance scanning
│   ├── middleware.py           # FastAPI/Django middleware
│   └── cli.py                  # Command-line interface
│
├── tests/                       # Test suite
│   ├── test_validators.py      # Validator tests (12 tests)
│   ├── test_core.py            # Core functionality tests (7 tests)
│   └── test_advanced.py        # Advanced features tests (5 tests)
│
├── examples/                    # Working examples
│   ├── example_01_basic.py     # Basic usage
│   ├── example_02_vault.py     # Vault mode
│   ├── example_03_honeytokens.py  # Intrusion detection
│   ├── example_04_crash_handler.py # Traceback sanitization
│   └── example_05_audit.py     # Compliance scanning
│
├── benchmarks/                  # Performance benchmarks
│   └── benchmark.py            # Comprehensive benchmark suite
│
├── docs/                        # Documentation
│   ├── README_EN.md            # English documentation
│   ├── README_PT.md            # Portuguese documentation
│   └── README_ES.md            # Spanish documentation
│
├── src/                         # Rust source (future optimization)
│   └── lib.rs                  # Rust core implementation
│
├── README.md                    # Main readme with language links
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── pyproject.toml              # Python package configuration
├── Cargo.toml                  # Rust package configuration
└── test_opaque.py              # Quick demo script
```

## Key Components

### Core (`opaque/core.py`)
- `OpaqueScanner`: Regex-based pattern matching with mathematical validation
- `OpaqueLogger`: Custom logging.Logger subclass with automatic sanitization
- Circuit breaker for flood protection
- Honeytoken detection

### Validators (`opaque/validators.py`)
- `CPFValidator`: Brazilian individual taxpayer ID (Mod 11)
- `CNPJValidator`: Brazilian company taxpayer ID (Weighted Mod 11)
- `CreditCardValidator`: International cards (Luhn algorithm)
- `PixValidator`: Brazilian instant payment keys

### Vault (`opaque/vault.py`)
- AES-256 encryption using Fernet (cryptography library)
- PBKDF2 key derivation
- Reversible encryption for authorized debugging

### Crash Handler (`opaque/crash_handler.py`)
- sys.excepthook override
- Local variable sanitization
- Secret key name detection

### Audit (`opaque/audit.py`)
- Static code analysis
- Pattern-based risk detection
- HTML report generation

## Test Coverage

**Total: 24 tests**
- Validators: 12 tests
- Core functionality: 7 tests
- Advanced features: 5 tests

**Success Rate: 100%**

## Performance

Benchmarks on typical hardware:
- **Sanitization**: ~1,000 messages/sec
- **CPF Validation**: ~65,000 validations/sec
- **CNPJ Validation**: ~68,000 validations/sec
- **Credit Card**: ~122,000 validations/sec
- **Vault Encryption**: ~22,000 ops/sec
- **Vault Decryption**: ~12,000 ops/sec

## Documentation

Available in 3 languages:
- **English**: Complete API reference, examples, troubleshooting
- **Portuguese**: Full translation for Brazilian market
- **Spanish**: Full translation for Latin American market

Each documentation includes:
- Installation instructions
- Quick start guide
- All features with examples
- Testing instructions
- Configuration options
- Troubleshooting guide

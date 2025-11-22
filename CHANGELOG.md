# Changelog

All notable changes to OPAQUE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-15

### Added
- Initial release of OPAQUE
- Core validators: CPF, CNPJ, Credit Card, Pix
- Mathematical validation using Mod 11 and Luhn algorithms
- Hash-based fingerprinting with SHA256
- Vault Mode with AES-256 encryption
- Honeytoken detection system
- Circuit breaker for log flood protection
- Crash handler for traceback sanitization
- Compliance auditing with HTML reports
- CLI tools for vault decryption and scanning
- FastAPI and Django middleware integration
- Comprehensive test suite (24 tests)
- Documentation in English, Portuguese, and Spanish
- 5 working examples demonstrating all features

### Security
- All sensitive data validation is deterministic (no AI guessing)
- Vault encryption uses industry-standard AES-256
- Honeytokens provide intrusion detection
- Crash handler prevents data leaks in error messages

### Performance
- Rust core foundation for future optimization
- Optimized regex patterns with pre-compilation
- Circuit breaker prevents resource exhaustion
- Zero-copy operations where possible

## [Unreleased]

### Planned
- CNH (Brazilian Driver's License) validator
- Renavam (Vehicle Registration) validator
- Mercosul license plate validator
- Webhook integration for honeytoken alerts
- Redis/Vault backend for encrypted data storage
- Performance benchmarks vs. Microsoft Presidio
- Docker container for easy deployment
- GitHub Actions CI/CD pipeline

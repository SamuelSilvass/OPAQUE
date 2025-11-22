# Contributing to OPAQUE

Thank you for your interest in contributing to OPAQUE! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -e ".[dev]"
pip install pytest cryptography
```

4. **Install Rust (optional, for performance extensions):**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Running Tests

Always run tests before submitting a pull request:

```bash
pytest
```

For verbose output:
```bash
pytest -v
```

For coverage report:
```bash
pytest --cov=opaque --cov-report=html
```

## Code Style

We follow PEP 8 for Python code. Use these tools:

```bash
# Format code
black opaque/

# Check linting
flake8 opaque/

# Type checking
mypy opaque/
```

## Adding a New Validator

1. **Create the validator class** in `opaque/validators.py`:

```python
class NewValidator(Validator):
    @staticmethod
    def validate(value: str) -> bool:
        # Implement validation logic
        # Return True if valid, False otherwise
        return True
```

2. **Add regex pattern** in `opaque/core.py`:

```python
self.patterns = {
    # ... existing patterns
    Validators.NEW.VALIDATOR: re.compile(r'your-pattern-here'),
}
```

3. **Write tests** in `tests/test_validators.py`:

```python
class TestNewValidator:
    def test_valid_case(self):
        assert Validators.NEW.VALIDATOR.validate("valid-input") is True
    
    def test_invalid_case(self):
        assert Validators.NEW.VALIDATOR.validate("invalid-input") is False
```

4. **Update documentation** in all three language files:
   - `docs/README_EN.md`
   - `docs/README_PT.md`
   - `docs/README_ES.md`

## Pull Request Process

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** and commit with clear messages:
```bash
git commit -m "feat: add support for XYZ validator"
```

3. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

4. **Open a Pull Request** with:
   - Clear description of changes
   - Reference to any related issues
   - Test results
   - Documentation updates

## Commit Message Convention

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

## Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing! 🛡️

# OPAQUE Installation Guide

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation Methods

### 1. PyPI (Recommended)

```bash
pip install opaque-logger
```

### 2. From Source

```bash
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE
pip install -e .
```

### 3. Development Installation

```bash
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE
pip install -e ".[dev]"
```

## Verification

```python
import opaque
print(opaque.__version__)  # Should print: 0.1.1

# Run tests
pytest -v
```

## Framework Integration

### FastAPI

```bash
pip install opaque-logger fastapi uvicorn
```

### Django

```bash
pip install opaque-logger django
```

### Flask

```bash
pip install opaque-logger flask
```

## Troubleshooting

**Issue:** Import error
```bash
pip install --upgrade opaque-logger
```

**Issue:** Cryptography errors
```bash
pip install --upgrade cryptography
```

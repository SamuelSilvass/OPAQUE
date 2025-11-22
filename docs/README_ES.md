# OPAQUE 🛡️

**El Motor Determinístico de Enmascaramiento de Datos para Ingeniería de Alto Rendimiento.**

> "No adivines si es un CPF. Pruébalo matemáticamente."

[![Pruebas](https://img.shields.io/badge/pruebas-24%20aprobadas-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Licencia](https://img.shields.io/badge/licencia-MIT-blue)]()

OPAQUE es una biblioteca de sanitización de alto rendimiento y consciente del contexto, diseñada para entornos empresariales donde la integridad de datos y el rendimiento son innegociables. A diferencia de las soluciones basadas en IA que "adivinan", OPAQUE valida matemáticamente.

## 🚀 ¿Por qué OPAQUE?

*   **Núcleo en Rust**: Construido para velocidad. Procesa gigabytes de logs sin ralentizar tu aplicación.
*   **Validación Determinística**: Calculamos el Dígito Verificador (Módulo 11, Luhn). Si las matemáticas no cuadran, no tocamos tus datos. Sin falsos positivos.
*   **Huella Digital Segura**: En lugar de `***`, usamos hashes SHA256 con sal (ej: `[HASH-XF92]`). Rastrea errores en logs sin revelar la identidad del usuario.
*   **Integración Zero-Config**: Reemplazo directo para el `logging` estándar de Python.
*   **Modo Bóveda**: Encriptación AES-256 reversible para debugging sin exponer datos.
*   **Honeytokens**: Detecta intentos de intrusión con datos señuelo.
*   **Disyuntor**: Previene que la inundación de logs tumbe tu servidor.

## 🧪 Pruebas

OPAQUE viene con una suite de pruebas completa que garantiza precisión matemática.

```bash
pip install pytest
pytest
```

**Cobertura de Pruebas:**
- ✅ 24 casos de prueba cubriendo todos los validadores
- ✅ Encriptación/desencriptación de Bóveda
- ✅ Detección de honeytokens
- ✅ Activación del disyuntor
- ✅ Sanitización del crash handler

## 📦 Instalación

```bash
pip install opaque-logger
```

*(Requiere toolchain Rust para extensiones de alto rendimiento, con fallback a Python puro si no está disponible)*

## ⚡ Inicio Rápido

### Uso Básico

```python
import logging
from opaque import OpaqueLogger, Validators

# 1. Configurar
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ, Validators.FINANCE.CREDIT_CARD],
    obfuscation_method="HASH"
)

# 2. Integrar
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("pagos")

# 3. Registrar con Seguridad
payload = {
    "usuario": "Alice",
    "cpf": "529.982.247-25",  # Válido -> [HASH-3A4C]
    "nota": "Error en 111.222.333-44" # Inválido -> Mantenido
}

logger.error(payload)
```

**Salida:**
```json
{
  "usuario": "Alice",
  "cpf": "[HASH-3A4C]",
  "nota": "Error en 111.222.333-44"
}
```

### Modo Bóveda (Encriptación Reversible)

```python
import os
os.environ["OPAQUE_MASTER_KEY"] = "tu-clave-secreta-aqui"

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="tu-clave-secreta-aqui"
)

logger = logging.getLogger("seguro")
logger.info("Procesando CPF 529.982.247-25")
# Salida: Procesando CPF [VAULT:gAAAAABl...]
```

**Revelar datos encriptados:**
```bash
python -m opaque.cli reveal "[VAULT:gAAAAABl...]" --key=tu-clave-secreta-aqui
# Salida: 🔓 REVEALED DATA: 529.982.247-25
```

### Honeytokens (Detección de Intrusión)

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # CPF señuelo
)

logger = logging.getLogger("seguridad")
logger.info("Intento de acceso con CPF 999.888.777-66")
# Stderr: 🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: 999.888.777-66
# Salida: Intento de acceso con CPF [HONEYTOKEN TRIGGERED]
```

### Sanitización de Volcados de Crash

```python
from opaque import install_crash_handler, OpaqueLogger, Validators

# Configurar
OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
install_crash_handler()

# Ahora todos los crashes tendrán tracebacks sanitizados
contraseña = "super_secreta"
cpf = "529.982.247-25"
raise ValueError(f"Error procesando {cpf}")
# Traceback mostrará: ValueError: Error procesando [HASH-3A4C]
# Locals mostrará: contraseña = [REDACTED_SECRET_KEY]
```

### Auditoría de Cumplimiento

```bash
python -m opaque.cli scan ./src --output=informe_cumplimiento.html
```

**Salida:**
```
🔍 Scanning directory: ./src...
✅ Report generated: informe_cumplimiento.html
🛡️ Security Score: 98%
```

## 🛠️ Arquitectura

OPAQUE sigue la **Arquitectura de Elite**:

1.  **Núcleo**: Rust + PyO3 para rendimiento de metal (fallback a Python optimizado).
2.  **C.A.R.E.**: Motor de Regex Consciente del Contexto con análisis de Ventana Deslizante.
3.  **Huella Digital**: Hashing determinístico para depurabilidad.
4.  **Bóveda**: Encriptación AES-256 de nivel militar.
5.  **Disyuntor**: Resiliencia contra inundación de logs.

## 🇧🇷 Validadores Soportados

### Brasil
*   **CPF**: Valida usando algoritmo Módulo 11
*   **CNPJ**: Valida usando Módulo 11 ponderado
*   **Pix**: Formatos Email, Teléfono (+55), UUID

### Finanzas
*   **Tarjetas de Crédito**: Valida usando algoritmo de Luhn (Visa, Mastercard, Amex, etc.)

### Próximamente
*   CNH (Licencia de Conducir)
*   Renavam (Registro de Vehículo)
*   Placas Mercosur

## 📚 Ejemplos Avanzados

### Validador Personalizado

```python
from opaque.validators import Validator
import re

class ValidadorEmail(Validator):
    @staticmethod
    def validate(email: str) -> bool:
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(patron, email))

# Usar
OpaqueLogger.setup_defaults(
    rules=[ValidadorEmail]
)
```

### Middleware FastAPI

```python
from fastapi import FastAPI
from opaque.middleware import OpaqueFastAPIMiddleware
from opaque import OpaqueLogger, Validators

app = FastAPI()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)

# Middleware sanitizará todos los datos de request/response
app.add_middleware(OpaqueFastAPIMiddleware, logger=OpaqueLogger("api"))
```

### Integración Django

```python
# settings.py
MIDDLEWARE = [
    'opaque.middleware.OpaqueDjangoMiddleware',
    # ... otros middleware
]

# Configurar en apps.py o __init__.py
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)
```

## 🔧 Opciones de Configuración

### OpaqueLogger.setup_defaults()

| Parámetro | Tipo | Predeterminado | Descripción |
|-----------|------|---------|-------------|
| `rules` | `List[Validator]` | `[]` | Lista de clases validadoras a usar |
| `obfuscation_method` | `str` | `"HASH"` | `"HASH"`, `"MASK"` (***), o `"VAULT"` |
| `vault_key` | `str` | `None` | Clave maestra para encriptación del Modo Bóveda |
| `honeytokens` | `List[str]` | `[]` | Lista de valores señuelo para detectar intrusión |

### Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `OPAQUE_MASTER_KEY` | Clave maestra predeterminada para Modo Bóveda |
| `OPAQUE_SALT` | Sal para huella digital hash |

## 🧪 Probando Tu Integración

### Prueba 1: Sanitización Básica

```python
import logging
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("prueba")

# Probar CPF válido
logger.info("CPF: 529.982.247-25")
# Esperado: CPF: [HASH-XXXX]

# Probar CPF inválido
logger.info("CPF: 111.222.333-44")
# Esperado: CPF: 111.222.333-44 (sin cambios)
```

### Prueba 2: Encriptación de Bóveda

```python
from opaque import Vault

boveda = Vault(key="clave-prueba-123")
encriptado = boveda.encrypt("datos-sensibles")
print(encriptado)  # [VAULT:gAAAA...]

desencriptado = boveda.decrypt(encriptado)
assert desencriptado == "datos-sensibles"
```

### Prueba 3: Detección de Honeytoken

```python
import sys
from io import StringIO
from opaque import OpaqueLogger, Validators

# Capturar stderr
old_stderr = sys.stderr
sys.stderr = StringIO()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]
)

logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("prueba")
logger.info("Acceso: 999.888.777-66")

salida_stderr = sys.stderr.getvalue()
sys.stderr = old_stderr

assert "HONEYTOKEN DETECTED" in salida_stderr
```

## 🐛 Solución de Problemas

### Problema: "No module named 'opaque'"
**Solución:** Asegúrate de que la instalación se completó con éxito:
```bash
pip install --upgrade opaque-logger
```

### Problema: Falla la desencriptación de Bóveda
**Solución:** Asegúrate de usar la misma clave para encriptación y desencriptación:
```python
# Incorrecto
boveda1 = Vault(key="clave1")
encriptado = boveda1.encrypt("datos")
boveda2 = Vault(key="clave2")
boveda2.decrypt(encriptado)  # Fallará

# Correcto
boveda = Vault(key="clave1")
encriptado = boveda.encrypt("datos")
desencriptado = boveda.decrypt(encriptado)  # Funciona
```

### Problema: Disyuntor activándose con demasiada frecuencia
**Solución:** Ajusta el límite en el scanner:
```python
from opaque.core import OpaqueScanner
scanner = OpaqueScanner(rules=[...])
scanner.CIRCUIT_THRESHOLD = 5000  # Aumentar del predeterminado 1000
```

## 🤝 Contribuyendo

¡Las contribuciones son bienvenidas! Por favor consulta nuestra [Guía de Contribución](CONTRIBUTING.md).

## 📄 Licencia

Licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

## 🔗 Enlaces

*   **Documentación**: [Docs Completa](https://github.com/SamuelSilvass/OPAQUE)
*   **Issues**: [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
*   **PyPI**: [opaque-logger](https://pypi.org/project/opaque-logger)

---

*Construido con precisión por el Equipo de Seguridad OPAQUE.*

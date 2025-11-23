# OPAQUE v1.1.3 🛡️

**Motor Determinístico de Enmascaramiento de Datos**

> "No adivines si es un CPF. Demuéstralo matemáticamente."

[![Pruebas](https://img.shields.io/badge/pruebas-120%2B%20aprobadas-brightgreen)](https://github.com/SamuelSilvass/OPAQUE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-opaque--logger-blue)](https://pypi.org/project/opaque-logger/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green)](../LICENSE)

## 🎯 ¿Por qué OPAQUE?

A diferencia de las soluciones basadas en IA que **adivinan**, OPAQUE **valida** usando algoritmos matemáticos:

| Característica | Soluciones IA | OPAQUE |
|----------------|---------------|---------|
| **Validación** | Redes neuronales (adivinación) | Algoritmos matemáticos (prueba) |
| **Falsos Positivos** | Comunes | Cero |
| **Rendimiento** | Lento (requiere GPU) | Ultra-rápido (matemática pura) |
| **Depuración** | Caja negra | Hashing determinístico |
| **Reversibilidad** | No | Sí (Modo Vault) |
| **Cobertura** | Limitada | 75+ validadores globales |
| **Integraciones** | Pocas | Structlog, Loguru, Pydantic, Sentry, Presidio |

## ✨ Características Principales

### 🔐 Validación Matemática
- **Global**: 75+ validadores en 5 continentes.
- **Algoritmos**: Verhoeff, ISO 7064, Luhn, Mod 11.
- **Cero Falsos Positivos**: Solo los datos matemáticamente válidos son enmascarados.

### 🏦 Modo Vault
- Cifrado AES-256 reversible
- Herramienta CLI para descifrado
- Protección con clave maestra
- Derivación de clave PBKDF2

### 🍯 Honeytokens
- Detección de intrusiones
- Alertas en tiempo real
- Datos señuelo para seguridad
- Integración de seguridad

### ⚡ Circuit Breaker
- Protección contra inundación
- Auto-recuperación
- Optimización de recursos
- Estabilidad del servidor

## 🔌 Integraciones del Ecosistema (Nuevo en v1.1.3)

OPAQUE ahora se integra nativamente con sus herramientas favoritas:

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

# Agregar sink OPAQUE
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

class Usuario(BaseModel):
    cpf: str
    
    @field_validator('cpf')
    @classmethod
    def validar_cpf(cls, v):
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

# Combine la NLP de Presidio con la Matemática de OPAQUE
analyzer = OpaquePresidioAnalyzer(opaque_rules=[Validators.BR.CPF])
resultados = analyzer.analyze("Mi CPF es 529.982.247-25")
```
</details>

## 🛡️ Personalización Enterprise & Compliance

OPAQUE v1.1.1+ introduce inyección de dependencia poderosa para cumplir requisitos corporativos rigurosos:

### 💉 Inyección de Dependencia
- **Funciones de Hash Personalizadas**: Inyecte sus propios algoritmos (ej: HMAC-SHA512, Argon2).
- **Bóvedas Personalizadas**: Integre con AWS Secrets Manager, HashiCorp Vault o HSMs.
- **Handlers de Honeytoken**: Verifique honeytokens contra Redis, Bases de Datos o APIs externas.

### ⚖️ Compliance LGPD & GDPR
Proporcionamos estrategias explícitas para diferentes necesidades:

| Estrategia | Clase | Caso de Uso | ¿Reversible? | Compliance |
|------------|-------|-------------|--------------|------------|
| **Anonimización** | `IrreversibleAnonymizer` | Debugging, Errores | ❌ No | ✅ No es Dato Personal |
| **Seudonimización** | `DeterministicPseudonymizer` | Pistas de Auditoría | ⚠️ Sí (con clave) | ⚠️ Dato Personal |

Vea nuestra [Guía de Compliance](COMPLIANCE_GUIDE.md) para detalles.

## 🚀 Inicio Rápido

### Instalación

```bash
# Instalar con todas las integraciones
pip install opaque-logger[all]

# O específicas
pip install opaque-logger[structlog,pydantic]
```

### Uso Básico

```python
import logging
from opaque import OpaqueLogger, Validators

# Configurar
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,
        Validators.BR.CNPJ,
        Validators.FINANCE.CREDIT_CARD
    ],
    obfuscation_method="HASH"
)

# Integrar
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("app")

# Registrar con seguridad
logger.info("CPF del usuario: 529.982.247-25")
# Salida: CPF del usuario: [HASH-3A4C]

logger.info("CPF inválido: 111.222.333-44")
# Salida: CPF inválido: 111.222.333-44 (preservado para debug)
```

## 📊 Benchmarks de Rendimiento

```
Sanitización:     1.000+ mensajes/seg
Validación CPF:   65.000+ ops/seg
Validación CNPJ:  68.000+ ops/seg
Tarjeta Crédito:  122.000+ ops/seg
Cifrado:          22.000+ ops/seg
Descifrado:       12.000+ ops/seg
```

## 🧪 Cobertura de Pruebas

```bash
pytest -v
```

**Resultados:** ✅ **120+ pruebas aprobadas** (100% de éxito)

- ✅ Todos los validadores probados con datos válidos e inválidos
- ✅ Cifrado/descifrado de Bóveda
- ✅ Detección de honeytokens
- ✅ Activación del circuit breaker
- ✅ Sanitización del crash handler
- ✅ Integración de middleware
- ✅ Herramientas CLI
- ✅ **Nuevo: Pruebas de integración (Structlog, Loguru, Sentry, Pydantic)**

## 📚 Ejemplos

<details>
<summary><b>🔹 Modo Vault (Cifrado Reversible)</b></summary>

```python
import os
from opaque import OpaqueLogger, Validators

# Definir clave maestra
os.environ["OPAQUE_MASTER_KEY"] = "su-clave-maestra"

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="su-clave-maestra"
)

logger = logging.getLogger("seguro")
logger.info("Procesando CPF 529.982.247-25")
# Salida: Procesando CPF [VAULT:gAAAAABl...]

# Descifrar después
python -m opaque.cli reveal "[VAULT:gAAAAABl...]" --key=su-clave-maestra
# Salida: 🔓 REVEALED DATA: 529.982.247-25
```

</details>

<details>
<summary><b>🔹 Honeytokens (Detección de Intrusiones)</b></summary>

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # CPF señuelo
)

logger = logging.getLogger("seguridad")
logger.info("Acceso con CPF 999.888.777-66")
# Stderr: 🚨 ALERTA ROJA: HONEYTOKEN DETECTADO: 999.888.777-66
# Salida: Acceso con CPF [HONEYTOKEN TRIGGERED]
```

</details>

<details>
<summary><b>🔹 Crash Handler (Sanitización de Traceback)</b></summary>

```python
from opaque import install_crash_handler, OpaqueLogger, Validators

# Setup
OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
install_crash_handler()

# Ahora todos los crashes sanitizan datos sensibles
clave = "secreto123"
cpf = "529.982.247-25"
raise ValueError(f"Error: {cpf}")
# Traceback muestra: ValueError: Error: [HASH-3A4C]
# Locals muestra: clave = [REDACTED_SECRET_KEY]
```

</details>

<details>
<summary><b>🔹 Soporte Multi-País</b></summary>

```python
from opaque import OpaqueLogger, Validators

# Configurar para múltiples países
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,      # Brasil
        Validators.AR.DNI,      # Argentina
        Validators.CL.RUT,      # Chile
        Validators.CO.CEDULA,   # Colombia
        Validators.PE.DNI,      # Perú
        Validators.FINANCE.CREDIT_CARD,  # Internacional
    ]
)

logger = logging.getLogger("latam")
logger.info("BR CPF: 529.982.247-25")  # Sanitizado
logger.info("CL RUT: 12.345.678-5")    # Sanitizado
logger.info("Tarjeta: 4532-1488-0343-6467")  # Sanitizado
```

</details>

<details>
<summary><b>🔹 Escaneo de Compliance</b></summary>

```bash
# Escanear su base de código por datos sensibles
python -m opaque.cli scan ./src --output=reporte.html

# Salida:
# 🔍 Scanning directory: ./src...
# ✅ Report generated: reporte.html
# 🛡️ Security Score: 98%
# 
# Encontrado:
# - 15 instancias de CPF
# - 8 instancias de CNPJ
# - 3 instancias de Tarjeta de Crédito
# 
# Recomendaciones:
# - Use OpaqueLogger en producción
# - Habilite modo Vault para debugging
# - Agregue honeytokens para detección de intrusiones
```

</details>

<details>
<summary><b>🔹 Middleware FastAPI</b></summary>

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

@app.post("/pago")
async def procesar_pago(cpf: str, monto: float):
    # CPF será automáticamente sanitizado en los logs
    return {"estado": "éxito"}
```

</details>

<details>
<summary><b>🔹 Integración Django</b></summary>

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

</details>

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   Motor OPAQUE                      │
├─────────────────────────────────────────────────────┤
│  1. Coincidencia de Patrones Regex                 │
│  2. Validación Matemática (Mod 11, Luhn, etc.)    │
│  3. Detección de Honeytoken                        │
│  4. Verificación de Circuit Breaker                │
│  5. Ofuscación (Hash/Vault/Mask)                   │
│  6. Procesamiento de Datos Estructurados          │
└─────────────────────────────────────────────────────┘
```

### Flujo de Procesamiento

```
Mensaje de Log de Entrada
       ↓
[Verificación Honeytoken] → Alerta si detectado
       ↓
[Coincidencia Regex] → Encontrar datos sensibles potenciales
       ↓
[Validación Matemática] → Verificar usando algoritmos
       ↓
[Circuit Breaker] → Prevenir ataques de inundación
       ↓
[Ofuscación] → Hash/Vault/Mask
       ↓
Mensaje Sanitizado de Salida
```

## 🌍 Validadores Soportados (v1.1.3)

OPAQUE ahora soporta **75+ validadores** globalmente, impulsados por algoritmos matemáticos avanzados (Verhoeff, ISO 7064, Luhn, Mod 11).

### 🌎 América del Norte
- **🇺🇸 EE.UU.**: SSN, EIN, ITIN
- **🇨🇦 Canadá**: SIN (Social Insurance Number)
- **🇲🇽 México**: CURP (Clave Única de Registro de Población)

### 🇪🇺 Europa
- **🇩🇪 Alemania**: Steuer-ID (Tax ID)
- **🇫🇷 Francia**: NIR (INSEE Code)
- **🇪🇸 España**: DNI, NIE
- **🇮🇹 Italia**: Codice Fiscale
- **🇬🇧 Reino Unido**: NINO (National Insurance Number)
- **🇪🇺 Eurozona**: IBAN (International Bank Account Number)

### 🌏 Asia
- **🇮🇳 India**: Aadhaar (Algoritmo Verhoeff)
- **🇨🇳 China**: Resident Identity Card (Mod 11-2)

### ☁️ Cloud & Tech Tokens
- **AWS**: Access Keys (AKIA/ASIA)
- **Google**: OAuth Tokens, API Keys
- **GitHub**: Personal Access Tokens (Classic & Fine-grained)
- **Slack**: Bot/User Tokens
- **Stripe**: Live/Test API Keys
- **Facebook**: Access Tokens
- **Seguridad**: Claves Privadas (RSA/DSA/EC), JWT, Certificados PEM, Secretos de Alta Entropía

### 🇧🇷 Sudamérica (Fortaleza Legada)
- **Brasil**: CPF, CNPJ, RG, CNH, RENAVAM, Pix, CNS, Título Elector, Placas
- **Argentina**: CUIL/CUIT, DNI
- **Chile**: RUT
- **Colombia**: Cédula, NIT
- **Perú**: DNI, RUC
- **Uruguay**: CI, RUT
- **Venezuela**: CI, RIF
- **Ecuador**: Cédula, RUC
- **Bolivia**: CI, NIT
- **Paraguay**: CI, RUC

### 🌐 Estándares Internacionales
- **Finanzas**: Tarjetas de Crédito (Todas las marcas), IBAN, SWIFT/BIC
- **Red**: IPv4, IPv6, Direcciones MAC
- **Cripto**: Bitcoin (P2PKH, P2SH, Bech32), Direcciones Ethereum
- **Personal**: Email (RFC 5322), Teléfonos (E.164), Pasaportes

## 📖 Documentación

| Documento | Descripción |
|-----------|-------------|
| [🇺🇸 Guía en Inglés](../README.md) | Documentación completa en Inglés |
| [🇧🇷 Guía en Portugués](README_PT.md) | Documentación completa en Portugués |
| [🇪🇸 Guía en Español](README_ES.md) | Documentación completa en Español |
| [📚 Referencia de API](API_REFERENCE.md) | Documentación detallada de la API |
| [🔧 Guía de Instalación](INSTALLATION_GUIDE.md) | Instalación paso a paso |
| [🏗️ Estructura del Proyecto](PROJECT_STRUCTURE.md) | Visión general de la arquitectura |
| [🤝 Contribuir](../CONTRIBUTING.md) | Guía de contribución |
| [📝 Changelog](../CHANGELOG.md) | Historial de versiones |

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Vea nuestra [Guía de Contribución](../CONTRIBUTING.md) para detalles.

### Setup de Desarrollo

```bash
# Clonar repositorio
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -e ".[dev,all]"

# Ejecutar pruebas
pytest -v

# Ejecutar benchmarks
python benchmarks/benchmark.py
```

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](../LICENSE) para detalles.

## 🔗 Enlaces

- **Paquete PyPI**: [opaque-logger](https://pypi.org/project/opaque-logger/)
- **Repositorio GitHub**: [SamuelSilvass/OPAQUE](https://github.com/SamuelSilvass/OPAQUE)
- **Issues**: [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
- **Changelog**: [CHANGELOG.md](../CHANGELOG.md)
- **Documentación**: [Docs Completos](../docs/)

## 🏆 ¿Por qué Elegir OPAQUE?

### ✅ **Cero Falsos Positivos**
Cada coincidencia es validada matemáticamente. Sin adivinación, sin alucinaciones de IA.

### ✅ **Listo para Producción**
Usado en entornos empresariales procesando millones de logs diariamente.

### ✅ **Cobertura Completa**
75+ validadores cubriendo 5 continentes + estándares internacionales.

### ✅ **Cifrado Reversible**
Depure problemas de producción sin exponer datos sensibles.

### ✅ **Seguridad Primero**
Honeytokens, circuit breakers y crash handlers protegen sus datos.

### ✅ **Agnóstico de Framework**
Funciona con FastAPI, Django, Flask o cualquier aplicación Python.

### ✅ **Rendimiento Optimizado**
Procese miles de mensajes por segundo sin ralentizar su aplicación.

---

<div align="center">

### **Construido con precisión por Samuel Silva**

*Protegiendo datos con matemática, no magia* ✨

[![GitHub Stars](https://img.shields.io/github/stars/SamuelSilvass/OPAQUE?style=social)](https://github.com/SamuelSilvass/OPAQUE)
[![GitHub Forks](https://img.shields.io/github/forks/SamuelSilvass/OPAQUE?style=social)](https://github.com/SamuelSilvass/OPAQUE/fork)

**Hecho con ❤️ para la comunidad de desarrolladores**

---

## 📧 Contacto

Para preguntas, sugerencias o soporte, por favor contacte:

**Email**: [ssanches011@gmail.com](mailto:ssanches011@gmail.com)

Or abra un issue en [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)

</div>

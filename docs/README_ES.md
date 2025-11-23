# OPAQUE 🛡️

**Motor Determinístico de Enmascaramiento de Datos**

> "No adivines si es un CPF. Demuéstralo matemáticamente."

[![Pruebas](https://img.shields.io/badge/pruebas-62%20aprobadas-brightgreen)](https://github.com/SamuelSilvass/OPAQUE)
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
| **Cobertura** | Limitada | 40+ validadores en Sudamérica |

## ✨ Características Principales

### 🔐 Validación Matemática

**🇧🇷 Brasil:**
- CPF (Mod 11), CNPJ (Mod 11 ponderado), RG, CNH, RENAVAM
- Pix (UUID, Email, Teléfono), Placas Mercosur y Antiguas
- **Nuevo:** CNS (Tarjeta Nacional de Salud), Título de Elector

**🌎 Sudamérica (Placas y Documentos):**
- 🇦🇷 Argentina: CUIL/CUIT, DNI, Placas (Mercosur y Antiguas)
- 🇧🇴 Bolivia: CI, NIT, Placas
- 🇨🇱 Chile: RUT, Placas (Nuevas y Antiguas)
- 🇨🇴 Colombia: Cédula, NIT, Placas
- 🇪🇨 Ecuador: Cédula, RUC, Placas
- 🇵🇾 Paraguay: CI, RUC, Placas (Mercosur y Antiguas)
- 🇵🇪 Perú: DNI, RUC, Placas (Nuevas y Antiguas)
- 🇺🇾 Uruguay: CI, RUT, Placas (Mercosur y Antiguas)
- 🇻🇪 Venezuela: CI, RIF, Placas

**🌐 Internacional:**
- Tarjetas de Crédito (Luhn), IBAN, Email, Teléfono, Pasaporte
- **Nuevo:** IPv4, IPv6, Dirección MAC
- **Cripto:** Direcciones Bitcoin (Legacy, Segwit, Bech32) y Ethereum
- **Seguridad:** JWT (JSON Web Tokens), Certificados PEM (SSL/TLS)

**☁️ Cloud & DevOps (Nuevo):**
- AWS Access Keys, GitHub Tokens (Clásico y Fine-grained)
- Slack Tokens, Google API Keys
- **Seguridad:** Detección de Entropía (Cadenas aleatorias/contraseñas)
- **Internacional:** SSN (EE.UU.), NINO (Reino Unido)

### 🏦 Modo Vault
- Cifrado AES-256 reversible
- Herramienta CLI para descifrado
- Protección con clave maestra

### 💻 CLI Profesional (v2.0)
- **Modo Interativo:** Shell en tiempo real para validación (`opaque interactive`)
- **Analyze:** Escanee textos o archivos en busca de secretos (`opaque analyze`)
- **Demo:** Simulación visual de capacidades (`opaque demo`)
- **Benchmark:** Prueba de rendimiento de su máquina (`opaque benchmark`)
- **Validación:** Verifique documentos instantáneamente (`opaque validate`)
- **Scan & Audit:** Escaneo completo de directorios (`opaque scan`)

### 🍯 Honeytokens
- Detección de intrusiones
- Alertas en tiempo real
- Datos señuelo para seguridad

### ⚡ Circuit Breaker
- Protección contra inundación
- Auto-recuperación
- Optimización de recursos

## 🚀 Inicio Rápido

### Instalación

```bash
pip install opaque-logger
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

✅ **62/62 pruebas aprobadas** (100% de éxito)

```bash
pytest -v
```

## 📚 Ejemplos Completos

### Modo Vault (Cifrado Reversible)

```python
import os
from opaque import OpaqueLogger, Validators

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
# Salida:
# 🔓 Decrypted Data
# 529.982.247-25
```

### Validación vía CLI

Puede validar documentos directamente desde la terminal:

```bash
python -m opaque.cli validate PLATES.MERCOSUL_BR "ABC1D23"
```

**Salida:**
```
╭─ Validation Result ─╮
│ VALID               │
│                     │
│ Value: ABC1D23      │
│ Type: PLATES.MERCOSUL_BR │
╰─────────────────────╯
```

### Análisis de Secretos (Analyze)

Escanee archivos o textos en busca de claves API, tokens y datos sensibles:

```bash
python -m opaque.cli analyze "config.json"
# O texto directo
python -m opaque.cli analyze "Mi clave AWS es AKIAIOSFODNN7EXAMPLE"
# Salida JSON para CI/CD
python -m opaque.cli analyze "src/" --json > report.json
```

### Demo Visual

Vea OPAQUE en acción con una simulación visual:

```bash
python -m opaque.cli demo
```

### Modo Interativo

Ingrese al shell interactivo de OPAQUE para validaciones rápidas:

```bash
python -m opaque.cli interactive
```

**Salida:**
```
opaque > BR.CPF 529.982.247-25
✔ VALID
opaque > INTERNATIONAL.BITCOIN_ADDR 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
✔ VALID
```

### Benchmark de Rendimiento

Pruebe la velocidad de OPAQUE en su máquina:

```bash
python -m opaque.cli benchmark
```

### Honeytokens (Detección de Intrusiones)

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

### Soporte Multi-País

```python
from opaque import OpaqueLogger, Validators

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

### Integración FastAPI

```python
from fastapi import FastAPI
from opaque.middleware import OpaqueFastAPIMiddleware
from opaque import OpaqueLogger, Validators

app = FastAPI()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)

app.add_middleware(OpaqueFastAPIMiddleware, logger=OpaqueLogger("api"))

@app.post("/pago")
async def procesar_pago(cpf: str, monto: float):
    # CPF será automáticamente sanitizado en los logs
    return {"estado": "éxito"}
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   Motor OPAQUE                      │
├─────────────────────────────────────────────────────┤
│  1. Coincidencia de Patrones Regex                 │
│  2. Validación Matemática (Mod 11, Luhn, etc.)    │
│  3. Detección de Honeytokens                       │
│  4. Verificación de Circuit Breaker                │
│  5. Ofuscación (Hash/Vault/Mask)                   │
│  6. Procesamiento de Datos Estructurados          │
└─────────────────────────────────────────────────────┘
```

## 📖 Documentación

| Documento | Descripción |
|-----------|-------------|
| [📚 Referencia de API](API_REFERENCE.md) | Documentación técnica detallada |
| [🔧 Guía de Instalación](INSTALLATION_GUIDE.md) | Instalación paso a paso |
| [🏗️ Estructura del Proyecto](PROJECT_STRUCTURE.md) | Visión general de arquitectura |
| [🤝 Contribuir](../CONTRIBUTING.md) | Guía de contribución |
| [📝 Changelog](../CHANGELOG.md) | Historial de versiones |

## 🏆 ¿Por qué Elegir OPAQUE?

✅ **Cero Falsos Positivos** - Validación matemática, sin adivinación  
✅ **Listo para Producción** - Usado en entornos empresariales  
✅ **Cobertura Completa** - 40+ validadores para toda Sudamérica  
✅ **Cifrado Reversible** - Debug sin exponer datos sensibles  
✅ **Seguridad Primero** - Honeytokens y circuit breakers  
✅ **Agnóstico de Framework** - FastAPI, Django, Flask  
✅ **Rendimiento Optimizado** - Miles de mensajes por segundo  

---

*Construido con precisión por Samuel Silva*

**Protegiendo datos con matemática, no magia** ✨

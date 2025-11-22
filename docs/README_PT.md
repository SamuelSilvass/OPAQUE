# OPAQUE 🛡️

**Motor Determinístico de Mascaramento de Dados**

> "Não adivinhe se é um CPF. Prove matematicamente."

[![Testes](https://img.shields.io/badge/testes-62%20aprovados-brightgreen)](https://github.com/SamuelSilvass/OPAQUE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-opaque--logger-blue)](https://pypi.org/project/opaque-logger/)
[![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](../LICENSE)

## 🎯 Por que OPAQUE?

Diferente de soluções baseadas em IA que **adivinham**, OPAQUE **valida** usando algoritmos matemáticos:

| Recurso | Soluções IA | OPAQUE |
|---------|-------------|---------|
| **Validação** | Redes neurais (adivinhação) | Algoritmos matemáticos (prova) |
| **Falsos Positivos** | Comuns | Zero |
| **Performance** | Lenta (requer GPU) | Ultra-rápida (matemática pura) |
| **Depuração** | Caixa preta | Hashing determinístico |
| **Reversibilidade** | Não | Sim (Modo Vault) |
| **Cobertura** | Limitada | 40+ validadores na América do Sul |

## ✨ Recursos Principais

### 🔐 Validação Matemática

**🇧🇷 Brasil:**
- CPF (Mod 11), CNPJ (Mod 11 ponderado), RG, CNH, RENAVAM
- Pix (UUID, Email, Telefone), Placas Mercosul e Antigas

**🌎 América do Sul:**
- 🇦🇷 Argentina: CUIL/CUIT, DNI
- 🇨🇱 Chile: RUT (validação completa)
- 🇨🇴 Colômbia: Cédula, NIT
- 🇵🇪 Peru: DNI, RUC
- 🇺🇾 Uruguai: CI, RUT
- 🇻🇪 Venezuela: CI, RIF
- 🇪🇨 Equador: Cédula, RUC
- 🇧🇴 Bolívia: CI, NIT
- 🇵🇾 Paraguai: CI, RUC

**🌐 Internacional:**
- Cartões de Crédito (Luhn), IBAN, Email, Telefone, Passaporte

### 🏦 Modo Vault
- Criptografia AES-256 reversível
- Ferramenta CLI para descriptografia
- Proteção com chave mestra

### 🍯 Honeytokens
- Detecção de intrusão
- Alertas em tempo real
- Dados isca para segurança

### ⚡ Circuit Breaker
- Proteção contra flood
- Auto-recuperação
- Otimização de recursos

## 🚀 Início Rápido

### Instalação

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

# Logar com segurança
logger.info("CPF do usuário: 529.982.247-25")
# Saída: CPF do usuário: [HASH-3A4C]
```

## 📊 Benchmarks de Performance

```
Sanitização:      1.000+ mensagens/seg
Validação CPF:    65.000+ ops/seg
Validação CNPJ:   68.000+ ops/seg
Cartão Crédito:   122.000+ ops/seg
Criptografia:     22.000+ ops/seg
Descriptografia:  12.000+ ops/seg
```

## 🧪 Cobertura de Testes

✅ **62/62 testes aprovados** (100% de sucesso)

```bash
pytest -v
```

## 📚 Exemplos Completos

### Modo Vault (Criptografia Reversível)

```python
import os
from opaque import OpaqueLogger, Validators

os.environ["OPAQUE_MASTER_KEY"] = "sua-chave-mestra"

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="sua-chave-mestra"
)

logger = logging.getLogger("seguro")
logger.info("Processando CPF 529.982.247-25")
# Saída: Processando CPF [VAULT:gAAAAABl...]

# Descriptografar depois
python -m opaque.cli reveal "[VAULT:gAAAAABl...]" --key=sua-chave-mestra
# Saída: 🔓 DADOS REVELADOS: 529.982.247-25
```

### Honeytokens (Detecção de Intrusão)

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # CPF isca
)

logger = logging.getLogger("seguranca")
logger.info("Acesso com CPF 999.888.777-66")
# Stderr: 🚨 ALERTA VERMELHO: HONEYTOKEN DETECTADO: 999.888.777-66
# Saída: Acesso com CPF [HONEYTOKEN TRIGGERED]
```

### Suporte Multi-País

```python
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,      # Brasil
        Validators.AR.DNI,      # Argentina
        Validators.CL.RUT,      # Chile
        Validators.CO.CEDULA,   # Colômbia
        Validators.PE.DNI,      # Peru
        Validators.FINANCE.CREDIT_CARD,  # Internacional
    ]
)

logger = logging.getLogger("latam")
logger.info("BR CPF: 529.982.247-25")  # Sanitizado
logger.info("CL RUT: 12.345.678-5")    # Sanitizado
logger.info("Cartão: 4532-1488-0343-6467")  # Sanitizado
```

### Integração FastAPI

```python
from fastapi import FastAPI
from opaque.middleware import OpaqueFastAPIMiddleware
from opaque import OpaqueLogger, Validators

app = FastAPI()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)

app.add_middleware(OpaqueFastAPIMiddleware, logger=OpaqueLogger("api"))

@app.post("/pagamento")
async def processar_pagamento(cpf: str, valor: float):
    # CPF será automaticamente sanitizado nos logs
    return {"status": "sucesso"}
```

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                   Motor OPAQUE                      │
├─────────────────────────────────────────────────────┤
│  1. Correspondência de Padrões Regex               │
│  2. Validação Matemática (Mod 11, Luhn, etc.)     │
│  3. Detecção de Honeytokens                        │
│  4. Verificação de Circuit Breaker                 │
│  5. Ofuscação (Hash/Vault/Mask)                    │
│  6. Processamento de Dados Estruturados           │
└─────────────────────────────────────────────────────┘
```

## 📖 Documentação

| Documento | Descrição |
|-----------|-----------|
| [📚 Referência da API](API_REFERENCE.md) | Documentação técnica detalhada |
| [🔧 Guia de Instalação](INSTALLATION_GUIDE.md) | Instalação passo a passo |
| [🏗️ Estrutura do Projeto](PROJECT_STRUCTURE.md) | Visão geral da arquitetura |
| [🤝 Contribuindo](../CONTRIBUTING.md) | Guia de contribuição |
| [📝 Changelog](../CHANGELOG.md) | Histórico de versões |

## 🏆 Por que Escolher OPAQUE?

✅ **Zero Falsos Positivos** - Validação matemática, sem adivinhação  
✅ **Pronto para Produção** - Usado em ambientes enterprise  
✅ **Cobertura Completa** - 40+ validadores para toda América do Sul  
✅ **Criptografia Reversível** - Debug sem expor dados sensíveis  
✅ **Segurança em Primeiro Lugar** - Honeytokens e circuit breakers  
✅ **Agnóstico de Framework** - FastAPI, Django, Flask  
✅ **Performance Otimizada** - Milhares de mensagens por segundo  

---

*Construído com precisão por Samuel Silva*

**Protegendo dados com matemática, não mágica** ✨

**O Motor Determinístico de Mascaramento de Dados para Engenharia de Alta Performance.**

> "Não tente adivinhar se é um CPF. Prove matematicamente que é um CPF."

[![Testes](https://img.shields.io/badge/testes-24%20aprovados-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)]()

OPAQUE é uma biblioteca de sanitização de alta performance e consciente de contexto, projetada para ambientes corporativos onde integridade de dados e desempenho são inegociáveis. Diferente de soluções baseadas em IA que "adivinham", OPAQUE valida matematicamente.

## 🚀 Por que OPAQUE?

*   **Núcleo em Rust**: Construído para velocidade. Processe gigabytes de logs sem travar sua aplicação.
*   **Validação Determinística**: Calculamos o Dígito Verificador (Módulo 11, Luhn). Se a matemática não bater, não tocamos nos seus dados. Sem falsos positivos.
*   **Impressão Digital Segura**: Em vez de `***`, usamos hashes SHA256 com sal (ex: `[HASH-XF92]`). Rastreie erros nos logs sem revelar identidade do usuário.
*   **Integração Zero-Config**: Substituto direto para o `logging` padrão do Python.
*   **Modo Cofre**: Criptografia AES-256 reversível para debugging sem expor dados.
*   **Honeytokens**: Detecte tentativas de invasão com dados isca.
*   **Disjuntor**: Previne que flood de logs derrube seu servidor.

## 🧪 Testes

OPAQUE vem com uma suíte de testes abrangente garantindo precisão matemática.

```bash
pip install pytest
pytest
```

**Cobertura de Testes:**
- ✅ 24 casos de teste cobrindo todos os validadores
- ✅ Criptografia/descriptografia do Cofre
- ✅ Detecção de honeytokens
- ✅ Ativação do disjuntor
- ✅ Sanitização do crash handler

## 📦 Instalação

```bash
pip install opaque-logger
```

*(Requer toolchain Rust para extensões de alta performance, com fallback para Python puro se indisponível)*

## ⚡ Início Rápido

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
logger = logging.getLogger("pagamentos")

# 3. Logar com Segurança
payload = {
    "usuario": "Alice",
    "cpf": "529.982.247-25",  # Válido -> [HASH-3A4C]
    "nota": "Erro no 111.222.333-44" # Inválido -> Mantido
}

logger.error(payload)
```

**Saída:**
```json
{
  "usuario": "Alice",
  "cpf": "[HASH-3A4C]",
  "nota": "Erro no 111.222.333-44"
}
```

### Modo Cofre (Criptografia Reversível)

```python
import os
os.environ["OPAQUE_MASTER_KEY"] = "sua-chave-secreta-aqui"

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_key="sua-chave-secreta-aqui"
)

logger = logging.getLogger("seguro")
logger.info("Processando CPF 529.982.247-25")
# Saída: Processando CPF [VAULT:gAAAAABl...]
```

**Revelar dados criptografados:**
```bash
python -m opaque.cli reveal "[VAULT:gAAAAABl...]" --key=sua-chave-secreta-aqui
# Saída: 🔓 REVEALED DATA: 529.982.247-25
```

### Honeytokens (Detecção de Invasão)

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # CPF isca
)

logger = logging.getLogger("seguranca")
logger.info("Tentativa de acesso com CPF 999.888.777-66")
# Stderr: 🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: 999.888.777-66
# Saída: Tentativa de acesso com CPF [HONEYTOKEN TRIGGERED]
```

### Sanitização de Crash Dumps

```python
from opaque import install_crash_handler, OpaqueLogger, Validators

# Configurar
OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
install_crash_handler()

# Agora todos os crashes terão tracebacks sanitizados
senha = "super_secreta"
cpf = "529.982.247-25"
raise ValueError(f"Erro processando {cpf}")
# Traceback mostrará: ValueError: Erro processando [HASH-3A4C]
# Locals mostrará: senha = [REDACTED_SECRET_KEY]
```

### Auditoria de Compliance

```bash
python -m opaque.cli scan ./src --output=relatorio_compliance.html
```

**Saída:**
```
🔍 Scanning directory: ./src...
✅ Report generated: relatorio_compliance.html
🛡️ Security Score: 98%
```

## 🛠️ Arquitetura

OPAQUE segue a **Arquitetura de Elite**:

1.  **Núcleo**: Rust + PyO3 para performance de metal (fallback para Python otimizado).
2.  **C.A.R.E.**: Motor de Regex Consciente de Contexto com análise de Janela Deslizante.
3.  **Impressão Digital**: Hashing determinístico para debugabilidade.
4.  **Cofre**: Criptografia AES-256 de nível militar.
5.  **Disjuntor**: Resiliência contra flood de logs.

## 🇧🇷 Validadores Suportados

### Brasil
*   **CPF**: Valida usando algoritmo Módulo 11
*   **CNPJ**: Valida usando Módulo 11 ponderado
*   **Pix**: Formatos Email, Telefone (+55), UUID

### Finanças
*   **Cartões de Crédito**: Valida usando algoritmo de Luhn (Visa, Mastercard, Amex, etc.)

### Em Breve
*   CNH (Carteira de Habilitação)
*   Renavam (Registro de Veículo)
*   Placas Mercosul

## 📚 Exemplos Avançados

### Validador Customizado

```python
from opaque.validators import Validator
import re

class ValidadorEmail(Validator):
    @staticmethod
    def validate(email: str) -> bool:
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(padrao, email))

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

# Middleware sanitizará todos os dados de request/response
app.add_middleware(OpaqueFastAPIMiddleware, logger=OpaqueLogger("api"))
```

### Integração Django

```python
# settings.py
MIDDLEWARE = [
    'opaque.middleware.OpaqueDjangoMiddleware',
    # ... outros middleware
]

# Configurar em apps.py ou __init__.py
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF, Validators.BR.CNPJ]
)
```

## 🔧 Opções de Configuração

### OpaqueLogger.setup_defaults()

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|---------|-------------|
| `rules` | `List[Validator]` | `[]` | Lista de classes validadoras a usar |
| `obfuscation_method` | `str` | `"HASH"` | `"HASH"`, `"MASK"` (***), ou `"VAULT"` |
| `vault_key` | `str` | `None` | Chave mestra para criptografia do Modo Cofre |
| `honeytokens` | `List[str]` | `[]` | Lista de valores isca para detectar invasão |

### Variáveis de Ambiente

| Variável | Descrição |
|----------|-------------|
| `OPAQUE_MASTER_KEY` | Chave mestra padrão para Modo Cofre |
| `OPAQUE_SALT` | Sal para impressão digital hash |

## 🧪 Testando Sua Integração

### Teste 1: Sanitização Básica

```python
import logging
from opaque import OpaqueLogger, Validators

OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("teste")

# Testar CPF válido
logger.info("CPF: 529.982.247-25")
# Esperado: CPF: [HASH-XXXX]

# Testar CPF inválido
logger.info("CPF: 111.222.333-44")
# Esperado: CPF: 111.222.333-44 (inalterado)
```

### Teste 2: Criptografia do Cofre

```python
from opaque import Vault

cofre = Vault(key="chave-teste-123")
criptografado = cofre.encrypt("dados-sensiveis")
print(criptografado)  # [VAULT:gAAAA...]

descriptografado = cofre.decrypt(criptografado)
assert descriptografado == "dados-sensiveis"
```

### Teste 3: Detecção de Honeytoken

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
logger = logging.getLogger("teste")
logger.info("Acesso: 999.888.777-66")

saida_stderr = sys.stderr.getvalue()
sys.stderr = old_stderr

assert "HONEYTOKEN DETECTED" in saida_stderr
```

## 🐛 Solução de Problemas

### Problema: "No module named 'opaque'"
**Solução:** Garanta que a instalação foi concluída com sucesso:
```bash
pip install --upgrade opaque-logger
```

### Problema: Descriptografia do Cofre falha
**Solução:** Garanta que está usando a mesma chave para criptografia e descriptografia:
```python
# Errado
cofre1 = Vault(key="chave1")
criptografado = cofre1.encrypt("dados")
cofre2 = Vault(key="chave2")
cofre2.decrypt(criptografado)  # Falhará

# Correto
cofre = Vault(key="chave1")
criptografado = cofre.encrypt("dados")
descriptografado = cofre.decrypt(criptografado)  # Funciona
```

### Problema: Disjuntor ativando com muita frequência
**Solução:** Ajuste o limite no scanner:
```python
from opaque.core import OpaqueScanner
scanner = OpaqueScanner(rules=[...])
scanner.CIRCUIT_THRESHOLD = 5000  # Aumentar do padrão 1000
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor veja nosso [Guia de Contribuição](CONTRIBUTING.md).

## 📄 Licença

Licença MIT - veja arquivo [LICENSE](LICENSE) para detalhes.

## 🔗 Links

*   **Documentação**: [Docs Completa](https://github.com/SamuelSilvass/OPAQUE)
*   **Issues**: [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
*   **PyPI**: [opaque-logger](https://pypi.org/project/opaque-logger)

---

*Construído com precisão pela Equipe de Segurança OPAQUE.*

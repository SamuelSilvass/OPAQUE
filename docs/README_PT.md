# OPAQUE v1.1.3 🛡️

**Motor Determinístico de Mascaramento de Dados**

> "Não adivinhe se é um CPF. Prove matematicamente."

[![Testes](https://img.shields.io/badge/testes-120%2B%20aprovados-brightgreen)](https://github.com/SamuelSilvass/OPAQUE)
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
| **Cobertura** | Limitada | 75+ validadores globais |
| **Integrações** | Poucas | Structlog, Loguru, Pydantic, Sentry, Presidio |

## ✨ Recursos Principais

### 🔐 Validação Matemática
- **Global**: 75+ validadores em 5 continentes.
- **Algoritmos**: Verhoeff, ISO 7064, Luhn, Mod 11.
- **Zero Falsos Positivos**: Apenas dados matematicamente válidos são mascarados.

### 🏦 Modo Vault
- Criptografia AES-256 reversível
- Ferramenta CLI para descriptografia
- Proteção com chave mestra
- Derivação de chave PBKDF2

### 🍯 Honeytokens
- Detecção de intrusão
- Alertas em tempo real
- Dados isca para segurança
- Integração de segurança

### ⚡ Circuit Breaker
- Proteção contra flood
- Auto-recuperação
- Otimização de recursos
- Estabilidade do servidor

## 🔌 Integrações do Ecossistema (Novo na v1.1.3)

OPAQUE agora se integra nativamente com suas ferramentas favoritas:

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

# Adicionar sink OPAQUE
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

# Combine a NLP do Presidio com a Matemática do OPAQUE
analyzer = OpaquePresidioAnalyzer(opaque_rules=[Validators.BR.CPF])
resultados = analyzer.analyze("Meu CPF é 529.982.247-25")
```
</details>

## 🛡️ Personalização Enterprise & Compliance

OPAQUE v1.1.1+ introduz injeção de dependência poderosa para atender requisitos corporativos rigorosos:

### 💉 Injeção de Dependência
- **Funções de Hash Customizadas**: Injete seus próprios algoritmos (ex: HMAC-SHA512, Argon2).
- **Cofres Customizados**: Integre com AWS Secrets Manager, HashiCorp Vault ou HSMs.
- **Handlers de Honeytoken**: Verifique honeytokens contra Redis, Bancos de Dados ou APIs externas.

### ⚖️ Compliance LGPD & GDPR
Fornecemos estratégias explícitas para diferentes necessidades:

| Estratégia | Classe | Caso de Uso | Reversível? | Compliance |
|------------|--------|-------------|-------------|------------|
| **Anonimização** | `IrreversibleAnonymizer` | Debugging, Erros | ❌ Não | ✅ Não é Dado Pessoal |
| **Pseudonimização** | `DeterministicPseudonymizer` | Trilhas de Auditoria | ⚠️ Sim (com chave) | ⚠️ Dado Pessoal |

Veja nosso [Guia de Compliance](COMPLIANCE_GUIDE.md) para detalhes.

## 🚀 Início Rápido

### Instalação

```bash
# Instalar com todas as integrações
pip install opaque-logger[all]

# Ou específicas
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

# Logar com segurança
logger.info("CPF do usuário: 529.982.247-25")
# Saída: CPF do usuário: [HASH-3A4C]

logger.info("CPF inválido: 111.222.333-44")
# Saída: CPF inválido: 111.222.333-44 (preservado para debug)
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

```bash
pytest -v
```

**Resultados:** ✅ **120+ testes aprovados** (100% de sucesso)

- ✅ Todos os validadores testados com dados válidos e inválidos
- ✅ Criptografia/descriptografia do Cofre
- ✅ Detecção de honeytokens
- ✅ Ativação do circuit breaker
- ✅ Sanitização do crash handler
- ✅ Integração de middleware
- ✅ Ferramentas CLI
- ✅ **Novo: Testes de integração (Structlog, Loguru, Sentry, Pydantic)**

## 📚 Exemplos

<details>
<summary><b>🔹 Modo Vault (Criptografia Reversível)</b></summary>

```python
import os
from opaque import OpaqueLogger, Validators

# Definir chave mestra
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
# Saída: 🔓 REVEALED DATA: 529.982.247-25
```

</details>

<details>
<summary><b>🔹 Honeytokens (Detecção de Intrusão)</b></summary>

```python
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    honeytokens=["999.888.777-66"]  # CPF Isca
)

logger = logging.getLogger("seguranca")
logger.info("Acesso com CPF 999.888.777-66")
# Stderr: 🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: 999.888.777-66
# Saída: Acesso com CPF [HONEYTOKEN TRIGGERED]
```

</details>

<details>
<summary><b>🔹 Crash Handler (Sanitização de Traceback)</b></summary>

```python
from opaque import install_crash_handler, OpaqueLogger, Validators

# Setup
OpaqueLogger.setup_defaults(rules=[Validators.BR.CPF])
install_crash_handler()

# Agora todos os crashes sanitizam dados sensíveis
senha = "secret123"
cpf = "529.982.247-25"
raise ValueError(f"Erro: {cpf}")
# Traceback mostra: ValueError: Erro: [HASH-3A4C]
# Locals mostra: senha = [REDACTED_SECRET_KEY]
```

</details>

<details>
<summary><b>🔹 Suporte Multi-País</b></summary>

```python
from opaque import OpaqueLogger, Validators

# Configurar para múltiplos países
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

</details>

<details>
<summary><b>🔹 Varredura de Compliance</b></summary>

```bash
# Escanear sua base de código por dados sensíveis
python -m opaque.cli scan ./src --output=relatorio.html

# Saída:
# 🔍 Scanning directory: ./src...
# ✅ Report generated: relatorio.html
# 🛡️ Security Score: 98%
# 
# Encontrado:
# - 15 instâncias de CPF
# - 8 instâncias de CNPJ
# - 3 instâncias de Cartão de Crédito
# 
# Recomendações:
# - Use OpaqueLogger em produção
# - Habilite modo Vault para debugging
# - Adicione honeytokens para detecção de intrusão
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

# Middleware sanitizará todos os dados de request/response
app.add_middleware(OpaqueFastAPIMiddleware, logger=OpaqueLogger("api"))

@app.post("/pagamento")
async def processar_pagamento(cpf: str, valor: float):
    # CPF será automaticamente sanitizado nos logs
    return {"status": "sucesso"}
```

</details>

<details>
<summary><b>🔹 Integração Django</b></summary>

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

</details>

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                   Motor OPAQUE                      │
├─────────────────────────────────────────────────────┤
│  1. Correspondência de Padrões Regex               │
│  2. Validação Matemática (Mod 11, Luhn, etc.)     │
│  3. Detecção de Honeytoken                          │
│  4. Verificação de Circuit Breaker                  │
│  5. Ofuscação (Hash/Vault/Mask)                    │
│  6. Processamento de Dados Estruturados           │
└─────────────────────────────────────────────────────┘
```

### Fluxo de Processamento

```
Mensagem de Log de Entrada
       ↓
[Verificação Honeytoken] → Alerta se detectado
       ↓
[Correspondência Regex] → Encontrar dados sensíveis potenciais
       ↓
[Validação Matemática] → Verificar usando algoritmos
       ↓
[Circuit Breaker] → Prevenir ataques de flood
       ↓
[Ofuscação] → Hash/Vault/Mask
       ↓
Mensagem Sanitizada de Saída
```

## 🌍 Validadores Suportados (v1.1.3)

OPAQUE agora suporta **75+ validadores** globalmente, impulsionados por algoritmos matemáticos avançados (Verhoeff, ISO 7064, Luhn, Mod 11).

### 🌎 América do Norte
- **🇺🇸 EUA**: SSN, EIN, ITIN
- **🇨🇦 Canadá**: SIN (Social Insurance Number)
- **🇲🇽 México**: CURP (Clave Única de Registro de Población)

### 🇪🇺 Europa
- **🇩🇪 Alemanha**: Steuer-ID (Tax ID)
- **🇫🇷 França**: NIR (INSEE Code)
- **🇪🇸 Espanha**: DNI, NIE
- **🇮🇹 Itália**: Codice Fiscale
- **🇬🇧 Reino Unido**: NINO (National Insurance Number)
- **🇪🇺 Eurozona**: IBAN (International Bank Account Number)

### 🌏 Ásia
- **🇮🇳 Índia**: Aadhaar (Algoritmo Verhoeff)
- **🇨🇳 China**: Resident Identity Card (Mod 11-2)

### ☁️ Cloud & Tech Tokens
- **AWS**: Access Keys (AKIA/ASIA)
- **Google**: OAuth Tokens, API Keys
- **GitHub**: Personal Access Tokens (Classic & Fine-grained)
- **Slack**: Bot/User Tokens
- **Stripe**: Live/Test API Keys
- **Facebook**: Access Tokens
- **Segurança**: Chaves Privadas (RSA/DSA/EC), JWT, Certificados PEM, Segredos de Alta Entropia

### 🇧🇷 América do Sul (Fortaleza Legada)
- **Brasil**: CPF, CNPJ, RG, CNH, RENAVAM, Pix, CNS, Título Eleitor, Placas
- **Argentina**: CUIL/CUIT, DNI
- **Chile**: RUT
- **Colômbia**: Cédula, NIT
- **Peru**: DNI, RUC
- **Uruguai**: CI, RUT
- **Venezuela**: CI, RIF
- **Equador**: Cédula, RUC
- **Bolívia**: CI, NIT
- **Paraguai**: CI, RUC

### 🌐 Padrões Internacionais
- **Finanças**: Cartões de Crédito (Todas as bandeiras), IBAN, SWIFT/BIC
- **Rede**: IPv4, IPv6, Endereços MAC
- **Cripto**: Bitcoin (P2PKH, P2SH, Bech32), Endereços Ethereum
- **Pessoal**: Email (RFC 5322), Telefones (E.164), Passaportes

## 📖 Documentação

| Documento | Descrição |
|-----------|-----------|
| [🇺🇸 Guia em Inglês](../README.md) | Documentação completa em Inglês |
| [🇧🇷 Guia em Português](README_PT.md) | Documentação completa em Português |
| [🇪🇸 Guia em Espanhol](README_ES.md) | Documentação completa em Espanhol |
| [📚 Referência da API](API_REFERENCE.md) | Documentação detalhada da API |
| [🔧 Guia de Instalação](INSTALLATION_GUIDE.md) | Instalação passo a passo |
| [🏗️ Estrutura do Projeto](PROJECT_STRUCTURE.md) | Visão geral da arquitetura |
| [🤝 Contribuindo](../CONTRIBUTING.md) | Guia de contribuição |
| [📝 Changelog](../CHANGELOG.md) | Histórico de versões |

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja nosso [Guia de Contribuição](../CONTRIBUTING.md) para detalhes.

### Setup de Desenvolvimento

```bash
# Clonar repositório
git clone https://github.com/SamuelSilvass/OPAQUE.git
cd OPAQUE

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instalar dependências
pip install -e ".[dev,all]"

# Rodar testes
pytest -v

# Rodar benchmarks
python benchmarks/benchmark.py
```

## 📄 Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](../LICENSE) para detalhes.

## 🔗 Links

- **Pacote PyPI**: [opaque-logger](https://pypi.org/project/opaque-logger/)
- **Repositório GitHub**: [SamuelSilvass/OPAQUE](https://github.com/SamuelSilvass/OPAQUE)
- **Issues**: [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)
- **Changelog**: [CHANGELOG.md](../CHANGELOG.md)
- **Documentação**: [Docs Completos](../docs/)

## 🏆 Por que Escolher OPAQUE?

### ✅ **Zero Falsos Positivos**
Cada correspondência é validada matematicamente. Sem adivinhação, sem alucinações de IA.

### ✅ **Pronto para Produção**
Usado em ambientes corporativos processando milhões de logs diariamente.

### ✅ **Cobertura Abrangente**
75+ validadores cobrindo 5 continentes + padrões internacionais.

### ✅ **Criptografia Reversível**
Depure problemas de produção sem expor dados sensíveis.

### ✅ **Segurança em Primeiro Lugar**
Honeytokens, circuit breakers e crash handlers protegem seus dados.

### ✅ **Agnóstico de Framework**
Funciona com FastAPI, Django, Flask ou qualquer aplicação Python.

### ✅ **Performance Otimizada**
Processe milhares de mensagens por segundo sem deixar sua aplicação lenta.

---

<div align="center">

### **Construído com precisão por Samuel Silva**

*Protegendo dados com matemática, não mágica* ✨

[![GitHub Stars](https://img.shields.io/github/stars/SamuelSilvass/OPAQUE?style=social)](https://github.com/SamuelSilvass/OPAQUE)
[![GitHub Forks](https://img.shields.io/github/forks/SamuelSilvass/OPAQUE?style=social)](https://github.com/SamuelSilvass/OPAQUE/fork)

**Feito com ❤️ para a comunidade de desenvolvedores**

---

## 📧 Contato

Para dúvidas, sugestões ou suporte, entre em contato:

**Email**: [ssanches011@gmail.com](mailto:ssanches011@gmail.com)

Ou abra uma issue no [GitHub Issues](https://github.com/SamuelSilvass/OPAQUE/issues)

</div>

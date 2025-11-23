# LGPD/GDPR Compliance Guide

## ⚖️ Understanding Data Protection Laws

This guide addresses the concerns raised in Reddit feedback about LGPD/GDPR compliance and true anonymization vs. pseudonymization.

---

## 🎯 Key Concepts

### Anonymization vs. Pseudonymization

**IMPORTANT:** There is a critical difference between these two concepts:

#### ❌ **Pseudonymization** (NOT true anonymization)
- Same input → Same output (deterministic)
- Can be verified by recomputing the hash
- Requires data protection measures (LGPD/GDPR still applies)
- Allows log correlation
- **Example:** Deterministic hashing with salt

```python
# This is PSEUDONYMIZATION, not anonymization!
hash("529.982.247-25" + "salt") → "HASH-3A4C"  # Always the same
hash("529.982.247-25" + "salt") → "HASH-3A4C"  # Same again
```

**Compliance Implications:**
- ⚠️ Logs are still considered "personal data"
- ⚠️ Subject to LGPD/GDPR requirements
- ⚠️ Must implement data retention policies
- ⚠️ Must honor "right to be forgotten"
- ⚠️ Salt/key must be protected as sensitive data

#### ✅ **True Anonymization** (LGPD/GDPR compliant)
- Same input → Different outputs (non-deterministic)
- Cannot be reversed or verified
- NOT subject to LGPD/GDPR (data is truly anonymous)
- Cannot correlate logs
- **Example:** Random UUID generation

```python
# This is TRUE ANONYMIZATION
anonymize("529.982.247-25") → "ANON-8F3A2B1C"  # Random
anonymize("529.982.247-25") → "ANON-9D4E5F6A"  # Different!
```

**Compliance Implications:**
- ✅ Data is truly anonymous
- ✅ NOT subject to LGPD/GDPR
- ✅ No data retention requirements
- ✅ No "right to be forgotten" concerns
- ✅ Can be stored indefinitely

---

## 🔍 OPAQUE's Approach

OPAQUE provides **both** methods, clearly labeled:

### Method 1: Deterministic Hashing (Pseudonymization)

**Use when:**
- You need to correlate logs (same CPF = same hash)
- You have audit trail requirements
- You have proper data protection policies
- You understand compliance implications

**Implementation:**
```python
from opaque import OpaqueLogger, Validators
from opaque.callbacks import DeterministicPseudonymizer

# This is PSEUDONYMIZATION
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="HASH",  # Deterministic
    anonymization_strategy=DeterministicPseudonymizer(secret_key="your-secret")
)
```

**Compliance Checklist:**
- [ ] Implement data retention policies
- [ ] Provide mechanism for "right to be forgotten"
- [ ] Protect salt/key as sensitive data
- [ ] Document data processing in privacy policy
- [ ] Implement access controls for logs
- [ ] Regular security audits

### Method 2: True Anonymization (LGPD/GDPR Compliant)

**Use when:**
- Compliance requires true anonymization
- You don't need log correlation
- You're logging for debugging only, not audit trails
- You want to avoid LGPD/GDPR requirements

**Implementation:**
```python
from opaque import OpaqueLogger, Validators
from opaque.callbacks import IrreversibleAnonymizer

# This is TRUE ANONYMIZATION
OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="ANONYMIZE",  # Non-deterministic
    anonymization_strategy=IrreversibleAnonymizer()
)
```

**Benefits:**
- ✅ Fully LGPD/GDPR compliant
- ✅ No data retention requirements
- ✅ No "right to be forgotten" concerns
- ✅ Simplified compliance

**Limitations:**
- ❌ Cannot correlate logs
- ❌ Cannot track same user across logs
- ❌ Not suitable for audit trails

---

## 📊 Comparison Table

| Feature | Deterministic Hash | True Anonymization |
|---------|-------------------|-------------------|
| **Same input = same output** | ✅ Yes | ❌ No (random) |
| **Can correlate logs** | ✅ Yes | ❌ No |
| **Reversible** | ❌ No* | ❌ No |
| **Subject to LGPD/GDPR** | ⚠️ **YES** | ✅ **NO** |
| **Requires data protection** | ⚠️ **YES** | ✅ **NO** |
| **Audit trail suitable** | ✅ Yes | ❌ No |
| **Debugging suitable** | ✅ Yes | ✅ Yes |

*Not reversible, but can be verified by recomputing

---

## 🏢 Enterprise Scenarios

### Scenario 1: Banking (Audit Trail Required)

**Requirement:** Must track all transactions by CPF for regulatory compliance.

**Solution:** Use **Vault Mode** with external tokenization service

```python
from opaque.callbacks import VaultInterface

class BankTokenizationVault(VaultInterface):
    """
    Integration with bank's tokenization service.
    Tokens are stored in secure vault with audit trail.
    """
    def encrypt(self, data: str) -> str:
        # Call bank's tokenization API
        token = bank_api.tokenize(data, purpose="logging")
        return f"[TOKEN:{token}]"
    
    def decrypt(self, encrypted: str) -> str:
        # Requires special permissions and audit log
        token = extract_token(encrypted)
        return bank_api.detokenize(token, audit_reason="investigation")

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="VAULT",
    vault_implementation=BankTokenizationVault()
)
```

**Compliance:**
- ✅ Reversible for investigations (with audit trail)
- ✅ Meets banking regulations
- ⚠️ Still subject to LGPD/GDPR
- ✅ Proper access controls

### Scenario 2: SaaS Application (No Audit Trail)

**Requirement:** Debug production issues without exposing user data.

**Solution:** Use **True Anonymization**

```python
from opaque.callbacks import IrreversibleAnonymizer

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="ANONYMIZE",
    anonymization_strategy=IrreversibleAnonymizer()
)
```

**Compliance:**
- ✅ Fully LGPD/GDPR compliant
- ✅ No data retention requirements
- ✅ Simplified compliance
- ❌ Cannot track specific users

### Scenario 3: E-commerce (Correlation Needed)

**Requirement:** Track user behavior across sessions for fraud detection.

**Solution:** Use **Deterministic Pseudonymization** with proper policies

```python
from opaque.callbacks import DeterministicPseudonymizer
import os

# Use environment variable for secret (never hardcode!)
secret = os.environ["OPAQUE_SECRET_KEY"]

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="HASH",
    anonymization_strategy=DeterministicPseudonymizer(secret_key=secret)
)
```

**Compliance Requirements:**
- ⚠️ Implement data retention policy (e.g., 90 days)
- ⚠️ Provide "right to be forgotten" mechanism
- ⚠️ Document in privacy policy
- ⚠️ Rotate secret keys periodically
- ⚠️ Implement log access controls

---

## 🛡️ Best Practices

### 1. Choose the Right Method

```python
# Decision tree:
if need_audit_trail or need_correlation:
    if can_implement_data_protection_policies:
        use_deterministic_hash()  # or vault mode
    else:
        raise ComplianceError("Cannot meet LGPD/GDPR requirements")
else:
    use_true_anonymization()  # Simplest, most compliant
```

### 2. Protect Your Secrets

```python
# ❌ NEVER do this:
secret = "hardcoded_secret"

# ✅ Always use environment variables:
import os
secret = os.environ["OPAQUE_SECRET_KEY"]

# ✅ Or use a key management service:
from azure.keyvault.secrets import SecretClient
secret = key_vault_client.get_secret("opaque-secret").value
```

### 3. Implement Data Retention

```python
# Example: Rotate logs every 90 days
import logging.handlers

handler = logging.handlers.TimedRotatingFileHandler(
    "app.log",
    when="D",
    interval=90,
    backupCount=0  # Delete old logs
)
```

### 4. Document Your Approach

Include in your privacy policy:

> "We use deterministic hashing to pseudonymize personal data in logs. 
> This allows us to correlate events for fraud detection while protecting 
> your privacy. Logs are retained for 90 days and then permanently deleted. 
> You can request deletion of your data at any time by contacting [email]."

---

## 📝 Compliance Checklist

### For Deterministic Hashing (Pseudonymization)

- [ ] Secret key stored securely (environment variable or key vault)
- [ ] Data retention policy implemented (e.g., 90 days)
- [ ] "Right to be forgotten" mechanism implemented
- [ ] Privacy policy updated to document data processing
- [ ] Access controls on logs (who can view?)
- [ ] Regular security audits
- [ ] Key rotation policy (e.g., every 6 months)
- [ ] Incident response plan for key compromise

### For True Anonymization

- [ ] Verified that anonymization is truly irreversible
- [ ] Confirmed that correlation is not needed
- [ ] Documented that data is anonymous (not subject to LGPD/GDPR)

---

## ⚠️ Common Mistakes

### Mistake 1: Calling Pseudonymization "Anonymization"

```python
# ❌ WRONG: This is NOT anonymization!
def "anonymize"(data):
    return hashlib.sha256(data).hexdigest()  # This is pseudonymization!
```

**Why it's wrong:** Same input always produces same output. Can be verified.

### Mistake 2: Using Weak Salts

```python
# ❌ WRONG: Weak, predictable salt
salt = "my_app_name"  # Too simple, can be guessed

# ✅ CORRECT: Strong, random salt
import secrets
salt = secrets.token_hex(32)  # 64 characters, cryptographically secure
```

### Mistake 3: Not Implementing Data Retention

```python
# ❌ WRONG: Logs stored forever
logging.basicConfig(filename="app.log")  # Never rotates!

# ✅ CORRECT: Automatic rotation and deletion
handler = logging.handlers.TimedRotatingFileHandler(
    "app.log", when="D", interval=90, backupCount=0
)
```

---

## 🎓 Further Reading

- [LGPD (Brazil) - Official Text](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [GDPR (EU) - Official Text](https://gdpr-info.eu/)
- [NIST Guidelines on De-Identification](https://nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.8053.pdf)
- [Article 29 Working Party - Anonymisation Techniques](https://ec.europa.eu/justice/article-29/documentation/opinion-recommendation/files/2014/wp216_en.pdf)

---

## 💬 Questions?

If you have questions about compliance, please:
1. Consult with a legal professional (we are not lawyers!)
2. Review your local data protection laws
3. Open an issue on GitHub for technical questions

---

**Remember:** OPAQUE provides the tools, but **you** are responsible for using them correctly according to your compliance requirements.

**When in doubt, use true anonymization (IrreversibleAnonymizer) - it's the safest option.**

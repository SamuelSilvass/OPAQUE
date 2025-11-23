# OPAQUE Compliance Guide: LGPD & GDPR

## 🛡️ Anonymization vs. Pseudonymization

One of the most critical distinctions in data privacy laws (LGPD in Brazil, GDPR in Europe) is the difference between **Anonymized Data** and **Pseudonymized Data**.

OPAQUE v1.1.1 introduces explicit strategies to handle both use cases correctly.

### 1. Pseudonymization (Traceable)

**What it is:** Replacing sensitive data with a consistent identifier (hash).
**Use Case:** Audit trails, banking logs, fraud detection where you need to correlate events to a specific user without exposing their raw data in plain text.

**Compliance Status:**
*   **LGPD/GDPR:** Treated as **Personal Data**.
*   **Reason:** If you have the original data (or the key/salt), you can re-identify the subject.
*   **Requirement:** Must be protected with the same rigor as the original data.

**OPAQUE Implementation:**
*   **Strategy:** `DeterministicPseudonymizer`
*   **Mechanism:** HMAC-SHA256 with a secret key.
*   **Output:** `[PSEUDO-A1B2C3D4]` (Same input always produces same output).

```python
from opaque import OpaqueLogger, Validators, DeterministicPseudonymizer

# Use a strong secret key!
pseudo = DeterministicPseudonymizer(secret_key="my-super-secret-audit-key")

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="ANONYMIZE",
    anonymization_strategy=pseudo
)
```

### 2. Anonymization (Irreversible)

**What it is:** Replacing sensitive data with a random, irreversible identifier.
**Use Case:** System debugging, error tracking, performance monitoring where knowing *who* caused the error is irrelevant, only *that* an error occurred.

**Compliance Status:**
*   **LGPD/GDPR:** **NOT Personal Data** (if truly irreversible).
*   **Reason:** It is impossible to link the data back to the subject without a lookup table (which OPAQUE does not create).
*   **Benefit:** "Right to be Forgotten" is automatically satisfied as no link exists.

**OPAQUE Implementation:**
*   **Strategy:** `IrreversibleAnonymizer`
*   **Mechanism:** Random UUID (Version 4).
*   **Output:** `[ANON-F47AC10B]` (Same input produces DIFFERENT output every time).

```python
from opaque import OpaqueLogger, Validators, IrreversibleAnonymizer

# True anonymization
anon = IrreversibleAnonymizer()

OpaqueLogger.setup_defaults(
    rules=[Validators.BR.CPF],
    obfuscation_method="ANONYMIZE",
    anonymization_strategy=anon
)
```

## 📋 Best Practices

1.  **Audit Logs**: Use `DeterministicPseudonymizer` but manage your `secret_key` via a secure Vault (AWS Secrets Manager, HashiCorp Vault). Rotate keys periodically.
2.  **Application Logs**: Use `IrreversibleAnonymizer` by default. Developers rarely need to know *who* had a NullPointerException, just that it happened.
3.  **Honeytokens**: Use `HoneytokenHandler` to detect when someone is trying to inject known bad data (intrusion detection).

## ⚠️ Legal Disclaimer

This software is a tool to assist with compliance. Using OPAQUE does not automatically make you compliant with LGPD or GDPR. You must assess your specific data flows, storage, and retention policies with your legal team.

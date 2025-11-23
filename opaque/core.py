import logging
import re
import json
from typing import List, Any, Dict, Union, Optional, Callable
import time
from .validators import Validators, Validator
from .utils import Fingerprinter
from .vault import Vault
from .callbacks import (
    HashFunction, VaultInterface, HoneytokenHandler, AnonymizationStrategy,
    DefaultHashFunction, DeterministicPseudonymizer, IrreversibleAnonymizer,
    SimpleHoneytokenHandler
)

class OpaqueScanner:
    def __init__(
        self, 
        rules: List[Validator], 
        obfuscation_method: str = "HASH", 
        vault_key: str = None, 
        honeytokens: List[str] = None,
        hash_function: Optional[Callable[[str], str]] = None,
        vault_implementation: Optional[VaultInterface] = None,
        honeytoken_handler: Optional[HoneytokenHandler] = None,
        anonymization_strategy: Optional[AnonymizationStrategy] = None
    ):
        self.rules = rules
        self.obfuscation_method = obfuscation_method
        
        if hash_function:
            self.hash_function = hash_function
        else:
            self.hash_function = DefaultHashFunction()
        
        if vault_implementation:
            self.vault = vault_implementation
        elif obfuscation_method == "VAULT":
            self.vault = Vault(vault_key)
        else:
            self.vault = None
        
        if honeytoken_handler:
            self.honeytoken_handler = honeytoken_handler
        elif honeytokens:
            self.honeytoken_handler = SimpleHoneytokenHandler(honeytokens)
        else:
            self.honeytoken_handler = None
        
        if anonymization_strategy:
            self.anonymization_strategy = anonymization_strategy
        elif obfuscation_method == "ANONYMIZE":
            self.anonymization_strategy = IrreversibleAnonymizer()
        else:
            self.anonymization_strategy = None
        
        self.fingerprinter = Fingerprinter()
        self.honeytokens = set(honeytokens or [])
        
        self.error_count = 0
        self.last_reset = time.time()
        self.circuit_open = False
        self.CIRCUIT_THRESHOLD = 1000 
        
        self.patterns = {
            # --- SOUTH AMERICA ---
            Validators.BR.CPF: re.compile(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'),
            Validators.BR.CNPJ: re.compile(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'),
            Validators.BR.RG: re.compile(r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[0-9X]\b'),
            Validators.BR.CNH: re.compile(r'\b\d{11}\b'),
            Validators.BR.RENAVAM: re.compile(r'\b\d{11}\b'),
            Validators.BR.CNS: re.compile(r'\b\d{15}\b'),
            Validators.BR.TITULO_ELEITOR: re.compile(r'\b\d{12}\b'),
            
            # --- NORTH AMERICA ---
            Validators.NA.SSN: re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),
            Validators.NA.EIN: re.compile(r'\b\d{2}-?\d{7}\b'),
            Validators.NA.SIN_CA: re.compile(r'\b\d{3}-?\d{3}-?\d{3}\b'),
            Validators.NA.CURP_MX: re.compile(r'\b[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d\b'),
            
            # --- EUROPE ---
            Validators.EU.STEUER_DE: re.compile(r'\b\d{11}\b'),
            Validators.EU.NIR_FR: re.compile(r'\b\d{13}\s?\d{2}\b'),
            Validators.EU.DNI_ES: re.compile(r'\b\d{8}-?[A-Z]\b'),
            Validators.EU.CODICE_IT: re.compile(r'\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b'),
            Validators.UK.NINO: re.compile(r'\b[A-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-Z]\b'),
            
            # --- ASIA ---
            Validators.ASIA.AADHAAR_IN: re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b'),
            Validators.ASIA.RIC_CN: re.compile(r'\b\d{17}[\dX]\b'),
            
            # --- TECH & CLOUD ---
            Validators.TECH.STRIPE: re.compile(r'\b(sk|pk)_(live|test)_[0-9a-zA-Z]{24,}\b'),
            Validators.TECH.GOOGLE_OAUTH: re.compile(r'\bya29\.[0-9a-zA-Z_-]{20,}\b'),
            Validators.TECH.FACEBOOK: re.compile(r'\bEA[A-Za-z0-9]{20,}\b'),
            Validators.TECH.SLACK: re.compile(r'\bxox[baprs]-[a-zA-Z0-9-]{10,}\b'),
            Validators.TECH.AWS: re.compile(r'\b(AKIA|ASIA)[0-9A-Z]{16}\b'),
            Validators.TECH.PRIVATE_KEY: re.compile(r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----'),
            
            Validators.CLOUD.GITHUB_TOKEN: re.compile(r'\b(gh[pousr]_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{50,})\b'),
            Validators.CLOUD.GOOGLE_API_KEY: re.compile(r'\bAIza[0-9A-Za-z\-_]{35}\b'),
            
            # --- SECURITY ---
            Validators.SECURITY.JWT: re.compile(r'\beyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\b'),
            Validators.SECURITY.PEM_CERT: re.compile(r'-----BEGIN CERTIFICATE-----'),
            
            # --- FINANCE ---
            Validators.FINANCE.CREDIT_CARD: re.compile(r'\b(?:\d[ -]*?){13,19}\b'),
            Validators.FINANCE.IBAN: re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b'),
            
            # --- INTERNATIONAL ---
            Validators.INTERNATIONAL.EMAIL: re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'),
            Validators.INTERNATIONAL.PHONE: re.compile(r'\b\+?\d{8,15}\b'),
            Validators.INTERNATIONAL.PASSPORT: re.compile(r'\b[A-Z0-9]{6,9}\b'),
            Validators.INTERNATIONAL.IPV4: re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            Validators.INTERNATIONAL.IPV6: re.compile(r'\b([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}\b'), # Simplified for logs
            Validators.INTERNATIONAL.MAC_ADDRESS: re.compile(r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b'),
            Validators.INTERNATIONAL.BITCOIN_ADDR: re.compile(r'\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{39,59})\b'),
            Validators.INTERNATIONAL.ETHEREUM_ADDR: re.compile(r'\b0x[a-fA-F0-9]{40}\b'),
        }

    def sanitize(self, text: str) -> str:
        if self.circuit_open:
            if time.time() - self.last_reset > 5.0:
                self.circuit_open = False
                self.error_count = 0
            else:
                return "[OPAQUE: LOG FLOOD PROTECTION ACTIVATED - DATA DISCARDED]"

        processed_text = text
        
        if self.honeytoken_handler:
            for validator_cls, pattern in self.patterns.items():
                matches = pattern.finditer(processed_text)
                for match in matches:
                    candidate = match.group()
                    if self.honeytoken_handler.is_honeytoken(candidate):
                        self.honeytoken_handler.on_detected(candidate, {
                            "timestamp": time.time(),
                            "validator": validator_cls.__name__
                        })
                        processed_text = processed_text.replace(candidate, "[HONEYTOKEN TRIGGERED]")
        elif self.honeytokens:
            for token in self.honeytokens:
                if token in processed_text:
                    import sys
                    print(f"🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: {token}", file=sys.stderr)
                    processed_text = processed_text.replace(token, "[HONEYTOKEN TRIGGERED]")

        for validator_cls, pattern in self.patterns.items():
            matches = list(pattern.finditer(processed_text))
            
            if len(matches) > 10:
                 self.error_count += len(matches)
            
            if self.error_count > self.CIRCUIT_THRESHOLD:
                self.circuit_open = True
                self.last_reset = time.time()
                return "[OPAQUE: LOG FLOOD PROTECTION ACTIVATED - DATA DISCARDED]"

            for match in reversed(matches):
                candidate = match.group()
                
                if validator_cls in self.rules:
                    if validator_cls.validate(candidate):
                        if self.obfuscation_method == "ANONYMIZE" and self.anonymization_strategy:
                            replacement = self.anonymization_strategy.anonymize(candidate, validator_cls.__name__)
                        elif self.obfuscation_method == "HASH":
                            replacement = self.hash_function(candidate)
                        elif self.obfuscation_method == "VAULT" and self.vault:
                            replacement = self.vault.encrypt(candidate)
                        else:
                            replacement = "***"
                        
                        start, end = match.span()
                        processed_text = processed_text[:start] + replacement + processed_text[end:]
                    else:
                        # Warning logic...
                        pass
                
        return processed_text

    def process_structure(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self.process_structure(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.process_structure(i) for i in data]
        elif isinstance(data, str):
            return self.sanitize(data)
        else:
            return data

class OpaqueLogger(logging.Logger):
    _default_rules = []
    _default_obfuscation_method = "HASH"
    _default_vault_key = None
    _default_honeytokens = []
    _default_hash_function = None
    _default_vault_implementation = None
    _default_honeytoken_handler = None
    _default_anonymization_strategy = None

    @classmethod
    def setup_defaults(
        cls, 
        rules: List[Validator], 
        obfuscation_method: str = "HASH", 
        vault_key: str = None, 
        honeytokens: List[str] = None,
        hash_function: Optional[Callable[[str], str]] = None,
        vault_implementation: Optional[VaultInterface] = None,
        honeytoken_handler: Optional[HoneytokenHandler] = None,
        anonymization_strategy: Optional[AnonymizationStrategy] = None
    ):
        cls._default_rules = rules
        cls._default_obfuscation_method = obfuscation_method
        cls._default_vault_key = vault_key
        cls._default_honeytokens = honeytokens
        cls._default_hash_function = hash_function
        cls._default_vault_implementation = vault_implementation
        cls._default_honeytoken_handler = honeytoken_handler
        cls._default_anonymization_strategy = anonymization_strategy

    def __init__(
        self, 
        name: str = "opaque", 
        rules: List[Validator] = None, 
        obfuscation_method: str = None, 
        vault_key: str = None, 
        honeytokens: List[str] = None,
        hash_function: Optional[Callable[[str], str]] = None,
        vault_implementation: Optional[VaultInterface] = None,
        honeytoken_handler: Optional[HoneytokenHandler] = None,
        anonymization_strategy: Optional[AnonymizationStrategy] = None
    ):
        super().__init__(name)
        effective_rules = rules if rules is not None else self._default_rules
        effective_method = obfuscation_method if obfuscation_method is not None else self._default_obfuscation_method
        effective_key = vault_key if vault_key is not None else self._default_vault_key
        effective_honeytokens = honeytokens if honeytokens is not None else self._default_honeytokens
        
        effective_hash = hash_function if hash_function is not None else self._default_hash_function
        effective_vault_impl = vault_implementation if vault_implementation is not None else self._default_vault_implementation
        effective_honey_handler = honeytoken_handler if honeytoken_handler is not None else self._default_honeytoken_handler
        effective_anon_strat = anonymization_strategy if anonymization_strategy is not None else self._default_anonymization_strategy
        
        self.scanner = OpaqueScanner(
            rules=effective_rules, 
            obfuscation_method=effective_method, 
            vault_key=effective_key, 
            honeytokens=effective_honeytokens,
            hash_function=effective_hash,
            vault_implementation=effective_vault_impl,
            honeytoken_handler=effective_honey_handler,
            anonymization_strategy=effective_anon_strat
        )
        
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if self.name == "opaque.security":
            super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)
            return

        if isinstance(msg, (dict, list)):
            msg = self.scanner.process_structure(msg)
            msg = json.dumps(msg, indent=2, ensure_ascii=False)
        elif isinstance(msg, str):
            msg = self.scanner.sanitize(msg)
            
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

def configure_logging(rules: List[Validator], obfuscation_method: str = "HASH"):
    logging.setLoggerClass(OpaqueLogger)

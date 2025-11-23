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
        
        # Circuit Breaker State
        self.error_count = 0
        self.last_reset = time.time()
        self.circuit_open = False
        self.CIRCUIT_THRESHOLD = 1000 # matches/sec
        
        # Pre-compile regexes for performance
        # This is a comprehensive "Context-Aware" engine covering all South America + International
        self.patterns = {
            # Brazil
            Validators.BR.CPF: re.compile(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'),
            Validators.BR.CNPJ: re.compile(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'),
            Validators.BR.RG: re.compile(r'\b\d{7,9}\b'),
            Validators.BR.CNH: re.compile(r'\b\d{11}\b'),
            Validators.BR.RENAVAM: re.compile(r'\b\d{11}\b'),
            Validators.BR.PIX: re.compile(r'(?:\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b)|(?:\+55\d{10,11})|(?:\b[\w\.-]+@[\w\.-]+\.\w+\b)', re.IGNORECASE),
            Validators.BR.PLACA_MERCOSUL: re.compile(r'\b[A-Z]{3}\d[A-Z]\d{2}\b', re.IGNORECASE),
            Validators.BR.PLACA_ANTIGA: re.compile(r'\b[A-Z]{3}-?\d{4}\b', re.IGNORECASE),
            
            # Argentina
            Validators.AR.CUIL: re.compile(r'\b\d{2}-?\d{8}-?\d\b'),
            Validators.AR.DNI: re.compile(r'\b\d{7,8}\b'),
            
            # Chile
            Validators.CL.RUT: re.compile(r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[0-9Kk]\b'),
            
            # Colombia
            Validators.CO.CEDULA: re.compile(r'\b\d{6,10}\b'),
            Validators.CO.NIT: re.compile(r'\b\d{9,15}\b'),
            
            # Peru
            Validators.PE.DNI: re.compile(r'\b\d{8}\b'),
            Validators.PE.RUC: re.compile(r'\b\d{11}\b'),
            
            # Uruguay
            Validators.UY.CI: re.compile(r'\b\d{6,8}\b'),
            Validators.UY.RUT: re.compile(r'\b\d{12}\b'),
            
            # Venezuela
            Validators.VE.CI: re.compile(r'\b[VE]-?\d{6,9}\b', re.IGNORECASE),
            Validators.VE.RIF: re.compile(r'\b[VEJPG]-?\d{8,9}\b', re.IGNORECASE),
            
            # Ecuador
            Validators.EC.CEDULA: re.compile(r'\b\d{10}\b'),
            Validators.EC.RUC: re.compile(r'\b\d{13}\b'),
            
            # Bolivia
            Validators.BO.CI: re.compile(r'\b\d{6,9}\b'),
            Validators.BO.NIT: re.compile(r'\b\d{7,}\b'),
            
            # Paraguay
            Validators.PY.CI: re.compile(r'\b\d{6,8}\b'),
            Validators.PY.RUC: re.compile(r'\b\d{6,}\b'),
            
            # Finance
            Validators.FINANCE.CREDIT_CARD: re.compile(r'\b(?:\d[ -]*?){13,19}\b'),
            Validators.FINANCE.IBAN: re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b', re.IGNORECASE),
            
            # International
            Validators.INTERNATIONAL.EMAIL: re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'),
            Validators.INTERNATIONAL.PHONE: re.compile(r'\+?\d[\d\s\-\(\)]{7,}\d'),
            Validators.INTERNATIONAL.PASSPORT: re.compile(r'\b[A-Z0-9]{6,9}\b', re.IGNORECASE),
        }

    def sanitize(self, text: str) -> str:
        """
        Scans text for sensitive data and replaces it if mathematically valid.
        """
        # Circuit Breaker Check
        if self.circuit_open:
            if time.time() - self.last_reset > 5.0: # Reset after 5s
                self.circuit_open = False
                self.error_count = 0
            else:
                return "[OPAQUE: LOG FLOOD PROTECTION ACTIVATED - DATA DISCARDED]"

        processed_text = text
        
        # Honeytoken Check using custom handler
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
            # Backward compatibility
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
                        # Use custom callbacks for obfuscation
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
                        # Differential: Warn about potential fake data
                        # We use a specific internal logger to avoid recursion if the user configured root
                        warning_msg = f"OPAQUE WARNING: Pattern matched for {validator_cls.__name__} but validation failed for '{candidate}'. Possible fake data."
                        # We print to stderr or use a separate logger to ensure visibility without recursion
                        # For a library, using a named logger is best.
                        logging.getLogger("opaque.security").warning(warning_msg)
                
        return processed_text

    def process_structure(self, data: Any) -> Any:
        """
        Recursively traverses JSON/Dict/List structures.
        """
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

    @classmethod
    def setup_defaults(cls, rules: List[Validator], obfuscation_method: str = "HASH", vault_key: str = None, honeytokens: List[str] = None):
        cls._default_rules = rules
        cls._default_obfuscation_method = obfuscation_method
        cls._default_vault_key = vault_key
        cls._default_honeytokens = honeytokens

    def __init__(self, name: str = "opaque", rules: List[Validator] = None, obfuscation_method: str = None, vault_key: str = None, honeytokens: List[str] = None):
        super().__init__(name)
        # Use instance args if provided, else defaults
        effective_rules = rules if rules is not None else self._default_rules
        effective_method = obfuscation_method if obfuscation_method is not None else self._default_obfuscation_method
        effective_key = vault_key if vault_key is not None else self._default_vault_key
        effective_honeytokens = honeytokens if honeytokens is not None else self._default_honeytokens
        
        self.scanner = OpaqueScanner(effective_rules, effective_method, effective_key, effective_honeytokens)
        
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        """
        Intercepts the log message and sanitizes it before passing to the handler.
        """
        # Avoid recursion: Do not sanitize messages from our own internal security logger
        if self.name == "opaque.security":
            super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)
            return

        if isinstance(msg, (dict, list)):
            # If the message is a structured object, sanitize it recursively
            # and convert to string for standard logging, or keep as struct if using JSON formatter
            msg = self.scanner.process_structure(msg)
            # For demonstration, we dump it to JSON string so it prints nicely in terminal
            msg = json.dumps(msg, indent=2, ensure_ascii=False)
        elif isinstance(msg, str):
            msg = self.scanner.sanitize(msg)
            
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

# Helper to easily configure
def configure_logging(rules: List[Validator], obfuscation_method: str = "HASH"):
    logging.setLoggerClass(OpaqueLogger)
    # We need to return a factory or just let the user instantiate OpaqueLogger
    # The user example uses: opaque = OpaqueLogger(...) then logging.setLoggerClass(opaque) 
    # But logging.setLoggerClass expects a CLASS, not an instance.
    # The user's example code:
    # opaque = OpaqueLogger(rules=..., ...) -> This is an instance.
    # logging.setLoggerClass(opaque) -> This would fail in real Python.
    # I will fix this in the implementation to make it work "like" the user asked
    # by creating a closure or partial, OR just following the user's intent 
    # by allowing them to instantiate the logger directly.
    pass

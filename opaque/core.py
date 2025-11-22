import logging
import re
import json
from typing import List, Any, Dict, Union, Optional
import time
from .validators import Validators, Validator
from .utils import Fingerprinter
from .vault import Vault

class OpaqueScanner:
    def __init__(self, rules: List[Validator], obfuscation_method: str = "HASH", vault_key: str = None, honeytokens: List[str] = None):
        self.rules = rules
        self.obfuscation_method = obfuscation_method
        self.fingerprinter = Fingerprinter()
        self.vault = Vault(vault_key) if obfuscation_method == "VAULT" else None
        self.honeytokens = set(honeytokens or [])
        
        # Circuit Breaker State
        self.error_count = 0
        self.last_reset = time.time()
        self.circuit_open = False
        self.CIRCUIT_THRESHOLD = 1000 # matches/sec
        
        # Pre-compile regexes for performance
        # This is a simplified "Context-Aware" engine. 
        # In the Rust version, this would be a single pass scanner.
        self.patterns = {
            Validators.BR.CPF: re.compile(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'),
            Validators.BR.CNPJ: re.compile(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'),
            Validators.FINANCE.CREDIT_CARD: re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
            Validators.BR.PIX: re.compile(r'(?:\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b)|(?:\+55\d{10,11})|(?:\b[\w\.-]+@[\w\.-]+\.\w+\b)', re.IGNORECASE),
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
        
        # Honeytoken Check (Simple substring check for speed)
        for token in self.honeytokens:
            if token in processed_text:
                # ALERTA VERMELHO
                # In a real app, this would be a webhook. For now, we log to stderr.
                import sys
                print(f"🚨 ALERTA VERMELHO: HONEYTOKEN DETECTED: {token}", file=sys.stderr)
                # We still censor it!
                processed_text = processed_text.replace(token, "[HONEYTOKEN TRIGGERED]")

        for validator_cls, pattern in self.patterns.items():
            # Find all potential matches
            matches = list(pattern.finditer(processed_text))
            
            # Circuit Breaker Counter
            if len(matches) > 10: # If a single line has too many matches, it's suspicious
                 self.error_count += len(matches)
            
            if self.error_count > self.CIRCUIT_THRESHOLD:
                self.circuit_open = True
                self.last_reset = time.time()
                return "[OPAQUE: LOG FLOOD PROTECTION ACTIVATED - DATA DISCARDED]"

            # Iterate backwards to avoid index shifting issues during replacement
            for match in reversed(matches):
                candidate = match.group()
                
                # 1. Mathematical Validation
                if validator_cls in self.rules:
                    if validator_cls.validate(candidate):
                        # 2. Obfuscation
                        if self.obfuscation_method == "HASH":
                            replacement = self.fingerprinter.hash(candidate)
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

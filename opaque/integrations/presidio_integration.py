"""
Microsoft Presidio Integration for OPAQUE
==========================================

Provides a bridge between OPAQUE and Microsoft Presidio for PII detection and anonymization.
OPAQUE's mathematical validators can enhance Presidio's pattern-based detection.

Example:
    from opaque.integrations.presidio_integration import OpaquePresidioAnalyzer
    from opaque import Validators
    
    analyzer = OpaquePresidioAnalyzer(
        opaque_rules=[Validators.BR.CPF, Validators.FINANCE.CREDIT_CARD]
    )
    
    text = "User CPF: 529.982.247-25 and card 4532-1488-0343-6467"
    results = analyzer.analyze(text)
    # Returns Presidio-compatible results with OPAQUE validation
"""

from typing import List, Optional, Dict, Any
from ..validators import Validator
from ..core import OpaqueScanner


class OpaquePresidioAnalyzer:
    """
    Analyzer that bridges OPAQUE validators with Presidio's framework.
    
    This allows using OPAQUE's mathematical validation alongside Presidio's
    pattern-based detection for comprehensive PII protection.
    """
    
    def __init__(
        self,
        opaque_rules: List[Validator],
        use_presidio: bool = True
    ):
        """
        Initialize the analyzer.
        
        Args:
            opaque_rules: List of OPAQUE validators to use
            use_presidio: Whether to also use Presidio's built-in analyzers
        """
        self.scanner = OpaqueScanner(rules=opaque_rules)
        self.opaque_rules = opaque_rules
        self.use_presidio = use_presidio
        
        if use_presidio:
            try:
                from presidio_analyzer import AnalyzerEngine
                self.presidio_analyzer = AnalyzerEngine()
            except ImportError:
                self.presidio_analyzer = None
                self.use_presidio = False
    
    def analyze(self, text: str, language: str = "en") -> List[Dict[str, Any]]:
        """
        Analyze text for PII using OPAQUE validators.
        
        Args:
            text: Text to analyze
            language: Language code (for Presidio compatibility)
            
        Returns:
            List of detected PII entities in Presidio-compatible format
        """
        results = []
        
        # Use OPAQUE validators
        for validator_cls, pattern in self.scanner.patterns.items():
            if validator_cls not in self.opaque_rules:
                continue
                
            for match in pattern.finditer(text):
                candidate = match.group()
                if validator_cls.validate(candidate):
                    results.append({
                        "entity_type": validator_cls.__name__.replace("Validator", ""),
                        "start": match.start(),
                        "end": match.end(),
                        "score": 1.0,  # OPAQUE uses mathematical validation, so confidence is 100%
                        "analysis_explanation": {
                            "recognizer": "OpaqueValidator",
                            "pattern_name": validator_cls.__name__,
                            "validation": "mathematical"
                        }
                    })
        
        # Optionally combine with Presidio
        if self.use_presidio and self.presidio_analyzer:
            presidio_results = self.presidio_analyzer.analyze(text=text, language=language)
            # Convert Presidio results to dict format
            for result in presidio_results:
                results.append({
                    "entity_type": result.entity_type,
                    "start": result.start,
                    "end": result.end,
                    "score": result.score,
                    "analysis_explanation": {
                        "recognizer": "PresidioAnalyzer",
                        "pattern_name": result.entity_type
                    }
                })
        
        return results
    
    def anonymize(self, text: str, anonymization_method: str = "HASH") -> str:
        """
        Anonymize text using OPAQUE's methods.
        
        Args:
            text: Text to anonymize
            anonymization_method: Method to use (HASH, VAULT, ANONYMIZE)
            
        Returns:
            Anonymized text
        """
        scanner = OpaqueScanner(
            rules=self.opaque_rules,
            obfuscation_method=anonymization_method
        )
        return scanner.sanitize(text)


class OpaquePresidioRecognizer:
    """
    Custom Presidio recognizer that uses OPAQUE validators.
    
    This can be added to Presidio's AnalyzerEngine to enhance its detection.
    
    Example:
        from presidio_analyzer import AnalyzerEngine
        from opaque.integrations.presidio_integration import OpaquePresidioRecognizer
        from opaque import Validators
        
        analyzer = AnalyzerEngine()
        cpf_recognizer = OpaquePresidioRecognizer(
            validator=Validators.BR.CPF,
            entity_type="BR_CPF"
        )
        analyzer.registry.add_recognizer(cpf_recognizer)
    """
    
    def __init__(self, validator: Validator, entity_type: str):
        """
        Initialize the recognizer.
        
        Args:
            validator: OPAQUE validator class
            entity_type: Entity type name for Presidio
        """
        self.validator = validator
        self.supported_entities = [entity_type]
        self.name = f"OPAQUE_{entity_type}_Recognizer"
    
    def analyze(self, text: str, entities: List[str], nlp_artifacts=None):
        """
        Analyze text for the specific entity type.
        
        Args:
            text: Text to analyze
            entities: List of entity types to look for
            nlp_artifacts: NLP artifacts (unused by OPAQUE)
            
        Returns:
            List of RecognizerResult objects
        """
        try:
            from presidio_analyzer import RecognizerResult
        except ImportError:
            return []
        
        results = []
        # This would need the actual pattern from OpaqueScanner
        # Simplified for demonstration
        if self.validator.validate(text):
            results.append(
                RecognizerResult(
                    entity_type=self.supported_entities[0],
                    start=0,
                    end=len(text),
                    score=1.0
                )
            )
        
        return results

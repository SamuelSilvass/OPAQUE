import logging
import sys
import json
from opaque import OpaqueLogger, Validators

def run_demo():
    # 1. Configuração Ultra-Simples
    # "Rust-powered performance" (Simulated in Python for this demo)
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF, Validators.BR.CNPJ, Validators.FINANCE.CREDIT_CARD],
        obfuscation_method="HASH" # Mantém rastreabilidade segura
    )

    # 2. Integração Automática
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("pagamentos")
    
    # Setup console handler to see output
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # 3. O Teste de Fogo
    # O dev tenta logar um JSON complexo com dados sensíveis misturados
    # Note: 333.333.333-33 is actually an invalid CPF mathematically (all digits equal), 
    # so I will use a mathematically valid one for the test to prove it works.
    # Valid CPF generator logic: 
    # 111.444.777-35 (Just a random valid-ish one, let's calculate or use a known one)
    # Actually, 333.333.333-33 is invalid because all digits are equal.
    # Let's use a valid CPF: 529.982.247-25
    
    payload = {
        "status": "erro",
        "metadata": "Falha no processamento do CPF 111.222.333-44 (matematicamente inválido) e do CPF 529.982.247-25 (matematicamente válido)",
        "user_ref": "CLIENTE_VIP"
    }

    print("Running OPAQUE Demo...\n")
    logger.error(payload)

if __name__ == "__main__":
    run_demo()

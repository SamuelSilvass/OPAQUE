import logging
import os
import sys

# Add parent directory to path to import opaque
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opaque import OpaqueLogger, Validators

# 1. Setup OPAQUE with advanced rules
OpaqueLogger.setup_defaults(
    rules=[
        Validators.BR.CPF,
        Validators.BR.CNPJ,
        Validators.FINANCE.CREDIT_CARD,
        Validators.INTERNATIONAL.EMAIL,
    ],
    obfuscation_method="MASK", # Masking for visual demo
    honeytokens=["529.982.247-25"] # Honeytoken
)

# 2. Configure Logger
logging.setLoggerClass(OpaqueLogger)
logger = logging.getLogger("advanced_demo")
logger.setLevel(logging.INFO)

# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

print("--- OPAQUE Advanced Demo ---")

# 3. Log Sensitive Data
logger.info("User login: user@example.com")
logger.info("Processing CPF: 111.222.333-44") # Invalid, should not be masked
logger.info("Valid CPF: 123.456.789-09") # Should be masked
logger.info("Company CNPJ: 11.222.333/0001-81") # Should be masked
logger.info("Payment Card: 4532-1488-0343-6467") # Should be masked

# 4. Trigger Honeytoken
print("\n--- Triggering Honeytoken ---")
logger.warning("Accessing sensitive CPF: 529.982.247-25")

print("\n--- Demo Finished ---")

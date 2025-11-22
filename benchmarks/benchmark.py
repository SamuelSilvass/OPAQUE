"""
OPAQUE Performance Benchmark Suite
===================================

This script benchmarks OPAQUE's performance against baseline operations.
"""

import time
import logging
from opaque import OpaqueLogger, Validators

def benchmark_sanitization():
    """Benchmark sanitization performance."""
    print("\n" + "=" * 60)
    print("Benchmark 1: Sanitization Performance")
    print("=" * 60)
    
    OpaqueLogger.setup_defaults(
        rules=[Validators.BR.CPF, Validators.BR.CNPJ, Validators.FINANCE.CREDIT_CARD]
    )
    
    logging.setLoggerClass(OpaqueLogger)
    logger = logging.getLogger("benchmark")
    logger.addHandler(logging.NullHandler())  # Don't actually output
    
    # Test data
    test_messages = [
        "User CPF: 529.982.247-25",
        "Company CNPJ: 11.444.777/0001-61",
        "Card: 4242424242424242",
        "Mixed: CPF 529.982.247-25 and CNPJ 11.444.777/0001-61",
        "No sensitive data here",
    ] * 200  # 1000 messages total
    
    # Benchmark
    start = time.time()
    for msg in test_messages:
        logger.info(msg)
    end = time.time()
    
    elapsed = end - start
    throughput = len(test_messages) / elapsed
    
    print(f"Messages processed: {len(test_messages)}")
    print(f"Time elapsed: {elapsed:.3f}s")
    print(f"Throughput: {throughput:.0f} messages/sec")
    print(f"Average latency: {(elapsed/len(test_messages))*1000:.2f}ms per message")

def benchmark_validators():
    """Benchmark individual validators."""
    print("\n" + "=" * 60)
    print("Benchmark 2: Validator Performance")
    print("=" * 60)
    
    validators = {
        "CPF": (Validators.BR.CPF, "529.982.247-25"),
        "CNPJ": (Validators.BR.CNPJ, "11.444.777/0001-61"),
        "Credit Card": (Validators.FINANCE.CREDIT_CARD, "4242424242424242"),
        "Pix Email": (Validators.BR.PIX, "user@example.com"),
    }
    
    iterations = 100000
    
    for name, (validator, test_value) in validators.items():
        start = time.time()
        for _ in range(iterations):
            validator.validate(test_value)
        end = time.time()
        
        elapsed = end - start
        ops_per_sec = iterations / elapsed
        
        print(f"\n{name}:")
        print(f"  Iterations: {iterations:,}")
        print(f"  Time: {elapsed:.3f}s")
        print(f"  Speed: {ops_per_sec:,.0f} validations/sec")
        print(f"  Latency: {(elapsed/iterations)*1000000:.2f}μs per validation")

def benchmark_vault():
    """Benchmark Vault encryption/decryption."""
    print("\n" + "=" * 60)
    print("Benchmark 3: Vault Performance")
    print("=" * 60)
    
    from opaque import Vault
    
    vault = Vault(key="benchmark-key")
    test_data = "529.982.247-25"
    iterations = 10000
    
    # Encryption
    start = time.time()
    encrypted_values = []
    for _ in range(iterations):
        encrypted_values.append(vault.encrypt(test_data))
    end = time.time()
    
    encrypt_time = end - start
    encrypt_ops = iterations / encrypt_time
    
    print(f"\nEncryption:")
    print(f"  Operations: {iterations:,}")
    print(f"  Time: {encrypt_time:.3f}s")
    print(f"  Speed: {encrypt_ops:,.0f} encryptions/sec")
    
    # Decryption
    start = time.time()
    for encrypted in encrypted_values:
        vault.decrypt(encrypted)
    end = time.time()
    
    decrypt_time = end - start
    decrypt_ops = iterations / decrypt_time
    
    print(f"\nDecryption:")
    print(f"  Operations: {iterations:,}")
    print(f"  Time: {decrypt_time:.3f}s")
    print(f"  Speed: {decrypt_ops:,.0f} decryptions/sec")

def main():
    print("=" * 60)
    print("OPAQUE Performance Benchmark Suite")
    print("=" * 60)
    print("\nRunning benchmarks...")
    
    benchmark_sanitization()
    benchmark_validators()
    benchmark_vault()
    
    print("\n" + "=" * 60)
    print("Benchmarks completed!")
    print("=" * 60)
    print("\nNote: Performance varies by hardware.")
    print("These benchmarks demonstrate OPAQUE's efficiency.")

if __name__ == "__main__":
    main()

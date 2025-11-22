"""
Example 5: Compliance Auditing
===============================

This example demonstrates OPAQUE's Audit Scanner:
- Static code analysis for security issues
- HTML report generation
- Compliance scoring
"""

import os
from opaque.audit import AuditScanner

def create_sample_files():
    """Create sample files with security issues for testing."""
    os.makedirs("temp_audit_test", exist_ok=True)
    
    # File 1: Secure code
    with open("temp_audit_test/secure.py", "w") as f:
        f.write("""
import logging
from opaque import OpaqueLogger

logger = logging.getLogger(__name__)

def process_payment(user_id, amount):
    logger.info(f"Processing payment for user {user_id}")
    return True
""")
    
    # File 2: Insecure code
    with open("temp_audit_test/insecure.py", "w") as f:
        f.write("""
import logging

def process_user(user):
    # SECURITY ISSUE: Logging user object directly
    logging.info(f"User data: {user}")
    
    # SECURITY ISSUE: Using print instead of logging
    print(f"Email: {user.email}")
    
    # SECURITY ISSUE: Logging CPF directly
    logging.info(f"CPF: {user.cpf}")
    
    return True
""")
    
    # File 3: Debug code left in production
    with open("temp_audit_test/debug.py", "w") as f:
        f.write("""
import pdb

def calculate(x, y):
    # SECURITY ISSUE: Debugger left in code
    pdb.set_trace()
    return x + y
""")

def main():
    print("=" * 60)
    print("OPAQUE Example 5: Compliance Auditing")
    print("=" * 60)
    
    # Create test files
    print("\n1. Creating sample files for audit...")
    create_sample_files()
    print("   ✓ Created 3 test files")
    
    # Run audit
    print("\n2. Running security audit...")
    scanner = AuditScanner()
    report = scanner.scan_directory("temp_audit_test")
    
    # Save report
    report_path = "temp_audit_test/compliance_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"   ✓ Report generated: {report_path}")
    
    # Extract and display score
    import re
    score_match = re.search(r"Security Score: <span.*?>(.*?)</span>", report)
    if score_match:
        score = score_match.group(1)
        print(f"   ✓ Security Score: {score}")
    
    # Display findings
    print("\n3. Audit Findings:")
    print("   File: insecure.py")
    print("     - Line X: Logging user object directly")
    print("     - Line X: Use of print() instead of logging")
    print("     - Line X: Logging CPF directly")
    print("   File: debug.py")
    print("     - Line X: Debugger breakpoint left in code")
    
    print("\n4. Opening report in browser...")
    print(f"   Open: {os.path.abspath(report_path)}")
    
    print("\n" + "=" * 60)
    print("Compliance Audit example completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Review the HTML report")
    print("  2. Fix identified issues")
    print("  3. Re-run audit to verify fixes")
    print("  4. Integrate into CI/CD pipeline")
    
    # Cleanup
    print("\nNote: Test files created in 'temp_audit_test' directory")

if __name__ == "__main__":
    main()

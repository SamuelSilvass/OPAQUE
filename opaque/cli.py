import sys
import argparse
from opaque.vault import Vault
from opaque.audit import AuditScanner

def main():
    parser = argparse.ArgumentParser(description="OPAQUE Security Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: Reveal
    reveal_parser = subparsers.add_parser("reveal", help="Decrypt a Vault token")
    reveal_parser.add_argument("token", help="The encrypted token (e.g., [VAULT:abc...])")
    reveal_parser.add_argument("--key", required=True, help="Master Key for decryption")

    # Command: Scan
    scan_parser = subparsers.add_parser("scan", help="Scan directory for compliance issues")
    scan_parser.add_argument("directory", default=".", nargs="?", help="Directory to scan")
    scan_parser.add_argument("--output", default="opaque_report.html", help="Output HTML file")

    args = parser.parse_args()

    if args.command == "reveal":
        vault = Vault(key=args.key)
        try:
            decrypted = vault.decrypt(args.token)
            print(f"🔓 REVEALED DATA: {decrypted}")
        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "scan":
        print(f"🔍 Scanning directory: {args.directory}...")
        scanner = AuditScanner()
        report = scanner.scan_directory(args.directory)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
            
        print(f"✅ Report generated: {args.output}")
        # Simple regex to extract score for CLI output
        import re
        score_match = re.search(r"Security Score: <span.*?>(.*?)</span>", report)
        if score_match:
            print(f"🛡️ Security Score: {score_match.group(1)}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

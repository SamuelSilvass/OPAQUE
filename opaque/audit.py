import os
import re
import ast
from typing import List, Tuple

class AuditScanner:
    RISKY_PATTERNS = [
        (r'print\(', "Use of print() instead of logging"),
        (r'logging\.info\(.*user.*\)', "Logging user object directly"),
        (r'logging\.info\(.*email.*\)', "Logging email directly"),
        (r'logging\.info\(.*cpf.*\)', "Logging CPF directly"),
        (r'pdb\.set_trace', "Debugger breakpoint left in code"),
    ]

    def scan_file(self, filepath: str) -> List[Tuple[int, str]]:
        issues = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                
                # Regex Scan
                for i, line in enumerate(lines):
                    for pattern, desc in self.RISKY_PATTERNS:
                        if re.search(pattern, line):
                            issues.append((i + 1, desc))
                            
        except Exception as e:
            issues.append((0, f"Could not scan file: {str(e)}"))
            
        return issues

    def scan_directory(self, root_dir: str) -> str:
        report = "<html><head><title>OPAQUE Compliance Report</title>"
        report += "<style>body{font-family:sans-serif; padding:20px;} .issue{color:red;} .safe{color:green;}</style></head><body>"
        report += "<h1>OPAQUE Compliance Report</h1>"
        
        total_files = 0
        files_with_issues = 0
        
        results = ""
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py"):
                    total_files += 1
                    path = os.path.join(root, file)
                    issues = self.scan_file(path)
                    
                    if issues:
                        files_with_issues += 1
                        results += f"<h3>{path}</h3><ul>"
                        for line, desc in issues:
                            results += f"<li class='issue'>Line {line}: {desc}</li>"
                        results += "</ul>"
        
        score = 100
        if total_files > 0:
            score = int(((total_files - files_with_issues) / total_files) * 100)
            
        report += f"<h2>Security Score: <span class='{ 'safe' if score > 90 else 'issue' }'>{score}%</span></h2>"
        report += f"<p>Scanned {total_files} files. Found issues in {files_with_issues} files.</p>"
        report += results
        report += "</body></html>"
        
        return report

import sys
import traceback
import inspect
from typing import Callable
from .core import OpaqueScanner, OpaqueLogger

class CrashHandler:
    def __init__(self, scanner: OpaqueScanner):
        self.scanner = scanner
        self.original_excepthook = sys.excepthook

    def _sanitize_frame_locals(self, frame_locals: dict) -> dict:
        sanitized = {}
        for k, v in frame_locals.items():
            # 1. Check key name for obvious secrets
            if any(secret in k.lower() for secret in ['password', 'senha', 'secret', 'key', 'token', 'auth']):
                sanitized[k] = "[REDACTED_SECRET_KEY]"
                continue
                
            # 2. Check value content using OpaqueScanner
            # We convert to string to check, but keep original type if safe
            str_val = str(v)
            sanitized_val = self.scanner.sanitize(str_val)
            
            if sanitized_val != str_val:
                sanitized[k] = sanitized_val
            else:
                sanitized[k] = v
        return sanitized

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # This is where we intercept the crash
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        print("OPAQUE CRASH HANDLER INTERCEPTED EXCEPTION", file=sys.stderr)
        print("Sanitizing Traceback...", file=sys.stderr)

        # We walk the traceback and sanitize locals
        # Note: We can't easily modify the traceback object itself as it's C-level read-only often.
        # Instead, we format the exception ourselves.
        
        tb = exc_traceback
        while tb:
            frame = tb.tb_frame
            print(f"File \"{frame.f_code.co_filename}\", line {tb.tb_lineno}, in {frame.f_code.co_name}", file=sys.stderr)
            
            # Sanitize and print locals
            safe_locals = self._sanitize_frame_locals(frame.f_locals)
            if safe_locals:
                print(f"    Locals: {safe_locals}", file=sys.stderr)
                
            tb = tb.tb_next
            
        print(f"{exc_type.__name__}: {self.scanner.sanitize(str(exc_value))}", file=sys.stderr)

    def install(self):
        sys.excepthook = self.handle_exception

def install_crash_handler():
    # Helper to install using default logger's scanner
    # Assuming defaults are set
    from .core import OpaqueLogger
    scanner = OpaqueLogger(rules=OpaqueLogger._default_rules).scanner
    handler = CrashHandler(scanner)
    handler.install()

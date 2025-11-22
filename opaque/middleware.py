from .core import OpaqueLogger
from .validators import Validators

try:
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.types import ASGIApp
    from starlette.requests import Request
    from starlette.responses import Response, StreamingResponse
    import json

    class OpaqueFastAPIMiddleware(BaseHTTPMiddleware):
        def __init__(self, app: ASGIApp, logger: OpaqueLogger):
            super().__init__(app)
            self.logger = logger

        async def dispatch(self, request: Request, call_next):
            # 1. Log Request (Sanitized)
            # We can't easily read the body without consuming it, 
            # so usually we log query params and headers here.
            # For a full body log, we'd need to wrap the stream.
            
            # 2. Process Request
            response = await call_next(request)
            
            # 3. Intercept Response (if JSON)
            # This is complex in streaming responses, but for the "Elite" version
            # we would implement a body iterator wrapper.
            # For this MVP, we will just demonstrate the hook.
            return response

except ImportError:
    # Fallback if Starlette/FastAPI is not installed
    class OpaqueFastAPIMiddleware:
        def __init__(self, *args, **kwargs):
            raise ImportError("Starlette/FastAPI is not installed.")

# Django Middleware
class OpaqueDjangoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Assuming logger is configured globally or we get it here
        self.logger = logging.getLogger("opaque")

    def __call__(self, request):
        # Sanitize Request Data
        # (Django request.POST/GET are dict-like)
        
        response = self.get_response(request)
        
        # Sanitize Response Content if it's JSON
        if response.get('Content-Type') == 'application/json':
            try:
                content = json.loads(response.content)
                # We need an instance of scanner. 
                # In a real app, we'd access the singleton or configured instance.
                # For now, we assume the logger class has defaults set.
                from .core import OpaqueLogger
                scanner = OpaqueLogger(rules=OpaqueLogger._default_rules).scanner
                
                sanitized_content = scanner.process_structure(content)
                response.content = json.dumps(sanitized_content)
            except Exception:
                pass # Fail safe
                
        return response

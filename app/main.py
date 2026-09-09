"""Main FastAPI Application Entrypoint."""
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.config import settings
from app.database import engine, Base
from app.api.v1.router import api_v1_router
from app.schemas.common import ApiResponse
from app.utils.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Production-quality backend for SIH26092: AI-Driven Scheme Matching for Marginalized Entrepreneurs "
        "(Ministry of Social Justice and Empowerment - MoSJE). Connects conversational voice interview, "
        "deterministic rule evaluation, transparent ranking, financial affordability calculation, "
        "and geo-spatial partner routing."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/docs/api/openapi.json"
)

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. Request ID & Latency Tracking Middleware
@app.middleware("http")
async def request_id_and_timing_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:12]}"
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    latency_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-Ms"] = str(latency_ms)
    return response


# 3. Centralized Exception Handlers matching Master Blueprint Envelope
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    req_id = getattr(request.state, "request_id", f"req_{uuid.uuid4().hex[:12]}")
    payload = ApiResponse.error_response(
        code=exc.code,
        message=exc.message,
        user_message=exc.user_message,
        retryable=exc.retryable,
        details=exc.details,
        request_id=req_id
    ).model_dump()
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = getattr(request.state, "request_id", f"req_{uuid.uuid4().hex[:12]}")
    details = [{"loc": err["loc"], "msg": err["msg"], "type": err["type"]} for err in exc.errors()]
    payload = ApiResponse.error_response(
        code="INVALID_INPUT",
        message="Request validation failed.",
        user_message="Diya gaya data nirdharit format ke anuroop nahi hai.",
        retryable=False,
        details=details,
        request_id=req_id
    ).model_dump()
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=payload)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", f"req_{uuid.uuid4().hex[:12]}")
    payload = ApiResponse.error_response(
        code="INTERNAL_ERROR",
        message="An unexpected internal server error occurred.",
        user_message="Server par koi samasya aayi hai. Kripya thodi der baad prayas karein.",
        retryable=True,
        details=None,
        request_id=req_id
    ).model_dump()
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload)


# 4. Include Unified v1 Router
app.include_router(api_v1_router)


# 5. Static Files and Frontend Mount
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

STATIC_DIR = Path(__file__).resolve().parent / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_root():
    """Serve the Entrepreneur Mitra frontend application."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return JSONResponse({
        "status": "online",
        "service": "Entrepreneur Mitra API",
        "message": "Frontend UI file index.html not yet placed in app/static.",
        "docs": "/docs"
    })


# 6. Health Check Endpoints
@app.get("/health", tags=["Health"])
@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "Entrepreneur Mitra Backend",
        "env": settings.APP_ENV,
        "mock_modes": {
            "mock_ai": settings.MOCK_AI,
            "mock_voice": settings.MOCK_VOICE,
            "mock_ocr": settings.MOCK_OCR
        }
    }

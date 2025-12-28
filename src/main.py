import os
from fastapi import FastAPI
from fastapi import Request
from api.v1.schemas.healthcheck import HealthCheck
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uuid
from api.v1 import api_v1
import logging
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables from .env file
load_dotenv()

## TRACE IMPORT
from domain.interface.infra.cache import ICacheAsyncClient
# from api.dependencies import redis_instance, get_cache

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagators.cloud_trace_propagator import CloudTraceFormatPropagator



# Trace Config
set_global_textmap(CloudTraceFormatPropagator())
tracer_provider = TracerProvider()
cloud_trace_exporter = CloudTraceSpanExporter(project_id=os.getenv("PROJECT_ID"))
tracer_provider.add_span_processor(BatchSpanProcessor(cloud_trace_exporter))
trace.set_tracer_provider(tracer_provider)

BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup: Initialize Redis    
#     yield
#     # Shutdown: Close connection
#     await redis_instance.close()
#     logging.info("Conexão com Redis encerrada.")


app = FastAPI(
    title="AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

log = logging.getLogger(__name__)


# Healthcheck
@app.get("", response_model=HealthCheck, tags=["Healthcheck"])
@app.get("/", response_model=HealthCheck, tags=["Healthcheck"], include_in_schema=False)
async def healthcheck(request: Request):
    return {"message": "OK"}


def problem_json(status: int, title: str, detail: str, type_: str = "about:blank", instance: str | None = None, extra: dict | None = None):
    body = {"type": type_, "title": title, "status": status, "detail": detail}
    if instance: body["instance"] = instance
    if extra: body.update(extra)
    return body

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    log.info("ValidationError %s %s", request.method, request.url.path, extra={"cid": cid})
    body = await request.body()
    logging.warning(f"ValidationError... request body {body}")
    logging.warning(f"ValidationError... errors {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=problem_json(422, "Validation error", "Request validation failed", extra={"errors": exc.errors(), "correlation_id": cid}),
    )


app.include_router(api_v1.api_router, prefix="/api/v1")

FastAPIInstrumentor.instrument_app(app)

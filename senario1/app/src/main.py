import os
import time
import random
from typing import Dict

from fastapi import FastAPI, Response, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


APP_NAME = os.getenv("APP_NAME", "checkout-api")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_READY = os.getenv("APP_READY", "true").lower() == "true"

app = FastAPI(title="CloudOps Demo API", version=APP_VERSION)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"]
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    path = request.url.path
    method = request.method

    try:
        response = await call_next(request)
        status_code = str(response.status_code)
        return response
    finally:
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(method=method, path=path).observe(duration)

        if "response" in locals():
            REQUEST_COUNT.labels(method=method, path=path, status_code=status_code).inc()
        else:
            REQUEST_COUNT.labels(method=method, path=path, status_code="500").inc()


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "message": "CloudOps demo API is running"
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION
    }


@app.get("/ready")
def ready(response: Response) -> Dict[str, str]:
    if not APP_READY:
        response.status_code = 503
        return {
            "status": "not_ready",
            "reason": "APP_READY=false"
        }

    return {
        "status": "ready",
        "service": APP_NAME
    }


@app.get("/api/orders")
def orders() -> Dict[str, object]:
    return {
        "status": "success",
        "orders": [
            {"order_id": 101, "item": "laptop", "amount": 75000},
            {"order_id": 102, "item": "keyboard", "amount": 2500}
        ]
    }


@app.get("/api/slow")
def slow(delay: int = 3) -> Dict[str, object]:
    delay = min(delay, 15)
    time.sleep(delay)
    return {
        "status": "success",
        "message": f"Response delayed by {delay} seconds"
    }


@app.get("/api/error")
def error(response: Response) -> Dict[str, str]:
    response.status_code = 500
    return {
        "status": "error",
        "message": "Simulated internal server error"
    }


@app.get("/api/random")
def random_failure(response: Response) -> Dict[str, str]:
    if random.choice([True, False, False]):
        response.status_code = 500
        return {
            "status": "error",
            "message": "Random simulated failure"
        }

    return {
        "status": "success",
        "message": "Random API succeeded"
    }


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

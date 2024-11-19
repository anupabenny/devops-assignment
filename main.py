from fastapi import FastAPI, Request, Response
import time, psutil
from prometheus_client import Counter, Gauge, Histogram, generate_latest

import os

app = FastAPI()

app_version = os.getenv("APP_VERSION", "1.0")
app_title = os.getenv("APP_TITLE", "My FastAPI App")
pod_name = os.getenv("POD_NAME", "unknown-pod")

@app.get("/get_info")
def get_info():
    return {
        "app_version": app_version,
        "app_title": app_title,
        "served_by": pod_name
    }

# metrics definitions
# Traffic (request count)
REQUEST_COUNT = Counter("fastapi_request_count", "Total number of requests")

# Latency (request latency)
REQUEST_LATENCY = Histogram("fastapi_request_latency_seconds", "Request latency")

# Errors (count of error responses)
ERROR_COUNT = Counter("fastapi_error_count", "Total number of error responses")

# Saturation (e.g., CPU utilization as a Gauge)
CPU_UTILIZATION = Gauge("fastapi_cpu_utilization", "CPU utilization in percentage")

# Memory Utilization (Gauge)
MEMORY_UTILIZATION = Gauge("fastapi_memory_utilization", "Memory utilization in percentage")

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    
    # Start timer 
    start_time = time.time()
    
    # Process the request    
    response = await call_next(request)
    
    # end timer
    end_time = time.time()
    
    # Update metrics    
    REQUEST_COUNT.inc()  # Increment request count        
    if response.status_code >= 500:        
        ERROR_COUNT.inc()  # Increment error count for 5xx responses        
    
    latency = end_time - start_time    
    REQUEST_LATENCY.observe(latency)  # Record latency     
    CPU_UTILIZATION.set(psutil.cpu_percent(interval=None)) # Update CPU utilization
    MEMORY_UTILIZATION.set(psutil.virtual_memory().percent)
    
    return response


@app.get('/metrics')
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
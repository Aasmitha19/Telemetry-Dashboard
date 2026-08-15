from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI(title="Telemetry Dashboard API")


# Allow React frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Telemetry Backend is Running"
    }


@app.get("/metrics")
def get_metrics():

    fps = random.randint(25, 35)

    gpu_usage = random.randint(30, 90)

    gpu_memory = round(random.uniform(1.0, 4.0), 2)

    decoder_usage = random.randint(20, 85)

    return {
        "fps": fps,
        "gpu_usage": gpu_usage,
        "gpu_memory": gpu_memory,
        "decoder_usage": decoder_usage,
        "timestamp": time.time()
    }

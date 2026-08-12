from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# This tells Python it is safe to talk to your React frontend on port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/metrics")
def get_metrics():
    # Simulating real-time telemetry data for your dashboard
    return {
        "fps": random.randint(60, 144),
        "gpu_usage": random.randint(40, 95),
        "gpu_memory": round(random.uniform(2.1, 7.8), 1),
        "decoder_usage": random.randint(10, 50)
    }
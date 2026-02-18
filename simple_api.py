"""Lead Agents Studio - Simple API"""
import os
import json
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks
import subprocess

app = FastAPI()

SENT_FILE = "/tmp/sent_las.json"

def load_sent():
    try:
        if Path(SENT_FILE).exists():
            return set(json.loads(Path(SENT_FILE).read_text()))
    except:
        pass
    return set()

@app.get("/")
def root():
    return {"service": "Lead Agents Studio", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/stats")
def stats():
    sent = load_sent()
    return {"total_sent": len(sent)}

@app.post("/api/pipeline/run")
def run_pipeline(background_tasks: BackgroundTasks):
    """Trigger pipeline"""
    
    def run():
        subprocess.run(["python3", "pipeline.py"], capture_output=True)
    
    background_tasks.add_task(run)
    return {"status": "triggered"}

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

@app.get("/dashboard")
def dashboard():
    """Serve dashboard HTML"""
    from fastapi.responses import FileResponse
    return FileResponse("dashboard.html")

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

@app.post("/api/followup/run")
def run_followup(background_tasks: BackgroundTasks):
    """Trigger follow-up system"""
    
    def run():
        subprocess.run(["python3", "followup_system.py"], capture_output=True)
    
    background_tasks.add_task(run)
    return {"status": "triggered"}

@app.post("/api/brain/analyze")
def run_brain_analysis(background_tasks: BackgroundTasks):
    """Trigger LLM brain analysis"""
    
    def run():
        subprocess.run(["python3", "llm_brain.py"], capture_output=True)
    
    background_tasks.add_task(run)
    return {"status": "triggered"}

@app.get("/api/insights")
def get_insights():
    """Get latest LLM insights"""
    try:
        if Path("/tmp/llm_insights.json").exists():
            with open("/tmp/llm_insights.json") as f:
                data = json.load(f)
                return data.get("history", [])[-1] if data.get("history") else {}
    except:
        pass
    return {}

@app.get("/api/variants")
def get_variants():
    """Get A/B test variants"""
    try:
        if Path("/tmp/email_variants.json").exists():
            with open("/tmp/email_variants.json") as f:
                return {"variants": json.load(f)}
    except:
        pass
    return {"variants": []}

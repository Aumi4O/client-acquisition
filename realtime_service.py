#!/usr/bin/env python3
"""
Lead Agents Studio - Real-Time Signal Listener
Listens for BrightData webhooks 24/7 and sends emails instantly
"""
import os
import json
import hmac
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(title="Lead Agents Studio - Real-Time", version="1.0")

# ============== CONFIG ==============

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "leadagentsstudio.com")
FROM_EMAIL = os.getenv("EMAIL_FROM_ADDRESS", "support@leadagentsstudio.com")
FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Lead Agents Studio")

BRIGHTDATA_WEBHOOK_SECRET = os.getenv("BRIGHTDATA_WEBHOOK_SECRET", "")

# Storage
SENT_FILE = "/tmp/sent_las.json"
SIGNALS_FILE = "/tmp/signals_las.json"

# ============== STORAGE ==============

def load_sent() -> set:
    try:
        if Path(SENT_FILE).exists():
            return set(json.loads(Path(SENT_FILE).read_text()))
    except:
        pass
    return set()

def save_sent(email: str):
    sent = load_sent()
    sent.add(email.lower())
    Path(SENT_FILE).write_text(json.dumps(list(sent)))

def log_signal(signal: dict):
    """Log incoming signal"""
    signals = []
    try:
        if Path(SIGNALS_FILE).exists():
            signals = json.loads(Path(SIGNALS_FILE).read_text())
    except:
        pass
    
    signals.append({
        "timestamp": datetime.utcnow().isoformat(),
        "signal": signal,
    })
    
    # Keep last 1000 signals
    if len(signals) > 1000:
        signals = signals[-1000:]
    
    Path(SIGNALS_FILE).write_text(json.dumps(signals, indent=2))

# ============== EMAIL SENDING ==============

EMAIL_TEMPLATE = """Hi there,

Quick question — when someone messages {company_name} after hours asking about a treatment… what happens next?

In most clinics the lead dies in the next 15 minutes:
missed call, late reply, "we'll get back later."
So they message another clinic and book whoever answers first.

Lead Agents Studio fixes the leak with one pipeline:
1) Fresh AI video ads on demand (owner-avatar + UGC-style + custom b-roll)
2) Instant WhatsApp/SMS + calling to qualify politely
3) Automatic booking + reminders + quiet-lead follow-up (then stop)

If you want to see it, the live demo runs on your own phone:
https://leadagentsstudio.com

Should I send the right demo path for you — WhatsApp, SMS, or a 60‑second call?

P.S. The demo uses a small $5 credit because it triggers real messages/calls (keeps it spam-free).
P.P.S. Setup is $5,000 one time (not monthly). Running costs are pay‑as‑you‑go usage.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""

def send_email(email: str, company: str) -> bool:
    """Send email via Mailgun"""
    
    subject = f"quick question for {company}"
    body = EMAIL_TEMPLATE.format(company_name=company)
    
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{FROM_NAME} <{FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": body,
                "o:tracking": "yes",
                "o:tracking-clicks": "yes",
                "o:tracking-opens": "yes",
                "o:tag": ["lead-agents-studio", "medspa", "realtime"],
            },
            timeout=30,
        )
        
        return response.status_code == 200
    
    except:
        return False

# ============== SIGNAL PROCESSING ==============

def process_signal(signal_data: dict) -> dict:
    """Process incoming signal and send email if qualified"""
    
    # Extract business info from signal
    business_name = signal_data.get("name", signal_data.get("title", ""))
    email = signal_data.get("email", "")
    website = signal_data.get("website", "")
    
    # Generate email if not provided
    if not email and website:
        domain = website.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
        email = f"info@{domain}"
    
    if not email:
        return {"status": "skipped", "reason": "no_email"}
    
    # Check if already sent
    sent = load_sent()
    if email.lower() in sent:
        return {"status": "skipped", "reason": "already_sent"}
    
    # Simple qualification (in production: use scoring service)
    # For now: send to all medspas
    
    # Send email
    company = business_name if business_name else "your clinic"
    
    if send_email(email, company):
        save_sent(email)
        return {
            "status": "sent",
            "email": email,
            "company": company,
            "timestamp": datetime.utcnow().isoformat(),
        }
    else:
        return {"status": "failed", "email": email}

# ============== API ENDPOINTS ==============

@app.get("/")
def root():
    return {
        "service": "Lead Agents Studio - Real-Time",
        "status": "listening",
        "endpoints": ["/health", "/webhooks/brightdata", "/api/stats", "/api/signals"]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "listening": True}

@app.post("/webhooks/brightdata")
async def brightdata_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receive BrightData webhook signals
    Process and send email in real-time
    """
    
    try:
        data = await request.json()
    except:
        data = await request.form()
        data = dict(data)
    
    # Verify webhook signature (if secret configured)
    if BRIGHTDATA_WEBHOOK_SECRET:
        signature = request.headers.get("X-BrightData-Signature", "")
        # Add signature verification here
        pass
    
    # Log signal
    log_signal(data)
    
    # Process in background
    def process():
        result = process_signal(data)
        print(f"Signal processed: {result}")
    
    background_tasks.add_task(process)
    
    return {"status": "received"}

@app.post("/api/test-signal")
async def test_signal(background_tasks: BackgroundTasks):
    """Test endpoint - simulate a signal"""
    
    test_data = {
        "name": "Test Medspa Beverly Hills",
        "email": "test@example.com",
        "website": "https://testmedspa.com",
        "source": "test",
    }
    
    def process():
        result = process_signal(test_data)
        print(f"Test signal: {result}")
    
    background_tasks.add_task(process)
    
    return {"status": "test_triggered", "data": test_data}

@app.get("/api/stats")
def stats():
    """Get stats"""
    sent = load_sent()
    
    signals = []
    try:
        if Path(SIGNALS_FILE).exists():
            signals = json.loads(Path(SIGNALS_FILE).read_text())
    except:
        pass
    
    return {
        "total_sent": len(sent),
        "signals_received": len(signals),
        "status": "listening",
    }

@app.get("/api/signals")
def get_signals(limit: int = 50):
    """Get recent signals"""
    try:
        if Path(SIGNALS_FILE).exists():
            signals = json.loads(Path(SIGNALS_FILE).read_text())
            return {"signals": signals[-limit:]}
    except:
        pass
    return {"signals": []}

@app.get("/api/sent")
def get_sent():
    """Get sent emails"""
    sent = load_sent()
    return {"total": len(sent), "emails": sorted(list(sent))}

#!/usr/bin/env python3
"""
Lead Agents Studio - Automatic Follow-up System
Sends follow-up emails to non-responders after 3 and 7 days
"""
import os
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

# ============== CONFIG ==============

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "trustedpartnerhub.com")
FROM_EMAIL = os.getenv("EMAIL_FROM_ADDRESS", "support@trustedpartnerhub.com")
FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Lead Agents Studio")

# Storage
SENT_FILE = "/tmp/sent_las.json"
FOLLOWUP_FILE = "/tmp/followup_tracking.json"

# ============== FOLLOW-UP TEMPLATES (OGILVY) ==============

FOLLOWUP_1 = {
    "subject": "following up - {company_name}",
    "body": """Hi {first_name},

Following up with one simple idea:

Clinics don't lose money because ads "don't work."
They lose money because:
(1) creative gets stale, and
(2) the first reply is slow.

Lead Agents Studio solves both:
fresh AI video creatives on demand + instant follow‑up/booking on WhatsApp/SMS/phone.

If you're curious, the live demo takes about a minute:
https://leadagentsstudio.com

Want the WhatsApp demo or the quick call demo?

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%""",
    "days_after": 3,
}

FOLLOWUP_2 = {
    "subject": "last note - {company_name}",
    "body": """Hi {first_name},

Last note from me.

If "fresh creatives + instant follow‑up that books" is relevant for {company_name},
here's the demo link:
https://leadagentsstudio.com

If it's not a priority right now, no worries — I'll close the loop.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%""",
    "days_after": 7,
}

# ============== STORAGE ==============

def load_followup_tracking() -> dict:
    """Load follow-up tracking data"""
    try:
        if Path(FOLLOWUP_FILE).exists():
            with open(FOLLOWUP_FILE) as f:
                return json.load(f)
    except:
        pass
    return {}

def save_followup_tracking(data: dict):
    """Save follow-up tracking"""
    with open(FOLLOWUP_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def track_initial_send(email: str, company: str):
    """Track when initial email was sent"""
    tracking = load_followup_tracking()
    
    tracking[email.lower()] = {
        "company_name": company,
        "first_name": "there",
        "initial_sent": datetime.utcnow().isoformat(),
        "followup_1_sent": None,
        "followup_2_sent": None,
        "replied": False,
        "opened": False,
        "clicked": False,
    }
    
    save_followup_tracking(tracking)

# ============== SENDING ==============

def send_email(email: str, subject: str, body: str, tag: str) -> bool:
    """Send via Mailgun"""
    
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
                "o:tag": ["lead-agents-studio", "medspa", tag],
            },
            timeout=30,
        )
        
        return response.status_code == 200
    
    except:
        return False

# ============== FOLLOW-UP LOGIC ==============

def send_followups():
    """Check and send follow-ups"""
    
    print(f"\n{'='*60}")
    print(f"FOLLOW-UP SYSTEM")
    print(f"Time: {datetime.utcnow().isoformat()}")
    print(f"{'='*60}\n")
    
    tracking = load_followup_tracking()
    now = datetime.utcnow()
    
    sent_followup_1 = 0
    sent_followup_2 = 0
    
    for email, data in tracking.items():
        # Skip if replied/clicked
        if data.get("replied") or data.get("clicked"):
            continue
        
        initial_sent = datetime.fromisoformat(data["initial_sent"])
        days_since = (now - initial_sent).days
        
        company = data.get("company_name", "your clinic")
        first_name = data.get("first_name", "there")
        
        # Follow-up 1 (Day 3)
        if days_since >= 3 and not data.get("followup_1_sent"):
            print(f"📧 Follow-up 1: {email} ({company}) - Day {days_since}")
            
            subject = FOLLOWUP_1["subject"].format(company_name=company)
            body = FOLLOWUP_1["body"].format(first_name=first_name, company_name=company)
            
            if send_email(email, subject, body, "followup-1"):
                data["followup_1_sent"] = now.isoformat()
                sent_followup_1 += 1
                print(f"   ✅ Sent")
            else:
                print(f"   ❌ Failed")
        
        # Follow-up 2 (Day 7)
        elif days_since >= 7 and not data.get("followup_2_sent"):
            print(f"📧 Follow-up 2: {email} ({company}) - Day {days_since}")
            
            subject = FOLLOWUP_2["subject"].format(company_name=company)
            body = FOLLOWUP_2["body"].format(first_name=first_name, company_name=company)
            
            if send_email(email, subject, body, "followup-2"):
                data["followup_2_sent"] = now.isoformat()
                sent_followup_2 += 1
                print(f"   ✅ Sent")
            else:
                print(f"   ❌ Failed")
        
        time.sleep(5)  # Rate limiting
    
    # Save updated tracking
    save_followup_tracking(tracking)
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Follow-up 1 sent: {sent_followup_1}")
    print(f"Follow-up 2 sent: {sent_followup_2}")
    print(f"{'='*60}\n")

# ============== MAIN ==============

if __name__ == "__main__":
    send_followups()

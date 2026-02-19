#!/usr/bin/env python3
"""
Lead Agents Studio - Scheduled Pipeline
Runs via Render Cron Jobs (or locally)

Scrapes leads → Enriches → Sends emails
"""
import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# ============== CONFIG ==============

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "leadagentsstudio.com")
EMAIL_FROM = os.getenv("EMAIL_FROM_ADDRESS", "support@leadagentsstudio.com")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Lead Agents Studio")

BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY", "")
SERP_API_KEY = os.getenv("SERP_API_KEY", "")

# Limits
MAX_EMAILS_PER_RUN = 20
DELAY_BETWEEN_EMAILS = 60  # seconds

# Search queries for Google Maps scraping
SEARCH_QUERIES = [
    "medspa Los Angeles",
    "medspa Miami",
    "medical spa Beverly Hills",
    "botox clinic Scottsdale",
    "aesthetic clinic New York",
    "medspa Houston",
    "cosmetic clinic Dallas",
    "medical spa Boca Raton",
    "medspa San Diego",
    "aesthetic clinic Atlanta",
    "medspa Chicago",
    "medical spa Denver",
    "botox clinic Phoenix",
    "medspa Las Vegas",
]

# Storage (use Redis/DB in production)
SENT_FILE = "/tmp/sent_emails.json"


# ============== STORAGE ==============

def load_sent_emails() -> set:
    """Load previously sent emails"""
    try:
        if os.path.exists(SENT_FILE):
            with open(SENT_FILE, 'r') as f:
                return set(json.load(f))
    except:
        pass
    return set()


def save_sent_email(email: str):
    """Save sent email"""
    sent = load_sent_emails()
    sent.add(email.lower())
    with open(SENT_FILE, 'w') as f:
        json.dump(list(sent), f)


# ============== EMAIL TEMPLATE ==============

EMAIL_TEMPLATE = """Hi {first_name},

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


# ============== SCRAPING ==============

def scrape_google_maps_brightdata(query: str) -> list:
    """Scrape Google Maps using BrightData SERP API"""
    
    if not BRIGHTDATA_API_KEY:
        print("   ⚠️ No BrightData API key configured")
        return []
    
    # BrightData SERP API for Google Maps
    url = "https://api.brightdata.com/serp/google/maps"
    
    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "query": query,
        "country": "us",
        "language": "en",
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("organic", [])
            
            leads = []
            for r in results:
                if r.get("email"):
                    leads.append({
                        "email": r["email"],
                        "company_name": r.get("title", ""),
                        "first_name": "there",  # Need enrichment for actual name
                        "city": r.get("city", ""),
                        "phone": r.get("phone", ""),
                        "website": r.get("website", ""),
                        "rating": r.get("rating"),
                        "reviews": r.get("reviews_count"),
                    })
            
            return leads
        else:
            print(f"   API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   Exception: {e}")
        return []


def get_sample_leads() -> list:
    """Fallback: Return sample leads for testing"""
    return [
        # Add your test leads here
        # {"email": "test@example.com", "first_name": "Test", "company_name": "Test Medspa"}
    ]


# ============== SENDING ==============

def send_email(to_email: str, subject: str, body: str) -> dict:
    """Send email via Mailgun"""
    
    if not MAILGUN_API_KEY:
        print("   ⚠️ No Mailgun API key configured")
        return {"success": False, "error": "No API key"}
    
    data = {
        "from": f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>",
        "to": to_email,
        "subject": subject,
        "text": body,
        "o:tracking": "yes",
        "o:tracking-clicks": "yes",
        "o:tracking-opens": "yes",
        "o:tag": ["lead-agents-studio", "medspa", "pipeline"],
    }
    
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data=data,
    )
    
    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "message_id": response.json().get("id") if response.status_code == 200 else None,
        "error": response.text if response.status_code != 200 else None,
    }


# ============== MAIN ==============

def run_pipeline():
    """Main pipeline execution"""
    
    print(f"\n{'='*60}")
    print(f"LEAD AGENTS STUDIO - PIPELINE")
    print(f"Time: {datetime.utcnow().isoformat()}")
    print(f"{'='*60}\n")
    
    # Load sent emails
    sent_emails = load_sent_emails()
    print(f"📧 Previously sent: {len(sent_emails)} emails")
    
    # Select query based on time
    query_idx = datetime.utcnow().hour % len(SEARCH_QUERIES)
    query = SEARCH_QUERIES[query_idx]
    
    print(f"\n🔍 Scraping: {query}")
    
    # Scrape leads
    leads = scrape_google_maps_brightdata(query)
    
    if not leads:
        print("   No leads found from scraping, using samples...")
        leads = get_sample_leads()
    
    print(f"   Found: {len(leads)} leads")
    
    # Filter already sent
    new_leads = [l for l in leads if l.get("email", "").lower() not in sent_emails]
    print(f"   New leads: {len(new_leads)}")
    
    # Limit per run
    to_send = new_leads[:MAX_EMAILS_PER_RUN]
    print(f"   Will send: {len(to_send)}")
    
    # Send emails
    sent = 0
    failed = 0
    
    for i, lead in enumerate(to_send):
        email = lead.get("email", "")
        company = lead.get("company_name", "your clinic")
        first_name = lead.get("first_name", "there")
        
        print(f"\n[{i+1}/{len(to_send)}] {email}")
        print(f"    Company: {company}")
        
        subject = f"quick question for {company}"
        body = EMAIL_TEMPLATE.format(
            first_name=first_name,
            company_name=company,
        )
        
        result = send_email(email, subject, body)
        
        if result["success"]:
            print(f"    ✅ Sent!")
            save_sent_email(email)
            sent += 1
        else:
            print(f"    ❌ Failed: {result.get('error', 'Unknown error')}")
            failed += 1
        
        # Rate limiting
        if i < len(to_send) - 1:
            print(f"    ⏳ Waiting {DELAY_BETWEEN_EMAILS}s...")
            time.sleep(DELAY_BETWEEN_EMAILS)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Query: {query}")
    print(f"Leads found: {len(leads)}")
    print(f"New leads: {len(new_leads)}")
    print(f"Sent: {sent}")
    print(f"Failed: {failed}")
    print(f"Total sent (all time): {len(sent_emails) + sent}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    run_pipeline()

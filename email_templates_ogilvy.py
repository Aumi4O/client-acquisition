"""
Lead Agents Studio - Email Templates (Ogilvy Copy)
All sequences with improved messaging
"""

# ============== SEQUENCE 1: CORE (DEFAULT) ==============

CORE_SEQUENCE = {
    "initial": {
        "subject": "quick question for {company_name}",
        "body": """Hi {first_name},

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
    },
    
    "followup_1": {
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

Unsubscribe: %unsubscribe_url%"""
    },
    
    "followup_2": {
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

Unsubscribe: %unsubscribe_url%"""
    }
}

# ============== SEQUENCE 2: RUNNING ADS ==============

RUNNING_ADS_SEQUENCE = {
    "initial": {
        "subject": "{company_name} ads + a quick question",
        "body": """Hi {first_name},

Saw {company_name} is running video ads — quick question:

What happens in the first 15 minutes after a lead comes in?

That's where most clinics leak revenue:
late reply → lead messages the next clinic → booking goes to whoever answers first.

Lead Agents Studio installs the full pipeline:
• AI video creatives on demand (owner-avatar + UGC-style + custom b-roll)
• WhatsApp/SMS + calling to qualify and book
• reminders + quiet-lead recovery (polite, then stop)

You can test the live flow on your own phone:
https://leadagentsstudio.com

Want the WhatsApp version or the 60‑second call version?

P.S. The demo uses a $5 credit (real messages/calls). Setup is $5,000 one time.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    },
    
    "followup_1": {
        "subject": "re: your lead follow-up",
        "body": """Hi {first_name},

If you're paying for ads, you're paying for speed.

Even a great campaign bleeds money if:
• replies happen late, or
• nobody follows up when the lead goes quiet.

That's exactly what we automate — plus we generate fresh ad creatives on demand so you don't have to keep filming.

Demo link:
https://leadagentsstudio.com

Should I point you to WhatsApp demo or the call demo?

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    },
    
    "followup_2": {
        "subject": "closing this out",
        "body": """Hi {first_name},

I'll close this out after today.

If you ever want to see the "ads → follow-up → booking" pipeline live:
https://leadagentsstudio.com

All good if now's not the time.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    }
}

# ============== SEQUENCE 3: HIRING ==============

HIRING_SEQUENCE = {
    "initial": {
        "subject": "saw you're hiring at {company_name}",
        "body": """Hi {first_name},

Noticed {company_name} is hiring — congrats.

When clinics scale, one thing breaks first:
response time.

More inquiries + the same front desk =
missed calls, late replies, and leads that quietly book elsewhere.

Lead Agents Studio handles the first contact automatically:
• fresh AI video creatives on demand (owner-avatar + UGC-style + b-roll)
• instant WhatsApp/SMS + calling
• qualification + booked consults + reminders

You can test it in about a minute:
https://leadagentsstudio.com

Worth sending you the WhatsApp demo path?

P.S. Demo is a $5 credit (real messages/calls). Setup is $5,000 one time.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    },
    
    "followup_1": {
        "subject": "quick follow-up",
        "body": """Hi {first_name},

Small follow-up.

Hiring helps — but it doesn't fix nights/weekends or "we'll reply later."
That's where leads disappear.

We install a system that replies instantly, qualifies, and books — and keeps your ads fresh without constant filming.

Demo:
https://leadagentsstudio.com

Want WhatsApp or a 60‑second call demo?

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    },
    
    "followup_2": {
        "subject": "last message from me",
        "body": """Hi {first_name},

Last message.

If you want to see how the system feels from a lead's perspective:
https://leadagentsstudio.com

If not, all good — I'll leave you be.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    }
}

# ============== SEQUENCE 4: HIGH REVIEWS ==============

HIGH_REVIEWS_SEQUENCE = {
    "initial": {
        "subject": "{company_name} reviews + a quick question",
        "body": """Hi {first_name},

Saw {company_name} has {google_review_count} Google reviews — clearly you're doing a lot right.

Quick question:
how do you handle inquiries that come in after hours or while the team is with clients?

That's the window where even great clinics leak bookings:
slow reply → lead messages another clinic → first responder wins.

Lead Agents Studio installs:
• AI video ads on demand (owner-avatar + UGC-style + custom b-roll)
• WhatsApp/SMS + calling to qualify and book
• reminders + quiet-lead recovery (polite, then stop)

Live demo:
https://leadagentsstudio.com

Should I point you to the WhatsApp demo path?

P.S. Demo uses a $5 credit (real messages/calls). Setup is $5,000 one time.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    },
    
    "followup_1": {
        "subject": "after-hours inquiries at {company_name}",
        "body": """Hi {first_name},

Following up on one specific point:

High‑review clinics lose money the same way everyone does:
the lead comes in when nobody can reply fast.

We fix it with instant follow‑up + booking — and keep your creative fresh without filming.

Demo:
https://leadagentsstudio.com

Want WhatsApp demo or a quick call demo?

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    },
    
    "followup_2": {
        "subject": "should I stop reaching out?",
        "body": """Hi {first_name},

Should I stop reaching out?

If "fresh creatives + instant booking follow‑up" is worth seeing, here's the demo:
https://leadagentsstudio.com

If not, just ignore this and I'll close the loop.

—
Lead Agents Studio
support@leadagentsstudio.com

Unsubscribe: %unsubscribe_url%"""
    }
}

# ============== SEQUENCE SELECTOR ==============

def get_sequence(signal: str = "core") -> dict:
    """Get email sequence based on signal"""
    
    sequences = {
        "core": CORE_SEQUENCE,
        "running_ads": RUNNING_ADS_SEQUENCE,
        "hiring": HIRING_SEQUENCE,
        "high_reviews": HIGH_REVIEWS_SEQUENCE,
    }
    
    return sequences.get(signal, CORE_SEQUENCE)

def get_email(sequence: str, stage: str) -> dict:
    """Get specific email from sequence"""
    
    seq = get_sequence(sequence)
    return seq.get(stage, seq["initial"])

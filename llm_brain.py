#!/usr/bin/env python3
"""
Lead Agents Studio - LLM Brain
Analyzes campaign performance and adapts strategy for better conversions

Runs daily to:
1. Analyze open/click/reply rates
2. Identify winning patterns
3. Adjust copy, timing, and targeting
4. Generate A/B test variants
"""
import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# ============== CONFIG ==============

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

# Storage
TRACKING_FILE = "/tmp/followup_tracking.json"
EVENTS_FILE = "/tmp/events_las.json"
INSIGHTS_FILE = "/tmp/llm_insights.json"
VARIANTS_FILE = "/tmp/email_variants.json"

# ============== DATA LOADING ==============

def load_tracking() -> dict:
    """Load follow-up tracking data"""
    try:
        if Path(TRACKING_FILE).exists():
            with open(TRACKING_FILE) as f:
                return json.load(f)
    except:
        pass
    return {}

def load_events() -> list:
    """Load email events"""
    try:
        if Path(EVENTS_FILE).exists():
            with open(EVENTS_FILE) as f:
                return json.load(f)
    except:
        pass
    return []

def load_insights() -> dict:
    """Load previous insights"""
    try:
        if Path(INSIGHTS_FILE).exists():
            with open(INSIGHTS_FILE) as f:
                return json.load(f)
    except:
        pass
    return {"history": []}

def save_insights(insights: dict):
    """Save insights"""
    with open(INSIGHTS_FILE, 'w') as f:
        json.dump(insights, f, indent=2)

def save_variants(variants: list):
    """Save email variants for A/B testing"""
    with open(VARIANTS_FILE, 'w') as f:
        json.dump(variants, f, indent=2)

# ============== ANALYSIS ==============

def calculate_metrics(tracking: dict, events: list) -> dict:
    """Calculate campaign metrics"""
    
    total_sent = len(tracking)
    
    # Count events
    opens = len([e for e in events if e.get("type") == "opened"])
    clicks = len([e for e in events if e.get("type") == "clicked"])
    bounces = len([e for e in events if e.get("type") == "bounced"])
    complaints = len([e for e in events if e.get("type") == "complained"])
    unsubscribes = len([e for e in events if e.get("type") == "unsubscribed"])
    
    # Count follow-up performance
    followup_1_sent = len([d for d in tracking.values() if d.get("followup_1_sent")])
    followup_2_sent = len([d for d in tracking.values() if d.get("followup_2_sent")])
    
    # Engagement by stage
    initial_opens = 0
    followup_1_opens = 0
    followup_2_opens = 0
    
    for email, data in tracking.items():
        if data.get("opened"):
            if not data.get("followup_1_sent"):
                initial_opens += 1
            elif not data.get("followup_2_sent"):
                followup_1_opens += 1
            else:
                followup_2_opens += 1
    
    return {
        "total_sent": total_sent,
        "opens": opens,
        "clicks": clicks,
        "bounces": bounces,
        "complaints": complaints,
        "unsubscribes": unsubscribes,
        "open_rate": round(opens / total_sent * 100, 1) if total_sent > 0 else 0,
        "click_rate": round(clicks / total_sent * 100, 1) if total_sent > 0 else 0,
        "bounce_rate": round(bounces / total_sent * 100, 1) if total_sent > 0 else 0,
        "followup_1_sent": followup_1_sent,
        "followup_2_sent": followup_2_sent,
        "initial_open_rate": round(initial_opens / total_sent * 100, 1) if total_sent > 0 else 0,
        "followup_1_open_rate": round(followup_1_opens / followup_1_sent * 100, 1) if followup_1_sent > 0 else 0,
        "followup_2_open_rate": round(followup_2_opens / followup_2_sent * 100, 1) if followup_2_sent > 0 else 0,
    }

# ============== LLM ANALYSIS ==============

def analyze_with_llm(metrics: dict, previous_insights: dict) -> dict:
    """Use LLM to analyze performance and suggest improvements"""
    
    prompt = f"""You are an expert cold email strategist analyzing a B2B outreach campaign for Lead Agents Studio (AI agent for medspas).

CURRENT PERFORMANCE:
- Total sent: {metrics['total_sent']} emails
- Open rate: {metrics['open_rate']}%
- Click rate: {metrics['click_rate']}%
- Bounce rate: {metrics['bounce_rate']}%
- Initial email open rate: {metrics['initial_open_rate']}%
- Follow-up 1 open rate: {metrics['followup_1_open_rate']}%
- Follow-up 2 open rate: {metrics['followup_2_open_rate']}%

PREVIOUS INSIGHTS:
{json.dumps(previous_insights.get('history', [])[-3:], indent=2)}

CURRENT COPY APPROACH:
- Ogilvy-style: problem-first, specific, conversational
- 3-email sequence: Day 0, Day 3, Day 7
- Target: Medspa/aesthetic clinic owners
- Offer: AI agent for instant patient follow-up + video ad generation

ANALYZE:
1. What's working? What's not?
2. Are open rates declining across follow-ups? Why?
3. Should we adjust timing (Day 3/7 vs Day 2/5)?
4. Should we test different subject lines?
5. Should we change the CTA or offer positioning?
6. What A/B test should we run next?

Provide:
1. Key insights (3-5 bullet points)
2. Recommended changes (specific, actionable)
3. A/B test hypothesis (1-2 variants to test)

Be specific and data-driven. Format as JSON."""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an expert cold email strategist focused on B2B SaaS conversions."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
            },
            timeout=60,
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = json.loads(result["choices"][0]["message"]["content"])
            return analysis
        else:
            print(f"OpenAI API Error: {response.status_code}")
            return {}
    
    except Exception as e:
        print(f"LLM Analysis Error: {e}")
        return {}

# ============== VARIANT GENERATION ==============

def generate_variants(insights: dict) -> list:
    """Generate A/B test email variants based on insights"""
    
    if not insights:
        return []
    
    prompt = f"""Based on these campaign insights, generate 2 A/B test email variants for the INITIAL email (Day 0).

INSIGHTS:
{json.dumps(insights, indent=2)}

CURRENT SUBJECT: "quick question for {{company_name}}"

Generate 2 new subject line + body variants that test the hypothesis from insights.
Keep the same structure (problem → solution → CTA) but test different angles.

Return as JSON array:
[
  {{
    "variant_id": "test_a",
    "hypothesis": "what we're testing",
    "subject": "new subject line",
    "body": "full email body with placeholders"
  }},
  ...
]

Keep {{company_name}}, {{first_name}}, %unsubscribe_url% placeholders."""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an expert copywriter specializing in cold email A/B testing."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "response_format": {"type": "json_object"},
            },
            timeout=60,
        )
        
        if response.status_code == 200:
            result = response.json()
            variants_data = json.loads(result["choices"][0]["message"]["content"])
            return variants_data.get("variants", [])
        else:
            return []
    
    except Exception as e:
        print(f"Variant Generation Error: {e}")
        return []

# ============== MAIN ==============

def run_analysis():
    """Run daily LLM analysis"""
    
    print(f"\n{'='*60}")
    print(f"LLM BRAIN - CAMPAIGN ANALYSIS")
    print(f"Time: {datetime.utcnow().isoformat()}")
    print(f"{'='*60}\n")
    
    # Load data
    tracking = load_tracking()
    events = load_events()
    previous_insights = load_insights()
    
    if not tracking:
        print("⚠️  No data yet. Run pipeline first.")
        return
    
    print(f"📊 Analyzing {len(tracking)} sent emails...")
    
    # Calculate metrics
    metrics = calculate_metrics(tracking, events)
    
    print(f"\nCurrent Metrics:")
    print(f"  Open rate: {metrics['open_rate']}%")
    print(f"  Click rate: {metrics['click_rate']}%")
    print(f"  Bounce rate: {metrics['bounce_rate']}%")
    
    # LLM Analysis
    print(f"\n🧠 Running LLM analysis...")
    insights = analyze_with_llm(metrics, previous_insights)
    
    if insights:
        print(f"\n✅ Insights generated:")
        print(json.dumps(insights, indent=2))
        
        # Save insights
        previous_insights["history"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics,
            "insights": insights,
        })
        save_insights(previous_insights)
        
        # Generate A/B test variants
        print(f"\n🧪 Generating A/B test variants...")
        variants = generate_variants(insights)
        
        if variants:
            print(f"✅ Generated {len(variants)} variants")
            save_variants(variants)
            
            for v in variants:
                print(f"\n  Variant: {v.get('variant_id')}")
                print(f"  Hypothesis: {v.get('hypothesis')}")
                print(f"  Subject: {v.get('subject')}")
        else:
            print("⚠️  No variants generated")
    else:
        print("⚠️  LLM analysis failed")
    
    print(f"\n{'='*60}")
    print(f"Analysis complete")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_analysis()

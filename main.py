#!/usr/bin/env python3
"""
AI Content Moderator - Core Script
Classifies user-generated content for Trust & Safety violations
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def moderate_content(text):
    """
    Moderate content using OpenAI's GPT model with Chain of Thought prompting

    Args:
        text (str): The content to moderate

    Returns:
        dict: Classification results with reasoning
    """

    prompt = f"""
You are an expert Trust & Safety moderator for a dating app. Use Chain of Thought reasoning to analyze this content through the lens of dating app safety.

Content to analyze: "{text}"

Follow this exact Chain of Thought process:

STEP 1 - CONTEXT CLASSIFICATION:
- Is this profile content (public) or message content (private 1v1)?
- What type of dating interaction is this? (initial match, ongoing conversation, profile description, etc.)

STEP 2 - DATING-SPECIFIC INTENT ANALYSIS:
- What is the user trying to accomplish? (genuine connection, hookup, scam, harassment)
- Are there romance scam indicators? (quick emotional attachment, financial requests, avoids meeting)
- Is this consensual adult interaction between matches?

STEP 3 - CONSENT & ENGAGEMENT ASSESSMENT:
- If intimate/sexual: Are there mutual engagement signals?
- Is this unwanted first contact vs. established conversation?
- Any signs of coercion or pressure?

STEP 4 - HARM RISK EVALUATION:
- Could this cause real-world harm? (financial scam, stalking, violence threats)
- Does this exploit dating app trust dynamics?
- Is this targeting vulnerable users? (emotional manipulation, catfishing)

STEP 5 - EDGE CASE RECOGNITION:
- Is this a gray area where context determines appropriateness?
- Does this need human reviewer escalation?
- Are there cultural/generational factors to consider?

Dating App Policy Categories:
- Romance/Financial Scams: Fake emotional connection for money
- Non-Consensual Intimate Content: Sexual content without mutual engagement
- Harassment: Persistent unwanted contact, threats, stalking behaviors
- Identity Fraud: Catfishing, fake photos, impersonation
- Commercial Solicitation: Escort services, OnlyFans promotion
- Harmful Contact Requests: Immediate meetup pressure, location sharing demands

Respond in this exact JSON format:
{{
    "violation_detected": true/false,
    "primary_category": "category name or null",
    "severity": "low/medium/high or null",
    "confidence": 0.0-1.0,
    "context_type": "profile/message/report",
    "consent_indicators": "mutual/non_consensual/unclear",
    "chain_of_thought": "your complete step-by-step analysis following the 5 steps above",
    "edge_case_flag": true/false,
    "recommended_action": "allow/human_review/remove/account_action"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise content moderation AI. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Demo the content moderator"""

    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return

    print("🔍 AI Content Moderator - Demo")
    print("=" * 40)

    # Test cases
    test_content = [
        "Hey there! Looking forward to meeting someone special 😊",
        "I hate all people from that country, they're all the same",
        "Send me $500 and I'll meet you tonight",
        "You're so ugly, nobody will ever love you"
    ]

    for i, content in enumerate(test_content, 1):
        print(f"\n📝 Test Case {i}: '{content}'")
        result = moderate_content(content)
        print(f"🤖 AI Response: {result}")
        print("-" * 40)

if __name__ == "__main__":
    main()
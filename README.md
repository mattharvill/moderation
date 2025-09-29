# Dating App Moderation That Actually Works

## What I Built
AI moderation system for dating apps that doesn't flag "Want to grab coffee?" as harassment.

Most moderation tools treat dating apps like Twitter - zero tolerance, immediate bans. I built something that understands dating conversations are different.

**Key features:**
- Progressive warnings instead of instant bans
- "You're beautiful" scored as appropriate, not harassment
- Crisis intervention for self-harm (support, not punishment)
- Dual system: gentle handling for normal chat, escalation for real threats

## Why It Matters
Dating apps lose users when moderation is too aggressive. Over-moderation kills engagement.

**The business problem:**
- False positives frustrate users into leaving
- Support tickets flood in from wrongly banned users
- Appeal processes waste time and money

**Dating app context matters:**
- "You're hot" between matched users isn't harassment
- Phone number requests are normal after conversation builds
- Hook-up language should score 2-3, not 8-9

## How It Works
Built two different prompts that route automatically:

**Normal conversations** → Gentle scoring with progressive enforcement
**Serious issues** → Immediate escalation (hate speech, self-harm, fraud)

**Evaluation process:**
- Tested on 45+ real dating app messages
- Manual scoring to find false positive patterns
- Langfuse tracking for every decision
- Systematic prompt improvements based on failures

**Crisis handling:**
Self-harm detection doesn't remove content - it provides mental health resources and notifies appropriate support teams.

## Demo/Results
[Live demo](http://172.20.152.153:8502) - test it yourself

**Try these:**
- "Hey! Want to grab coffee?" → Score 1 (appropriate)
- "What's your phone number?" → Context-aware scoring
- "I want to kill myself" → Crisis intervention triggered

**Results from testing:**
- Reduced false positives in severity scoring (cases identified and fixed)
- Cases of appropriate content correctly identified
- Progressive enforcement maintains safety while improving user experience

---
Built with: Python, GPT-4, Langfuse observability, real Hinge community guidelines

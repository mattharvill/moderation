# AI Content Moderator - Hinge PM Interview Project

## Project Overview
Building a hands-on AI content moderation system to demonstrate technical skills for the **AI Product Manager, Trust & Safety** role at Hinge.

**Current Learning Mode:** Deep understanding approach - explaining technical choices and reasoning for interview preparation.

## Learning Objectives
Develop interview-ready expertise in key job requirements:

### Core Technical Skills
- [x] **Chain of Thought prompting** - 5-step dating app specific reasoning process
- [x] **Problem Analysis** - Identified dating app specific moderation challenges
- [ ] **Langfuse integration** - LLM tracing and performance analysis
- [ ] **False positive/negative analysis** - T&S metrics and error detection
- [ ] **Python prototyping** - Comfortable modifying AI workflows
- [ ] **A/B testing framework** - Comparing prompt strategies with measurable outcomes

### Interview Story Arc
*"Leadership asked me to prototype AI moderation for the queue. I analyzed our pain points - volume, speed, and context complexity - then built Chain of Thought prompts that handle dating app consent and context nuances..."*

## Project Structure
```
/moderation/
├── main.py              # Core AI moderation script with sophisticated CoT prompting
├── .env                 # API keys (secure, not committed)
├── requirements.txt     # Dependencies
├── .gitignore          # Protects API keys
└── README.md           # This file
```

## Cross-Platform Setup

### PC (WSL2) Setup
```bash
cd /home/matt/projects/moderation
source .venv/bin/activate
pip install openai python-dotenv
python main.py
```

### MacBook Setup
```bash
cd ~/Documents/Github/moderation-sep-25/moderation
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv
echo "OPENAI_API_KEY=your_key_here" > .env
python3 main.py
```

## Current Status
✅ **Environment Setup** - Cross-platform Python venv, OpenAI API integration
✅ **Sophisticated Chain of Thought** - 5-step dating app specific prompting
✅ **Problem Analysis Complete** - Identified volume, speed, context challenges
✅ **GitHub Sync** - Project accessible on both machines
🔄 **In Progress** - Testing reasoning on consent implications and social media complexity
⏳ **Next** - Langfuse integration for LLM tracing

## Current Context - Deep Learning Approach
**Where we are:** Testing understanding of dating app moderation complexity

**Pending Challenges:**
1. **Consent Logic:** How to handle "consent implied by being on dating app" vs. first message dick pics
2. **Social Media Complexity:** Clarify why dating apps don't need the "depth" of social media moderation

## Key Job Requirements Mapping

| Hinge JD Requirement | Our Implementation | Interview Story |
|---------------------|-------------------|----------------|
| "Chain of Thought reasoning" | Step-by-step moderation prompts | "I engineered prompts that break down decisions..." |
| "LLM tracing platforms (Langfuse)" | Integrated tracing & analysis | "I used Langfuse to debug false positives..." |
| "False-positive/negative rates" | Error analysis framework | "I built metrics to track moderation accuracy..." |
| "Python for prototyping" | Hands-on script development | "I prototyped and iterated on AI workflows..." |
| "A/B tests" | Prompt comparison framework | "I tested different prompt strategies..." |

## Interview Questions to Practice
*Will be added after each major section completion*

## Notes for Future Sessions
- Focus on **understanding** over building - need to explain technical choices
- Each section ends with 3 interview questions to test comprehension
- Goal: Speak confidently about every bullet point in the job description

---
*Last updated: [Date] - Ready to continue with advanced Chain of Thought techniques*
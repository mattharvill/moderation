# AI Content Moderator - Hinge PM Interview Project

## Project Overview
Building a hands-on AI content moderation system to demonstrate technical skills for the **AI Product Manager, Trust & Safety** role at Hinge.

## Learning Objectives
Develop interview-ready expertise in key job requirements:

### Core Technical Skills
- [x] **Chain of Thought prompting** - Step-by-step AI reasoning for complex moderation decisions
- [ ] **Langfuse integration** - LLM tracing and performance analysis
- [ ] **False positive/negative analysis** - T&S metrics and error detection
- [ ] **Python prototyping** - Comfortable modifying AI workflows
- [ ] **A/B testing framework** - Comparing prompt strategies with measurable outcomes

### Interview Story Arc
*"I built an AI content moderator using Chain of Thought prompting to reduce false positives in dating app content. Here's how I engineered prompts that break down moderation decisions into auditable steps..."*

## Project Structure
```
/moderation/
├── main.py              # Core AI moderation script
├── .env                 # API keys (secure)
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Setup Instructions
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install openai python-dotenv

# Set API key in .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Run the moderator
python main.py
```

## Current Status
✅ **Environment Setup** - Python venv, OpenAI API integration
✅ **Basic Chain of Thought** - Structured prompting foundation
🔄 **In Progress** - Advanced Chain of Thought techniques
⏳ **Next** - Langfuse integration for LLM tracing

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
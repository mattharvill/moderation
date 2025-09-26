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
✅ **Consent Logic Understanding** - Respect-based framework established
✅ **GitHub Sync** - Project accessible on both machines
🔄 **In Progress** - Full PM strategy development (PRD + Technical Deep-Dive)
⏳ **Next** - Complete mock PRD analysis and Langfuse integration

## Current Context - Strategic PM Learning Phase
**Where we are:** Building complete PM workflow from business problem to technical solution

**Role-Play Scenario:**
- **Role:** Trust & Safety PM at Hinge (AI background from Maven courses)
- **Challenge:** Leadership wants path to 100% AI moderation + agent efficiency
- **Timeline:** Thursday evening → Monday morning presentation
- **Constraints:** Focus on text/images first, video later
- **🚨 CRITICAL:** Must have working prototype ready for live demo Monday

**Mock Data Analysis in Progress:**
- Text messages: 45K daily reports (78% volume), 12% appeal rate
- Photos: 12.5K daily reports (22% volume), 23% appeal rate
- Geographic: English 60% (11% appeals), Spanish 25% (19% appeals)
- Harm priorities: Financial scams (high harm), NCII (highest harm), harassment (medium harm)

**Learning Goals Achieved:**
1. ✅ Strategic thinking - Data-driven prioritization approach
2. 🔄 Technical evaluation - Why Chain of Thought, why Langfuse
3. ⏳ Execution planning - Phases, metrics, risks

## Tomorrow's Critical Path (Friday, Sep 26)

### Morning Session: Strategic Analysis
- [ ] **Data Analysis:** Review mock metrics and develop prioritization strategy
- [ ] **Business Case:** Articulate why AI moderation is the right solution
- [ ] **Success Metrics:** Define what good looks like for leadership

### Afternoon Session: Prototype Enhancement
- [ ] **Demo Readiness:** Enhance existing main.py for live presentation
- [ ] **Langfuse Integration:** Add tracing for AI decision transparency
- [ ] **Test Scenarios:** Prepare demo cases based on data priorities

### Evening Session: Presentation Prep
- [ ] **Demo Run-Through:** Test prototype with realistic scenarios
- [ ] **Edge Cases:** Show AI reasoning and human escalation triggers
- [ ] **Failure Scenarios:** Demonstrate when human review is needed

## Monday Presentation Structure
**Part 1:** Strategic Recommendation (Data → Problem → Solution)
**Part 2:** Live Prototype Demo (Proof of concept validation)
**Part 3:** Implementation Roadmap (Timeline, resources, risks)

## Interview Story Arc Complete
*"Leadership challenged me to solve our moderation bottleneck. I analyzed our data, identified the highest-impact opportunities, built a Chain of Thought prototype with Langfuse observability, and demonstrated measurable improvements in decision accuracy and speed."*

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

## Key Files for Tomorrow
- `main.py` - Current Chain of Thought prototype (needs demo enhancement)
- `README.md` - Project documentation and progress tracking
- Mock data metrics from today's session (in README)

## Tomorrow's Success Criteria
✅ **Strategic clarity:** Can articulate data-driven prioritization
✅ **Technical demonstration:** Working prototype with Langfuse tracing
✅ **Business presentation:** Ready for Monday leadership demo

---
*Last updated: Sep 25, 2025 - Ready for Friday sprint to Monday demo*
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
├── main.py                   # Original prototype (reference only)
├── hinge_moderation_v2.py    # New prototype built from scratch with full understanding
├── .env                      # API keys (secure, not committed)
├── requirements.txt          # Dependencies
├── .gitignore               # Protects API keys
└── README.md                # This file
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
✅ **PRD Development** - Business problem, success metrics, technical strategy defined
✅ **5-Step Chain of Thought Design** - Complete AI reasoning framework designed
✅ **Prototype Foundation** - Basic Python structure built and tested (`hinge_moderation_v2.py`)
✅ **Interview-Ready Logic** - Can defend technical choices and business outcomes
✅ **Complete Text Moderation** - GPT-4 integration with Chain of Thought reasoning
✅ **Real Policy Integration** - Actual Hinge community guidelines loaded and applied
✅ **Multi-Modal AI System** - GPT-4V image moderation with visual content analysis
✅ **Professional Web Interface** - Streamlit demo with dual-mode display
✅ **Production-Grade Error Handling** - AI safety system integration and graceful degradation
✅ **Live Demo Ready** - http://172.20.152.153:8502 for Monday presentation
🎯 **DEMO COMPLETE** - Full multi-modal AI moderation system ready for interview

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

### Morning Session: Strategic Analysis ✅ COMPLETED
- [x] **PRD Development:** Business problem, success metrics, technical strategy
- [x] **Chain of Thought Design:** Complete 5-step AI reasoning framework
- [x] **Prototype Foundation:** Built `hinge_moderation_v2.py` from scratch with full understanding

### Afternoon Session: Implementation
- [ ] **Code Chain of Thought:** Implement 5-step reasoning into prototype
- [ ] **OpenAI Integration:** Connect AI logic to GPT-4 API
- [ ] **Demo Scenarios:** Test with realistic dating app content

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
## Morning Session Accomplishments (Sep 26, 9:24am - 12pm)

### ✅ PRD & Business Strategy
- **Business Problem Defined:** 57.5K daily reports, 12-23% appeal rates, $5M annual cost
- **Success Metrics:** 10% appeal reduction, 95% AI confidence, 25-50% faster decisions
- **Technical Strategy:** Chain of Thought + Langfuse for transparency and continuous improvement

### ✅ 5-Step Chain of Thought Framework Designed
1. **Context Analysis:** Content type, engagement signals, conversation context
2. **Intent Assessment:** Harm scoring, account metadata, tiered response system
3. **Policy Application:** Severity-ordered violations, emergency escalation for CP/suicide
4. **Evidence Documentation:** NYT publishability standard, bias checking
5. **Action Recommendation:** Self-correction, user-centric outcomes, auto-ban triggers

### ✅ Prototype Built from Scratch
- **File:** `hinge_moderation_v2.py` - Complete understanding of every component
- **Structure:** Python classes, imports, Chain of Thought placeholder
- **Testing:** Basic structure runs successfully
- **Learning:** Syntax debugging, virtual environments, development workflow

### 🔄 Current Status: Ready for Implementation
- Chain of Thought logic designed and interview-ready
- Technical foundation built with full understanding
- Ready to code AI reasoning into working prototype

---

## Friday Afternoon Accomplishments (Sep 26, 2:00pm - 6:00pm)

### ✅ Complete Multi-Modal AI Moderation System
- **Text Moderation**: GPT-4 with 5-step Chain of Thought reasoning
- **Image Moderation**: GPT-4V visual content analysis with same framework
- **Policy Integration**: Real Hinge community guidelines (`hinge-principles.txt`)
- **Error Handling**: Production-grade safety system integration

### ✅ Professional Web Interface (`web_demo.py`)
- **Dual-Mode Display**: Demo mode (full AI reasoning) vs User mode (clean output)
- **Multi-Modal Support**: Single interface for text and image uploads
- **Live Demo URL**: http://172.20.152.153:8502
- **Interactive Testing**: Real-time content analysis for recruiters

### ✅ Advanced AI Product Insights Discovered
- **AI Safety Limitations**: GPT-4V refuses explicit content analysis
- **Non-Determinism**: Same content produces different scores (3 vs 5)
- **Production Challenges**: Need for human-in-the-loop systems
- **LangFuse Integration**: Clear value proposition for observability

### ✅ Interview-Ready Demo Assets
**Technical Demonstration**:
- Multi-modal AI system with consistent reasoning framework
- Real policy integration showing business application
- Error handling demonstrating production thinking
- Debug capabilities showing technical depth

**PM Story Arc**:
*"Built Chain of Thought moderation, extended to images, discovered AI safety limitations through testing, and created dual interfaces for different stakeholders. Ready to present scalable solution with clear next steps."*

### 🎯 Monday Presentation Strategy
1. **Live Demo**: Interactive web interface with multiple content types
2. **Technical Depth**: Show both user experience and AI reasoning
3. **Business Value**: Real Hinge policies with measurable outcomes
4. **Advanced Insights**: AI limitations and production considerations
5. **Scalability**: Clear path to 100% AI moderation with human oversight

---
*Last updated: Sep 26, 2025 - Complete multi-modal demo ready for Monday presentation*
#!/usr/bin/env python3 #This tells your computer "run this file using Python 3." It's called a "shebang" line.
""" #this starts a docstring, a multi-line comment
Hinge AI Content Moderator - AI-Moderator tool used to identify and mitigate harmful content. 
Business Problem: 57.5K daily reports, 12-23% appeal rates, $5M annual cost
Solution: Chain of Thought AI with human-in-the-loop for high-risk cases
"""
import os # for reading API keys from environment - reads API key from .env file
import json # for handling structured data - formats responses
import base64 # converts image to base64
import re # for parsing scores from AI responses
#from openai import OpenAI # for calling GPT
from langfuse.openai import openai
# from datetime import datetime # for timestamps - tracks when decisions are made (currently unused)
from dotenv import load_dotenv
class HingeAIModerator: # this is our main AI moderator. 
    # a class is like a blueprint. It contains all the functions and data our moderator needs

    """AI Content Moderator for Hinge Dating App""" # description of our class
    def __init__(self): # this runs when we create a new moderator
            print ("Starting Hinge AI Moderator...") # welcome message
            load_dotenv()
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            #load Hinge guidelines once when moderator starts
            with open("hinge-principles.txt","r") as file:
                self.principles = file.read()
            with open("hinge-terms-of-use.txt", "r") as file:
                self.terms = file.read()
    
    def create_chain_of_thought_prompt(self, content):
        """Create the general moderation prompt with streamlined policies"""
        return f"""
        You are an AI content moderator for Hinge dating app. Follow this exact 5-step process:

        STEP 1: Context Analysis
        - Content type: Message, profile bio, photo caption
        - Interaction stage: First message, ongoing conversation, or profile content
        - Tone: Analyze delivery style (respectful, aggressive, playful, demanding, threatening)
        - Cultural/generational context: Slang, references, communication style
        - Dating app expectations: Is this normal courtship behavior or boundary violation?

        STEP 2: Intent Assessment
        - Primary intent: Genuine connection, sexual interest, harassment, harm, self-harm, fraud
        - Harm potential: Immediate safety risk vs. boundary pushing vs. acceptable

        DATING APP CONTEXT: Remember this is a dating platform where:
        - Expressing romantic/sexual interest is expected and normal
        - "Hook up" language is standard dating app communication
        - Focus on RESPECT and BOUNDARIES rather than sexual content itself
        - Score based on tone, pressure, and respect for boundaries

        SCORING EXAMPLES:
        - "Want to hook up tonight?" = Score 2-3 (direct but expected dating app language)
        - "Hey sexy, want to hook up tonight?" = Score 2-3 (forward but normal dating app communication)
        - "Send me nudes now" = Score 7-8 (demanding, inappropriate boundary crossing)
        - "You better hook up or else" = Score 9-10 (threatening, harassment)

        STEP 3: Policy Application
        Identify the TOP 2 most relevant policy violations (if any):
        1. [Primary violation - highest harm level]
        2. [Secondary violation - if applicable]
        Focus on highest-impact violations rather than listing everything.

        Apply these official Hinge TRUST & SAFETY POLICIES:

            PROHIBITED CONTENT (Section 2d):
            1. Could reasonably be deemed to be offensive or to harass, upset, embarrass, alarm or annoy any other person;
            2. Is obscene, pornographic, violent or otherwise may offend human dignity, or contains nudity;
            3. Is abusive, insulting or threatening, discriminatory or that promotes or encourages racism, sexism, hatred or bigotry;
            4. Is illegal or encourages or facilitates any illegal activity including, without limitation, terrorism, human trafficking, money muling, child abuse and exploitation, or the incitement of violence or hatred;
            5. Encourages or facilitates any activity that may result in harm to the user or another person, including, but not limited to, promotion of self-harm, eating disorders, dangerous challenges, violent extremism, or harmful misinformation;
            6. Relates to commercial activities (including, without limitation, sales, competitions, employment or investment opportunities, promotions, and advertising, solicitation for services, "sugar daddy" or "sugar baby" relationships);
            7. Infringes upon any third party's rights (including, without limitation, intellectual property rights and privacy rights);
            8. Includes the image or likeness of another person without that person's consent;

            PROHIBITED ACTIONS (Section 2c):
            1. Misrepresent your identity, age, employment, qualifications, or affiliations;
            2. Harass, bully, stalk, intimidate, assault, defame, harm or otherwise mistreat any person;
            3. Solicit money or other items of value from another user;
            4. Use our Services in relation to fraud, a pyramid scheme, or other similar practice;
            5. Disclose private or proprietary information that you do not have the right to disclose;

            ENFORCEMENT (Section 4):
            - Immediate suspension or termination for Prohibited Content
            - Serious violations (illegal/harmful content) result in account ban
            - Automated tools and human reviewers enforce content rules
            - Priority detection of most serious harmful violations

        STEP 4: Evidence Documentation
        - NYT publishability standard, bias checking
        - Document reasoning and check for potential bias
        - Consider cultural/linguistic context

        STEP 5: Action Recommendation
        - Self-correction, user-centric outcomes, auto-ban triggers
        - Recommend action with appeal process
        - Human escalation for borderline cases

        STEP 6: Automation Decision
        You MUST include these fields in this exact format:
        - AI CONFIDENCE LEVEL: [Exact percentage, e.g., "95%" or "73%"]
        - USER VIOLATION HISTORY: [Assume: 1st offense / 2nd offense / 3rd offense / 4th+ offense]
        - AUTO-ACTION: [Specific automated decision based on logic below]

            PROGRESSIVE ENFORCEMENT LOGIC:
            FIRST OFFENSE ("First Speeding Ticket"):
            - SCORES 1-6: No action (educational opportunity)
            - SCORES 7-8: Warning only - "This content violates our guidelines. Please review our community standards."
            - SCORES 9-10: Content removal + educational warning (unless extreme safety threat)

            SECOND OFFENSE:
            - SCORES 4-6: Formal warning - "This is your second warning. Continued violations may result in account restrictions."
            - SCORES 7-10: Content removal + escalating warning

            THIRD OFFENSE:
            - SCORES 3+: Final warning - "This is your 3rd and final warning. You will be banned if this behavior continues."
            - Content removal + temporary restriction

            FOURTH OFFENSE:
            - Any violation = AUTOMATIC BAN

            IMMEDIATE BAN (Override progressive system):
            - Extreme safety threats: "I'll find you and hurt you"
            - Illegal content: Any unlawful material
            - Doxxing: Sharing private information

        Content to analyze: {content}

        USER VIEW (for display to content creator):
        You MUST format this section EXACTLY as shown below with no deviations:

        Score: [single number 1-10]
        Analysis: [brief professional explanation in one sentence]
        Policy Reference: [specific policy citation or "Complies with Hinge Community Guidelines"]
        Action: [clear action recommendation]
        """

    def create_specialized_prompt(self, content):
        """Create specialized prompt for hate speech, self-harm, and fraud detection"""
        return f"""
        You are an AI content moderator for Hinge dating app. Follow this exact 6-step process:

        STEP 1: Context Analysis
        - Content type: Message, profile bio, photo caption
        - Interaction stage: First message, ongoing conversation, or profile content
        - Tone: Analyze delivery style (respectful, aggressive, playful, demanding, threatening)
        - Cultural/generational context: Slang, references, communication style
        - Dating app expectations: Is this normal courtship behavior or boundary violation?

        STEP 2: Intent Assessment
        - Primary intent: [Genuine connection, harassment, hate speech, self-harm, fraud]
        - Harm potential: [Immediate safety risk vs. boundary pushing vs. acceptable]
        - SCORING: [Provide initial score reasoning]

        Critical Categories:
        HATE SPEECH: Targeting protected characteristics, slurs, discriminatory content
        SELF-HARM: Suicide ideation, self-injury references, eating disorders
        FRAUD: Romance scams, money solicitation, financial schemes

        STEP 3: Policy Application
        Identify the TOP 2 most relevant policy violations (if any):
        1. [Primary violation - highest harm level] Section [X]: [Policy description]
        2. [Secondary violation - if applicable] Section [X]: [Policy description]

        Key Policies:
        Section 2d.1: Offensive, harassing, upsetting content
        Section 2d.3: Abusive, discriminatory, promoting hatred/bigotry
        Section 2c.2: Harassment, bullying, stalking, intimidation
        Section 2c.3: Soliciting money or items of value
        Section 2c.4: Fraud, pyramid schemes

        STEP 4: Evidence Documentation
        - Document specific harmful elements and reasoning
        - Consider cultural/linguistic context
        - Check for bias in interpretation

        STEP 5: Action Recommendation
        - Recommend appropriate enforcement level
        - Consider progressive enforcement vs immediate action
        - For self-harm: NEVER recommend content removal - focus on crisis intervention

        STEP 6: Automation Decision
        - AI CONFIDENCE LEVEL: [Exact percentage, e.g., "95%"]
        - USER VIOLATION HISTORY: [Assume: 1st offense / 2nd offense / 3rd offense / 4th+ offense]
        - AUTO-ACTION: [Specific automated decision]

        SPECIAL SELF-HARM PROTOCOL:
        For self-harm content: Crisis intervention (NO content removal) + mental health resources + specialist escalation

        Content to analyze: {content}

        USER VIEW (for display to content creator):
        You MUST format this section EXACTLY as shown below with no deviations:

        Score: [single number 1-10]
        Analysis: [brief professional explanation in one sentence]
        Policy Reference: [specific policy citation or "Complies with Hinge Community Guidelines"]
        Action: [clear action recommendation]
        """

    def create_image_chain_of_thought_prompt(self):
        """Create Chain of Thought prompt specifically for image analysis"""
        return f"""You are an AI image moderator for Hinge dating app.
        Analyze this image using this 5-step process:

        STEP 1: Context Analysis
        - Identify image type (profile photo, inappropriate content, nudity, etc.)
        - Determine if suitable for dating app context
        - Assess image quality and authenticity

        STEP 2: Intent Assessment
        - Detect nudity, sexual content, or suggestive poses
        - Identify potential safety concerns (weapons, drugs, etc.)
        - Assess appropriateness for dating platform

        STEP 3: Policy Application
        Apply these official Hinge community guidelines:
        PRINCIPLES:
        {self.principles}

        STEP 4: Evidence Documentation
        - Document specific visual elements that violate or comply with policies
        - Note any text overlay or inappropriate symbols
        - Consider cultural context of image content

        STEP 5: Action Recommendation
        - Recommend approval, warning, or removal
        - Suggest human review if needed
        - Consider user education opportunities

        USER VIEW (for display to content creator):
        You MUST follow this EXACT format. Put each item on a separate line:

        Score: [number 1-10]

        Analysis: [brief professional explanation]

        Action: [clear recommendation]
        """





    def detect_critical_content(self, content):
        """Detect if content requires specialized handling for hate speech/self-harm/fraud"""
        # Keywords and patterns that indicate critical content
        hate_keywords = ['kill yourself', 'kys', 'hate all', 'hate women', 'hate men', 'nazi', 'hitler', 'supremacy', 'genocide', 'stupid bitch', 'fucking bitch', 'disgusting', 'go back to your', 'your country', 'racist', 'bigot', 'retard', 'faggot', 'nigger', 'wetback', 'chink']
        self_harm_keywords = ['suicide', 'kill myself', 'want to die', 'self harm', 'cutting', 'bulimia', 'anorexia', 'overdose', 'end my life']
        fraud_keywords = ['send money', 'wire transfer', 'inheritance', 'lottery', 'investment opportunity', 'sugar daddy', 'sugar baby', 'cash app', 'venmo', 'send me $', 'investment']

        content_lower = content.lower()

        # Check for hate speech indicators
        for keyword in hate_keywords:
            if keyword in content_lower:
                return True

        # Check for self-harm indicators
        for keyword in self_harm_keywords:
            if keyword in content_lower:
                return True

        # Check for fraud indicators
        for keyword in fraud_keywords:
            if keyword in content_lower:
                return True

        return False

    def moderate_content(self, content): # this function analyzes content
        """Analyze content and decide if it violates policies"""
        print(f"Analyzing: {content}") # show what we're checking

        # Route to specialized prompt for critical content
        if self.detect_critical_content(content):
            print("Using specialized prompt for critical content detection")
            prompt = self.create_specialized_prompt(content)
        else:
            print("Using general prompt")
            prompt = self.create_chain_of_thought_prompt(content)

        response = self.client.chat.completions.create(
             model="gpt-4",
             messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content # return the AI's moderation decision

    def moderate_image(self, uploaded_image): # this function analyzes images
        """Analyze image content and decide if it violates policies"""
        image_base64 = base64.b64encode(uploaded_image.read()).decode('utf-8')
        print(f"Analyzing image: {uploaded_image.name}") # show what we're checking

        # Create image-specific prompt
        prompt = self.create_image_chain_of_thought_prompt()

        # Call GPT-4V with image
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
            )
            result = response.choices[0].message.content
            print(f"GPT-4V Success: {len(result)} characters returned")  # Debug line
            return result
        except Exception as e:
            print(f"GPT-4V Error: {e}")  # Debug line
            return f"""STEP 1: Context Analysis
GPT-4V safety filters triggered - content requires human review

USER VIEW (for display to content creator):
Score: 10 (explicit content detected)
Analysis: Content flagged by AI safety systems
**Action: Human review required**"""

    def parse_score_from_response(self, ai_response):
        """Extract the 1-10 score from AI response"""
        # Look for "Score: X" pattern in the response
        score_match = re.search(r'Score:\s*(\d+)', ai_response)
        if score_match:
            return int(score_match.group(1))
        return None  # If no score found

    def run_evaluation(self):
        """Evaluate AI performance against ground truth dataset"""
        print("Running evaluation against ground truth...")

        # Step 1: Load your evaluation dataset
        with open("evaluation_dataset.json", "r") as file:
            test_cases = json.load(file)

        results = []

        # Step 2: Test each case and track with Langfuse
        for case in test_cases:
            content = case["content"]
            expected_range = case["expected_score_range"]

            ai_response = self.moderate_content(content)
            ai_score = self.parse_score_from_response(ai_response)

            # Check if score is within expected range
            is_accurate = False
            if ai_score is not None:
                is_accurate = expected_range[0] <= ai_score <= expected_range[1]

            results.append({
                "content": content,
                "ai_response": ai_response,
                "ai_score": ai_score,
                "expected_range": expected_range,
                "is_accurate": is_accurate
      })

        # Step 3: Generate accuracy report
        total_cases = len(results)
        accurate_cases = sum(1 for r in results if r["is_accurate"])
        accuracy_percentage = (accurate_cases / total_cases) * 100 if total_cases > 0 else 0

        # Identify false positives and negatives
        false_positives = []  # AI scored too high (overly restrictive)
        false_negatives = []  # AI scored too low (missed violations)

        for result in results:
            if result["ai_score"] is not None and not result["is_accurate"]:
                expected_min, expected_max = result["expected_range"]
                ai_score = result["ai_score"]

                if ai_score > expected_max:
                    false_positives.append({
                        "content": result["content"],
                        "ai_score": ai_score,
                        "expected_range": result["expected_range"],
                        "severity": ai_score - expected_max
                    })
                elif ai_score < expected_min:
                    false_negatives.append({
                        "content": result["content"],
                        "ai_score": ai_score,
                        "expected_range": result["expected_range"],
                        "severity": expected_min - ai_score
                    })

        # Print evaluation summary
        print(f"\n{'='*60}")
        print("EVALUATION RESULTS")
        print(f"{'='*60}")
        print(f"Total test cases: {total_cases}")
        print(f"Accurate predictions: {accurate_cases}")
        print(f"Overall accuracy: {accuracy_percentage:.1f}%")
        print(f"False positives: {len(false_positives)} (overly restrictive)")
        print(f"False negatives: {len(false_negatives)} (missed violations)")

        if false_positives:
            print(f"\nTOP FALSE POSITIVES (AI too restrictive):")
            for fp in sorted(false_positives, key=lambda x: x["severity"], reverse=True)[:3]:
                print(f"  - \"{fp['content'][:50]}...\" (AI: {fp['ai_score']}, Expected: {fp['expected_range']})")

        if false_negatives:
            print(f"\nTOP FALSE NEGATIVES (AI missed violations):")
            for fn in sorted(false_negatives, key=lambda x: x["severity"], reverse=True)[:3]:
                print(f"  - \"{fn['content'][:50]}...\" (AI: {fn['ai_score']}, Expected: {fn['expected_range']})")

        return {
            "results": results,
            "accuracy": accuracy_percentage,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "summary": {
                "total_cases": total_cases,
                "accurate_cases": accurate_cases,
                "fp_count": len(false_positives),
                "fn_count": len(false_negatives)
            }
        }

def main(): # this is where our program starts
     """Run the AI moderator demo"""
     print("=" * 50) # creates a line of equals signs
     print("HINGE MODERATION DEMO") #title
     print("=" * 50) # another line

     moderator = HingeAIModerator() #create our AI moderator

     # Run evaluation against ground truth dataset
     results = moderator.run_evaluation()
     print(f"Evaluated {len(results)} test cases")

        
if __name__ == "__main__": # this runs when we execute the file
     main()
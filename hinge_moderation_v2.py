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
from datetime import datetime # for timestamps - tracks when decisions are made
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
            #with open("hinge-terms-of-use.txt", "r") as file:
                # self.terms = file.read()
    
    def create_chain_of_thought_prompt(self, content):#instructors for the AI #self = "this specific AI moderator" #content = "the message you want me to analyze"
        """Create the 5-step Chain of Thought prompt"""
        return f"""
        You are an AI content moderator for Hinge dating app. Follow this exact 5-step process:
        STEP 1: Context Analysis
        - Identify the content type (profile bio, message, photo caption) and interaction stage. 
        - For messages: Determine if this is initial contact or ongoing conversation. 
        STEP 2: Intent Assessment
        - Harm scoring, account metadata, tiered response system
        - Analyze potential harm using tiered scoring system
        - Suicide (high harm), harassment (medium harm)
        STEP 3: Policy Application
        Apply these official Hinge community guidelines:
        PRINCIPLES:
        {self.principles}

        STEP 4: Evidence Documentation
        - NYT publishability standard, bias checking
        - Document reasoning and check for potential bias
        - Consider cultural/linguistic context
        STEP 5: Action Recommendation
        - Self-correction, user-centric outcomes, auto-ban triggers
        - Recommend action with appeal process
        - Human escalation for borderline cases 
        
        Content to analyze: {content}
   
        USER VIEW (for display to content creator):
        Score: [1-10 where 1=completly appropriate, 10=extremly harmful requiring immediate action]
        Analysis: [brief, professional explanation]
        **Action: [clear recommendation]**
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
        Score: [1-10 where 1=completely appropriate, 10=extremely harmful requiring immediate action]
        Analysis: [brief, professional explanation of image assessment]
        **Action: [clear recommendation]**
        """





    def moderate_content(self, content): # this function analyzes content
        """Analyze content and decide if it violates policies"""
        print(f"Analzying: {content}") # show what we're checking
        prompt = self.create_chain_of_thought_prompt(content) # Now you have the prompt stored in a variable.
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
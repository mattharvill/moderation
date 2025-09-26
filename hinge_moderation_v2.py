#!/usr/bin/env python3 #This tells your computer "run this file using Python 3." It's called a "shebang" line.
""" #this starts a docstring, a multi-line comment
Hinge AI Content Moderator - AI-Moderator tool used to identify and mitigate harmful content. 
Business Problem: 57.5K daily reports, 12-23% appeal rates, $5M annual cost
Solution: Chain of Thought AI with human-in-the-loop for high-risk cases
"""
import os # for reading API keys from environment - reads API key from .env file
import json # for handling structured data - formats responses
import base64 # converts image to base64
from openai import OpenAI # for calling GPT
from datetime import datetime # for timestamps - tracks when decisions are made
from dotenv import load_dotenv
class HingeAIModerator: # this is our main AI moderator. 
    # a class is like a blueprint. It contains all the functions and data our moderator needs

    """AI Content Moderator for Hinge Dating App""" # description of our class
    def __init__(self): # this runs when we create a new moderator
            print ("Starting Hinge AI Moderator...") # welcome message
            load_dotenv()
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #OpenAI connection
            
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


def main(): # this is where our program starts
     """Run the AI moderator demo"""
     print("=" * 50) # creates a line of equals signs
     print("HINGE MODERATION DEMO") #title
     print("=" * 50) # another line

     moderator = HingeAIModerator() #create our AI moderator
     test_content = "Hey sexy, send me your number" #sample content to test
     result = moderator.moderate_content(test_content) # analyze the content
     print(f"Result: {result}") # show the decision

if __name__ == "__main__": # this runs when we execute the file
     main()
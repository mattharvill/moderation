import streamlit as st
from hinge_moderation_v2 import HingeAIModerator

def extract_user_view(full_response):
    """Extract only the USER VIEW section from the AI response"""
    if "USER VIEW" in full_response:
        user_section = full_response.split("USER VIEW")[1]
        # Clean up the formatting
        user_section = user_section.replace("(for display to content creator):", "").strip()
        return user_section
    else:
        return "Unable to extract user view from response"

st.title("🔍 AI Content Moderator")
st.write("Demo")

# Demo mode toggle
demo_mode = st.checkbox("Demo Mode (show full AI reasoning)")

# Text input
content = st.text_area("Enter content to moderate:",
                      placeholder="Hey sexy, send me your number")
# Image upload option
uploaded_image = st.file_uploader("Or upload an image to moderate:",
                                 type=['png', 'jpg', 'jpeg'])

# Moderate button
if st.button("Analyze Content"):
    if content or uploaded_image:
        moderator = HingeAIModerator()

        if uploaded_image:
            result = moderator.moderate_image(uploaded_image)
        else:
            result = moderator.moderate_content(content)

        if demo_mode:
            st.write("### Full AI Analysis (for interview demo):")
            st.write(result)
        else:
            st.write("### Content Analysis:")
            user_view = extract_user_view(result)
            st.write(user_view)
    else:
        st.warning("Please enter some content or upload an image to analyze")
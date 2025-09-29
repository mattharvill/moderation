import streamlit as st
from hinge_moderation_v2 import HingeAIModerator

def extract_user_view(full_response):
    """Extract and format the USER VIEW section from the AI response"""
    try:
        if "USER VIEW" in full_response:
            # Find the USER VIEW section
            user_start = full_response.find("USER VIEW")
            user_section = full_response[user_start:]

            # Remove the header and any parenthetical text
            user_section = user_section.replace("USER VIEW (for display to content creator):", "")
            user_section = user_section.replace("USER VIEW", "", 1)
            user_section = user_section.strip()

            # Remove leading colon if present
            if user_section.startswith(":"):
                user_section = user_section[1:].strip()
        else:
            # Fallback: look for the standard format at the end
            lines = full_response.strip().split('\n')
            user_lines = []
            collecting = False

            for line in lines:
                line = line.strip()
                if line.startswith('Score:'):
                    collecting = True
                if collecting and line:
                    user_lines.append(line)

            if user_lines:
                user_section = '\n'.join(user_lines)
            else:
                return "Unable to extract user view from response"

        # Parse the components
        lines = [line.strip() for line in user_section.split('\n') if line.strip()]

        score = ""
        analysis = ""
        policy_ref = ""
        action = ""

        # Extract each component
        for line in lines:
            line = line.strip()  # Extra strip to be sure
            if line.startswith('Score:'):
                score = line[6:].strip()
                # Remove /10 suffix if present (but not individual digits)
                if score.endswith('/10'):
                    score = score[:-3].strip()
            elif line.startswith('Analysis:'):
                analysis = line[9:].strip()
            elif line.startswith('Policy Reference:'):
                policy_ref = line[17:].strip()
            elif line.startswith('Action:') or line.startswith('**Action:'):
                if line.startswith('**Action:'):
                    action = line[9:].replace('**', '').strip()
                else:
                    action = line[7:].strip()

        # Format the output consistently
        formatted_output = f"**Score: {score}**\n\n"

        if analysis:
            formatted_output += f"**Analysis:**\n{analysis}\n\n"

        if policy_ref:
            formatted_output += f"**Policy Reference:**\n{policy_ref}\n\n"

        if action:
            formatted_output += f"**Action:**\n{action}"

        return formatted_output.strip()

    except Exception:
        # If parsing fails completely, return raw USER VIEW section
        if "USER VIEW" in full_response:
            user_start = full_response.find("USER VIEW")
            return full_response[user_start:].strip()
        return "Unable to extract user view from response"

st.title("🔍 AI Content Moderator")
st.markdown("**Dating app moderation that understands context**")

# Initialize session state for content
if "test_content" not in st.session_state:
    st.session_state.test_content = ""

# Layout with columns
col1, col2 = st.columns([3, 1])

with col1:
    # Input section
    st.subheader("Content Input")
    content = st.text_area("Enter message to moderate:",
                          value=st.session_state.test_content,
                          placeholder="Hey sexy, send me your number",
                          height=100)

    # Image upload option
    uploaded_image = st.file_uploader("Or upload an image to moderate:",
                                     type=['png', 'jpg', 'jpeg'])

with col2:
    # Controls section
    st.subheader("Options")
    demo_mode = st.checkbox("Show full AI reasoning")

    # Quick test examples
    st.markdown("**Quick tests:**")
    if st.button("Hate Speech", type="secondary"):
        st.session_state.test_content = "You're disgusting, go back to your own country"
        st.rerun()
    if st.button("Self-Harm Content", type="secondary"):
        st.session_state.test_content = "I want to kill myself, nothing matters anymore"
        st.rerun()
    if st.button("Fraud", type="secondary"):
        st.session_state.test_content = "Send me $500 via Venmo and I'll send you nudes"
        st.rerun()

# Analyze button (full width)
analyze_button = st.button("🔍 Analyze Content", type="primary", use_container_width=True)

if analyze_button:
    if content or uploaded_image:
        with st.spinner("🤖 Analyzing content..."):
            moderator = HingeAIModerator()

            if uploaded_image:
                result = moderator.moderate_image(uploaded_image)
            else:
                result = moderator.moderate_content(content)

        # Success message
        st.success("✅ Analysis complete!")

        if demo_mode:
            # Demo mode with expandable sections (only show for detailed responses)
            with st.expander("🧠 Full AI Analysis (Technical View)", expanded=True):
                lines = result.split('\n')
                formatted_lines = []

                for line in lines:
                    line = line.strip()
                    if line.startswith('STEP '):
                        # Add blank line BEFORE each step (except the first one)
                        if formatted_lines:  # Only add space if this isn't the first step
                            formatted_lines.append('')

                        # Add the bold step header
                        formatted_lines.append(f"**{line}**")
                        formatted_lines.append('')  # Blank line AFTER step header

                    elif line.startswith('USER VIEW'):
                        # Stop processing before the USER VIEW section in demo mode
                        break

                    elif line:  # If the line is not empty, make it a bullet point
                        # Remove any existing bullet markers first
                        if line.startswith('- ') or line.startswith('• '):
                            line = line[2:]

                        # Add our consistent bullet point on its own line
                        formatted_lines.append(f"• {line}")

                # Join with double line breaks to ensure proper spacing
                formatted_result = '\n\n'.join(formatted_lines)
                st.markdown(formatted_result)

        # Always show user-facing results
        st.subheader("📊 Moderation Result")
        user_view = extract_user_view(result)

        # Fallback if extraction fails - show raw response for debugging
        if user_view == "Unable to extract user view from response":
            st.error("Unable to parse results properly")
            with st.expander("🔧 Debug Info"):
                st.text(result[:500])  # Show first 500 chars for debugging

            # Simple fallback formatting
            if "Score:" in result:
                lines = result.split('\n')
                for line in lines:
                    if line.strip().startswith("Score:"):
                        score_text = line.strip().replace("Score:", "").strip()
                        st.metric("Safety Score", score_text, help="1-10 scale, lower is safer")
                    elif line.strip().startswith("Analysis:"):
                        st.write("**Analysis:**")
                        st.write(line.replace("Analysis:", "").strip())
                    elif line.strip().startswith("Action:"):
                        st.write("**Recommended Action:**")
                        st.write(line.replace("Action:", "").strip())
            else:
                st.write(result)
        else:
            st.markdown(user_view)
    else:
        st.error("⚠️ Please enter some content or upload an image to analyze")
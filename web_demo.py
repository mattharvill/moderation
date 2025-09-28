import streamlit as st
from hinge_moderation_v2 import HingeAIModerator

def extract_user_view(full_response):
    """Extract and format the USER VIEW section from the AI response"""
    if "USER VIEW" in full_response:
        user_section = full_response.split("USER VIEW")[1]
        # Clean up the formatting - handle both formats
        user_section = user_section.replace("(for display to content creator):", "").strip()
        user_section = user_section.replace(":", "", 1).strip()  # Remove first colon if present

        # Parse and format the components
        lines = user_section.split('\n')
        formatted_output = ""

        # First check if there's a single line containing all elements
        full_text = user_section.strip()
        if "Score:" in full_text and "Analysis:" in full_text and "Action:" in full_text and len(lines) <= 2:
            # Extract score
            score_start = full_text.find("Score:") + 6
            analysis_start = full_text.find("Analysis:")
            score_text = full_text[score_start:analysis_start].strip()
            formatted_output += f"**Score: {score_text}**\n\n"

            # Extract analysis
            action_start = full_text.find("Action:")
            analysis_text = full_text[analysis_start + 9:action_start].strip()
            formatted_output += f"**Analysis:**\n{analysis_text}\n\n"

            # Extract action
            action_text = full_text[action_start + 7:].strip()
            formatted_output += f"**Action:**\n{action_text}\n\n"
        else:
            # Handle multi-line format
            for line in lines:
                line = line.strip()
                if line.startswith('Score:'):
                    # Normalize score format - remove "/10" if present and ensure consistent format
                    score_text = line.replace('Score:', '').strip()
                    score_text = score_text.replace('/10', '')  # Remove /10 if present
                    formatted_output += f"**Score: {score_text}**\n\n"
                elif line.startswith('Analysis:'):
                    formatted_output += f"**Analysis:**\n{line.replace('Analysis:', '').strip()}\n\n"
                elif line.startswith('**Action:') or line.startswith('Action:'):
                    action_text = line.replace('**Action:', '').replace('Action:', '').replace('**', '').strip()
                    formatted_output += f"**Action:**\n{action_text}\n\n"
                elif line and not line.startswith('Score:') and not line.startswith('Analysis:') and not line.startswith('Action:') and line != '**':
                    # Handle any other content but skip empty ** lines
                    formatted_output += f"{line}\n\n"

        return formatted_output.strip()
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

            # Format the full response with consistent structure
            lines = result.split('\n')
            formatted_lines = []

            for line in lines:
                line = line.strip()
                if line.startswith('STEP '):
                    # Add spacing before each step and make it bold
                    formatted_lines.append('')  # Empty line for spacing
                    formatted_lines.append(f"**{line}**")
                    formatted_lines.append('')  # Empty line after step header
                elif line.startswith('USER VIEW'):
                    # Add separator before USER VIEW
                    formatted_lines.append('')
                    formatted_lines.append('---')
                    formatted_lines.append('')
                    formatted_lines.append(f"**{line}**")
                    formatted_lines.append('')  # Empty line after USER VIEW header
                elif line.startswith('- ') or line.startswith('1. ') or line.startswith('2. '):
                    # Format bullet points and numbered lists
                    formatted_lines.append(f"• {line[2:]}")
                elif line and not line.startswith('STEP') and not line.startswith('USER VIEW'):
                    # Regular content lines
                    formatted_lines.append(line)

            # Join and display with markdown
            formatted_result = '\n'.join(formatted_lines)
            st.markdown(formatted_result)
        else:
            st.write("### Content Analysis:")
            user_view = extract_user_view(result)

            # Fallback if extraction fails - show raw response for debugging
            if user_view == "Unable to extract user view from response":
                st.write("**Debug - Raw AI Response:**")
                st.text(result[:500])  # Show first 500 chars for debugging

                # Simple fallback formatting
                if "Score:" in result:
                    lines = result.split('\n')
                    formatted_lines = []
                    for line in lines:
                        if line.strip().startswith("Score:"):
                            formatted_lines.append(f"**{line.strip()}**")
                        elif line.strip().startswith("Analysis:"):
                            formatted_lines.append(f"**Analysis:**")
                            formatted_lines.append(line.replace("Analysis:", "").strip())
                        elif line.strip().startswith("Action:"):
                            formatted_lines.append(f"**Action:**")
                            formatted_lines.append(line.replace("Action:", "").strip())

                    for line in formatted_lines:
                        st.write(line)
                else:
                    st.write(result)
            else:
                st.write(user_view)
    else:
        st.warning("Please enter some content or upload an image to analyze")
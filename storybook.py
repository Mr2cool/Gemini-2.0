import streamlit as st
import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fpdf import FPDF
import tempfile

# Function to generate story text using the Gemini-2.0-flash-exp model
def generate_story(api_key, prompt, age_group, theme, characters, moral):
    detailed_prompt = f"""
    Create a children's story with the following details:
    - Age group: {age_group}
    - Theme: {theme}
    - Main characters: {characters}
    - Moral or lesson: {moral}
    - Additional requirements: {prompt}
   
    The story should be appropriate for children, engaging, and include a clear beginning, middle, and end.
    Please format the story with proper paragraphs and include a title.
    """
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
        data = {
            "contents": [{"parts": [{"text": detailed_prompt}]}],
            "generation_config": {"temperature": 0.7, "maxOutputTokens": 2048}
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        story_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        return {"text": story_text.strip(), "images": []}
    except requests.RequestException as e:
        return {"text": f"API Error: {str(e)}", "images": []}
    except (KeyError, IndexError) as e:
        return {"text": f"Error parsing API response: {str(e)}", "images": []}

# Function to generate placeholder images
def generate_placeholder_image(scene_text):
    width, height = 400, 300
    image = Image.new("RGB", (width, height), color=(255, 255, 240))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Use default font to avoid external dependencies
    text = f"Illustration:\n{scene_text[:100]}"  # Truncate long text
    draw.multiline_text((10, 10), text, fill=(0, 0, 0), font=font)
    return image

# Function to create a PDF from story text and images
def create_pdf(story_title, story_text, images):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)  # Use built-in font
    pdf.cell(0, 10, story_title, ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, story_text.encode('latin1', 'replace').decode('latin1'))
   
    temp_files = []
    for idx, image in enumerate(images):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            image.save(tmp_file, format="PNG")
            temp_files.append(tmp_file.name)
        pdf.add_page()
        pdf.set_font("Helvetica", size=14)
        pdf.cell(0, 10, f"Scene {idx+1}", ln=True, align="C")
        pdf.image(tmp_file.name, x=10, y=30, w=pdf.w - 20, type="PNG")
   
    pdf_data = pdf.output(dest="S").encode("latin1", "replace")
    for f in temp_files:
        os.remove(f)
    return BytesIO(pdf_data)

def main():
    st.set_page_config(page_title="Children's Storybook Generator", page_icon="📚", layout="wide")
   
    # Custom CSS for styling
    st.markdown("""
    <style>
    .title { text-align: center; color: #1E88E5; font-size: 3rem; }
    .storybox { background-color: #f9f9f9; border-radius: 10px; padding: 20px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)
   
    st.markdown("<h1 class='title'>📚 Children's Storybook Generator</h1>", unsafe_allow_html=True)
    st.markdown("Create magical stories for children using AI! Fill in the details below.")
   
    # Sidebar for API and settings
    with st.sidebar:
        st.header("API Configuration")
        api_key = st.text_input("Enter your Gemini API Key:", type="password")
       
        st.header("Story Settings")
        age_group = st.select_slider("Age Group", options=["3-5 years", "6-8 years", "9-12 years"])
        theme = st.selectbox("Theme", ["Adventure", "Fantasy", "Friendship", "Nature", "Learning", "Family", "Animals", "Space", "Custom"])
        if theme == "Custom":
            theme = st.text_input("Enter custom theme:", key="custom_theme")

    # Two-column layout
    col1, col2 = st.columns([1, 1])
   
    with col1:
        st.header("Story Details")
        characters = st.text_input("Main Characters (separated by commas):")
        moral = st.text_input("Moral or Lesson of the Story:")
        prompt = st.text_area("Additional Story Elements:", height=150)
        generate_button = st.button("✨ Generate Storybook", type="primary", use_container_width=True)
   
    with col2:
        # Initialize session state
        if "story" not in st.session_state:
            st.session_state.story = ""
            st.session_state.title = "Your Story Will Appear Here"
            st.session_state.images = []
       
        st.header(st.session_state.title)
       
        # Generate story and images on button click
        if generate_button:
            if not api_key:
                st.error("Please enter your Gemini API Key.")
            elif not (characters and moral and prompt):
                st.error("Please fill in all story details.")
            else:
                with st.spinner("Creating your magical story... ✨"):
                    result = generate_story(api_key, prompt, age_group, theme, characters, moral)
                    story_lines = result["text"].split('\n', 1)
                    st.session_state.title = story_lines[0].strip('# ') if len(story_lines) > 1 else "Generated Story"
                    st.session_state.story = story_lines[1].strip() if len(story_lines) > 1 else result["text"]
                   
                    # Generate placeholder images
                    st.session_state.images = [
                        generate_placeholder_image("Scene 1: The adventure begins."),
                        generate_placeholder_image("Scene 2: A new friend appears.")
                    ]
                    st.write(f"Debug: Generated {len(st.session_state.images)} images")

        # Display story and images
        if st.session_state.story:
            st.markdown(f"<div class='storybox'>{st.session_state.story}</div>", unsafe_allow_html=True)
            if st.session_state.images:
                st.subheader("Illustrations")
                for idx, img in enumerate(st.session_state.images):
                    try:
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        st.image(buf.getvalue(), caption=f"Scene {idx+1}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Error displaying image {idx+1}: {str(e)}")
            else:
                st.warning("No images available to display.")
           
            # PDF download button
            try:
                pdf_file = create_pdf(st.session_state.title, st.session_state.story, st.session_state.images)
                st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_file,
                    file_name="storybook.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Failed to generate PDF: {str(e)}")

if __name__ == "__main__":
    main()

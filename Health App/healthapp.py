import streamlit as st
import requests
import json

##############################################
# About BazAI
##############################################

st.set_page_config(page_title="BazAI: Personalized Health Recommendation App", layout="wide", page_icon="🏃")
st.markdown("""
# BazAI: Personalized Health Recommendation App

**Purpose:**  
BazAI is a personalized exercise recommendation app designed to suggest appropriate physical activities based on your name, height, weight, and current emotional state. The app aims to align exercise routines with your emotional well-being, promoting holistic health.

**Target Audience:**  
Individuals seeking tailored exercise guidance, particularly those who want to synchronize physical activity with their emotional state.

---

## Features
- **User Input:** Collects your details (name, height, weight) and current feeling via a dropdown menu.
- **BMI Calculation:** Computes your Body Mass Index (BMI) using:  
  \[
  \text{BMI} = \frac{\text{weight (kg)}}{(\text{height (m)})^2}
  \]
- **Exercise Intensity Determination:**  
  - **Light:** Low BMI or if feeling *stressed*/*tired*  
  - **Moderate:** Normal BMI or if feeling *neutral*  
  - **Intense:** High BMI or if feeling *happy*/*energetic*
- **Personalized Recommendations:** Displays a list of tailored exercises.
- **Input Validation:** Warns if any required field is left blank.
- **Clean UI:** Simple, intuitive, and optimized for both desktop and mobile devices.

## Technology Stack
- **Backend:** Python  
- **Frontend:** Streamlit  
- **Data Storage:** Exercise recommendations are stored in a Python dictionary.

**Privacy Note:** Your input is processed only within the app and is not stored externally.

---

For support or more information, please contact: [support@bazai.com](mailto:support@bazai.com) or visit [www.bazai.com](http://www.bazai.com).
""")
st.markdown("---")

##############################################
# Sidebar: Optional Gemini API Key for Extra Health Tips
##############################################

st.sidebar.header("Optional: Gemini API Key")
gemini_api_key = st.sidebar.text_input("Enter your Gemini API Key for additional health tips:", type="password")

##############################################
# Exercise Recommendation Functions
##############################################

# Define exercise recommendations based on intensity level
exercise_recommendations = {
    "Light": ["Yoga", "Walking", "Stretching"],
    "Moderate": ["Jogging", "Pilates", "Brisk Walking"],
    "Intense": ["Strength Training", "Running", "HIIT"]
}

# Define an ordering for intensity levels
intensity_order = {"Light": 1, "Moderate": 2, "Intense": 3}

# Compute BMI using weight and height
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # Convert height to meters
    if height_m > 0:
        return weight / (height_m ** 2)
    return None

# Determine intensity based on BMI
def bmi_intensity(bmi):
    if bmi < 18.5:
        return "Light"
    elif bmi < 25:
        return "Moderate"
    else:
        return "Intense"

# Determine intensity based on the user's current feeling
def feeling_intensity(feeling):
    if feeling in ["Stressed", "Tired"]:
        return "Light"
    elif feeling == "Neutral":
        return "Moderate"
    elif feeling in ["Happy", "Energetic"]:
        return "Intense"
    else:
        return None

# Combine BMI and feeling intensity by choosing the lower intensity level for safety
def overall_intensity(bmi_level, feeling_level):
    if intensity_order[bmi_level] <= intensity_order[feeling_level]:
        return bmi_level
    else:
        return feeling_level

##############################################
# Gemini‑2.0‑flash‑exp Health Tips Function
##############################################

def generate_health_tips(api_key, bmi, final_intensity, feeling, name):
    prompt = f"""
    Provide additional health tips for {name}, who has a BMI of {bmi:.2f}, a recommended exercise intensity of {final_intensity}, and is currently feeling {feeling}.
    Include advice on diet, exercise, and lifestyle modifications to improve overall health.
    """
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generation_config": {"temperature": 0.7, "maxOutputTokens": 2048}
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        health_tips_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        return health_tips_text.strip()
    except requests.RequestException as e:
        return f"API Error: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: {str(e)}"

##############################################
# Main UI: Collect User Input and Display Recommendations
##############################################

st.header("Get Your Personalized Exercise Recommendation")

# Collect user input for name, height, weight, and current feeling
name = st.text_input("Enter your name:")
height = st.number_input("Enter your height (in cm):", min_value=0.0, step=0.1)
weight = st.number_input("Enter your weight (in kg):", min_value=0.0, step=0.1)
feeling = st.selectbox("How are you feeling today?", ["Happy", "Neutral", "Stressed", "Tired", "Energetic"])

if st.button("Get Recommendation"):
    # Input Validation
    if not name or height <= 0 or weight <= 0:
        st.warning("Please provide valid inputs for name, height, and weight.")
    else:
        # Calculate BMI and display it
        bmi = calculate_bmi(weight, height)
        st.write(f"**{name}**, your BMI is: **{bmi:.2f}**")
        
        # Determine exercise intensity based on BMI and current feeling
        bmi_level = bmi_intensity(bmi)
        feeling_level = feeling_intensity(feeling)
        final_intensity = overall_intensity(bmi_level, feeling_level)
        st.write(f"**Recommended Exercise Intensity:** {final_intensity}")
        
        # Display tailored exercise recommendations
        exercises = exercise_recommendations.get(final_intensity, [])
        if exercises:
            st.write("**Tailored Exercise Recommendations:**")
            for exercise in exercises:
                st.write(f"- {exercise}")
        else:
            st.write("No recommendations available at this time.")
        
        # Fetch additional health tips from Gemini‑2.0‑flash‑exp if API key is provided
        if gemini_api_key:
            with st.spinner("Fetching additional health tips..."):
                health_tips = generate_health_tips(gemini_api_key, bmi, final_intensity, feeling, name)
                st.markdown("### Additional Health Tips")
                st.write(health_tips)
        else:
            st.info("Provide your Gemini API Key in the sidebar to receive extra health tips.")

# Gemini-2.0
BazAI
Below is a sample `README.md` file for your Children's Storybook Generator project:

---

# Children's Storybook Generator

**Children's Storybook Generator** is a Streamlit-based application that uses the Gemini‑2.0‑flash‑exp model to create engaging children's stories. Users can enter various story details (age group, theme, main characters, moral, and additional requirements) and receive a generated story along with placeholder illustrations. The generated story can also be downloaded as a PDF.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Functionality](#functionality)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [Support and Contact](#support-and-contact)

---

## Introduction

**Purpose:**  
The Children's Storybook Generator app is designed to generate magical and engaging stories for children using AI. By providing specific story parameters like age group, theme, characters, and moral, users can create unique stories that include proper structure and formatting.

**Target Audience:**  
This tool is ideal for educators, parents, and anyone looking to create personalized children's stories for entertainment or educational purposes.

---

## Features

- **User Input:**  
  Collects essential details including age group, theme, main characters, moral, and any additional story elements.
  
- **Story Generation:**  
  Uses the Gemini‑2.0‑flash‑exp API to generate a story with a clear beginning, middle, and end, along with a title.
  
- **Placeholder Illustrations:**  
  Generates simple placeholder images for key story scenes using the Pillow library.
  
- **PDF Creation:**  
  Compiles the generated story and illustrations into a downloadable PDF.
  
- **Input Validation:**  
  Provides error messages for missing or invalid inputs to ensure a smooth user experience.
  
- **Clean and Responsive UI:**  
  Built with Streamlit for an intuitive, mobile-friendly design.

---

## Functionality

1. **User Input:**
   - Users enter story details such as age group, theme, main characters, moral, and additional prompts.
   - An API key for Gemini‑2.0‑flash‑exp is required to generate the story.

2. **Story Generation:**
   - A detailed prompt is constructed based on user input.
   - The app sends the prompt to the Gemini‑2.0‑flash‑exp model to generate a story.

3. **Image Generation:**
   - Placeholder images are generated for specific story scenes.

4. **PDF Generation:**
   - The story text and images are compiled into a PDF that users can download.

---

## Technology Stack

- **Backend:** Python
- **Frontend:** Streamlit
- **API:** Gemini‑2.0‑flash‑exp for AI-generated content
- **Image Processing:** Pillow (PIL)
- **PDF Generation:** FPDF

---

## Installation and Setup

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)  
- Required Python packages (see [requirements.txt](./requirements.txt))

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/childrens-storybook-generator.git
   cd childrens-storybook-generator
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   streamlit run app.py
   ```

4. **Access the App:**

   Open the provided local URL in your browser.

---

## Usage

1. **API Configuration:**
   - Enter your Gemini‑2.0‑flash‑exp API key in the sidebar.

2. **Story Settings:**
   - Select the age group, theme, and fill in the custom theme if needed.

3. **Story Details:**
   - Provide the main characters, moral, and any additional story elements.
   
4. **Generate the Story:**
   - Click the "✨ Generate Storybook" button to create your story.
   - The app displays the generated story along with placeholder illustrations.
   
5. **Download the Story:**
   - Use the provided download button to save the story as a PDF.

---

## Future Enhancements

- **Enhanced Illustrations:**  
  Replace placeholder images with AI-generated illustrations.

- **Advanced Formatting:**  
  Improve text formatting and styling of the generated story.

- **User Profiles:**  
  Allow users to save their stories for future reference.

- **Additional API Integration:**  
  Support additional AI models for varied storytelling styles.

---

## Support and Contact

For inquiries or support, please contact:  
**Email:** [support@bazai.com](mailto:support@bazai.com)  
**Website:** [www.bazai.com](http://www.bazai.com)

---

Feel free to contribute to the project or suggest improvements via GitHub. Enjoy generating magical stories for children with BazAI!

---

This README provides a comprehensive overview of the project, covering its purpose, features, setup instructions, and future directions. Adjust the contact information and repository URL as needed for your project.

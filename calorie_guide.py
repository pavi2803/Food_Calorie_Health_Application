# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image

# ------------------------------
# CONFIG & SETUP
# ------------------------------
# Configure the SDK with your API key
# Make sure your .streamlit/secrets.toml file contains: [GOOGLE_API_KEY]
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except FileNotFoundError:
    st.error("Secrets file not found. Please add your API key to .streamlit/secrets.toml")
    st.stop()

# Initialize the model
# Using 'gemini-1.5-flash' as it is fast and capable for vision tasks
model = genai.GenerativeModel('gemini-1.5-flash')

# ------------------------------
# FUNCTION TO CALL GEMINI (SDK Version)
# ------------------------------
def get_gemini_response(input_prompt_text, input_image):
    try:
        # The SDK handles PIL images directly.
        # Crucially, we pass the prompt and image as a list directly to the function.
        # NO 'parts=' keyword is used here. This fixes the error you saw previously.
        response = model.generate_content([input_prompt_text, input_image])
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {e}"

# ------------------------------
# STREAMLIT UI
# ------------------------------
st.set_page_config(page_title="Calorie App", layout="centered")
st.header("Know your Food Better 🍎")
st.write("Upload an image to get calorie and health insights:")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    # resize for display if it's huge, to save bandwidth
    display_image = image.copy()
    display_image.thumbnail((700, 700))
    st.image(display_image, caption="Uploaded Image.", use_column_width=False)

# The Prompt
prompt_template = """
You are a nutritionist. Analyze the image provided.
Do the following tasks:

1. Firstly, if the image is NOT a food item (e.g., a person, a car, an animal), explicitly state: "It's not a food item, please upload a food image" and STOP further analysis.

2. If it IS a food item, proceed with the following format:

## **Dish Name:** [Name of the dish]

---

### **Breakdown & Calorie Estimates:**
List the distinct items visible on the plate:

* **[Food item 1 Name]:** (~ [approx calories] kcal)
* **[Food item 2 Name]:** (~ [approx calories] kcal)
* *(Continue for all major items...)*

---

### **Ingredient Analysis:**

**1. [Food item 1 Name]**
* ✅ **The Good:** [List healthy ingredients/nutrients]
* ⚠️ **The Concerns:** [List unhealthy ingredients, excess sugar/salt/fats]

**2. [Food item 2 Name]**
* ✅ **The Good:** [...]
* ⚠️ **The Concerns:** [...]

---

### **Total Summary:**

**Total Estimated Calories:** ~ [Sum of calories] kcal

**Daily Context:** This meal represents approximately **[Percentage]%** of a standard 2000 kcal daily intake recommendations.
"""


submit = st.button("Tell me about this food")

if submit:
    if image is not None:
        with st.spinner("Analyzing your food... please wait..."):
            response_text = get_gemini_response(prompt_template, image)
            st.subheader("Food Calorie Insights:")
            st.markdown(response_text)
    else:
        st.warning("Please upload an image first.")
# -*- coding: utf-8 -*-
import streamlit as st
import requests
import base64
from PIL import Image
import io

# ------------------------------
# CONFIG
# ------------------------------
API_KEY = st.secrets["GOOGLE_API_KEY"]  # uses your existing secret
MODEL = "models/gemini-1.5-flash-latest"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta2/{MODEL}:generateContent"

# ------------------------------
# FUNCTION TO CALL GEMINI
# ------------------------------
def get_gemini_response(input_prompt, image: Image.Image):
    try:
        # Convert image to bytes
        fmt = image.format or "PNG"
        mime_type = "image/jpeg" if fmt.upper() == "JPEG" else "image/png"
        img_bytes_io = io.BytesIO()
        image.save(img_bytes_io, format=fmt)
        img_bytes = img_bytes_io.getvalue()

        # Base64 encode image
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        # Build request payload
        payload = {
            "prompt": [
                {
                    "content": [
                        {"text": input_prompt},
                        {"blob": {"mime_type": mime_type, "data": img_b64}}
                    ]
                }
            ],
            "temperature": 0.7,
            "candidate_count": 1
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        # Make POST request
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extract generated text
        return result["candidates"][0]["content"][0]["text"]

    except Exception as e:
        return f"❌ Error generating response: {e}"

# ------------------------------
# STREAMLIT UI
# ------------------------------
st.set_page_config(page_title="Calorie")
st.header("Know your Food Better")
st.write("Upload an image to get calorie and health insights:")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about this food")

input_prompt = """
Do the following tasks:
Firstly, if the image is not a food item, just say "It's not a food item, please upload a food image".
If it's a food item, proceed with the following:
Name the Dish in the format - "This is - "
List the items present in the food plate or display:

Food item 1: (approx calories - .....)

Food item 2: (approx calories - .....)
----
----

Display possible harmful ingredients and healthy ingredients present in the food that might impact health:
1. Food item 1:

    What's good in it?
    * Healthy ingredient 1..
    * Healthy ingredient 2..
    ---
    ---
    What's bad in it?
    * Unhealthy ingredient 1..
    * Unhealthy ingredient 2..
    ---
    ---
2. Food item 2:

    What's good in it?
    * Healthy ingredient 1..
    * Healthy ingredient 2..
    ---
    ---
    What's bad in it?
    * Unhealthy ingredient 1..
    * Unhealthy ingredient 2..
    ---
    ---
---

Total Estimated Calories:
and display the proportion of this calorie with respect to total daily necessary calorie intake for a person. Do this in the format, "which is ...% of your daily calorie consumption"
"""

if submit and uploaded_file:
    response_text = get_gemini_response(input_prompt, image)
    st.subheader("Food Calorie Insights:")
    st.write(response_text)

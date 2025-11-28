# -*- coding: utf-8 -*-
"""
Updated on July 16, 2025

@author: Pavithra
"""

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import io

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Correct model name
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

import base64

import base64

def get_gemini_response(input_prompt, image: Image.Image):
    try:
        # Determine format and MIME type
        fmt = image.format  # 'JPEG', 'PNG', etc.
        mime_type = "image/jpeg" if fmt == "JPEG" else "image/png"

        # Convert image to bytes
        img_bytes_io = io.BytesIO()
        image.save(img_bytes_io, format=fmt)
        img_bytes = img_bytes_io.getvalue()

        # Encode bytes as base64
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        # Prepare request in the correct format
        response = model.generate_content([
            {"text": input_prompt},
            {
                "blob": {
                    "mime_type": mime_type,
                    "data": img_b64
                }
            }
        ])
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {e}"



st.set_page_config(page_title="Calorie")
st.header("Know your Food Better")
st.write("Upload an image to get calorie and health insights:")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit = st.button("Tell me about this food")

input_prompt = """
Do the following tasks:
Firstly, if the image is not a food item, Just say "Its not a food item, Please upload a food image".
If it's a food item, proceed with the following:
Name the Dish in the format - "This is - "
List the items present in the food plate or in the display in the below format:

Food item 1: (approx calories - .....)

Food item 2: (approx calories - .....)
----
----

Display Possible harmful ingredients and healthy ingredients present in the food that might impact health in the following format:
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
    response = get_gemini_response(input_prompt, image)
    st.subheader("Food Calorie Insights:")
    st.write(response)

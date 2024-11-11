# -*- coding: utf-8 -*-
"""
Created on Wed May 22 13:54:55 2024

@author: Pavithra
"""

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyB4btXoYPwPUSAz37MJbyt7xUQwabRcIVg")


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Assuming image is a list of dictionaries with mime type and data
    response = model.generate_content([input_prompt, image[0]['data']])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
        
        
st.set_page_config(page_title="Calorie")

st.header("Know your Food Better")

st.write("Upload the image for which you'd like to know the calorie information - ")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""    

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
    ---
    
Total Estimated Calories:
    and display the proportion of this calorie with respect to total daily necessary calorie intake for a person. Do this in the format, "which is ...% of your daily calorie consumption"
"""

## If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("Food Calorie Insights:")
    st.write(response)
    

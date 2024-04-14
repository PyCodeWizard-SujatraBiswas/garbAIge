from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
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


# Initialize streamlit app
st.set_page_config(page_title="garbAIge")

st.header("Ask your AI Garbage expert")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Please Give the image of dumped Garbage......", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Give Garbage Info")

input_prompt = """

Prompt:
Develop a generative AI model to accurately analyze images of garbage items and efficiently separate them into distinct categories:

1. Categorized List of Wastes:
   - Organic Waste: [List of items accurately identified as organic waste]
   - Hazardous Waste: [List of items accurately identified as hazardous waste]
   - Solid Waste: [List of items accurately identified as solid waste]
   - Liquid Waste: [List of items accurately identified as liquid waste]
   - Recyclable Waste: [List of items accurately identified as recyclable waste]

2. Environmental Impact Data:
   - Organic Waste: [Percentage of environmental harm caused by accurately identified organic waste]
   - Hazardous Waste: [Percentage of environmental harm caused by accurately identified hazardous waste]
   - Solid Waste: [Percentage of environmental harm caused by accurately identified solid waste]
   - Liquid Waste: [Percentage of environmental harm caused by accurately identified liquid waste]
   - Recyclable Waste: [Percentage of environmental harm caused by accurately identified recyclable waste]

   Note: The sum of all percentages of environmental impact data equals 100%. This ensures a comprehensive understanding of the environmental implications associated with different types of waste accurately identified from the given image.
"""

# If submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Generating Garbage info....")
    st.write(response)

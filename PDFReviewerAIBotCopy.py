# to run file: streamlit run <filename>.py

import streamlit as streamlit
import os
import fitz  # PyMuPDF
from io import BytesIO
import base64
import copy
import hashlib
import io
import json
import mimetypes
import pathlib
import pprint
import requests
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting


import PIL.Image
import IPython.display
from IPython.display import Markdown

os.environ['GEMINI_API_KEY'] = 'AIzaSyCwgkHMh5XhyDqiDIwh5d3XUrD5qhSAK5o'

import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# try:
#     model = 'gemini-1.5-pro' # @param {isTemplate: true}
#     contents_b64 = 'W10=' # @param {isTemplate: true}
#     generation_config_b64 = 'eyJ0ZW1wZXJhdHVyZSI6MSwidG9wX3AiOjAuOTUsInRvcF9rIjo0MCwibWF4X291dHB1dF90b2tlbnMiOjgxOTJ9' # @param {isTemplate: true}
#     safety_settings_b64 = "e30="  # @param {isTemplate: true}
#     gais_contents = json.loads(base64.b64decode(contents_b64))
#     generation_config = json.loads(base64.b64decode(generation_config_b64))
#     safety_settings = json.loads(base64.b64decode(safety_settings_b64))
#     stream = False
#     models = genai.list_models()
#     print("Available models:", models)
# except Exception as e:
#     print("Error Fetching the models:", str(e))

#model = genai.GenerativeModel('gemini-1.5-pro')

def generate():
    vertexai.init(project="gen-lang-client-0042161442", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    responses = model.generate_content(
        [],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

#generate()

# Function definition for generating the response
def get_gemini_response(input_prompt, pdf_text):
    try:
        model = genai.get_model('gemini-1.5-pro')
        #model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        return f"Error fetching model: {str(e)}"
    #model = genai.GenerativeModel('gemini-1.5-pro')
    #model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config,)
    #model = genai.get_model('gemini-pro-vision')

    if input_prompt == "":
        response = model.generate_content([input_prompt, pdf_text])
    else:
        response = model.generate_content(pdf_text)
    return response.text

streamlit.set_page_config(page_title='AI DOC ReviewerBot')

streamlit.header('AI_DOCUMENT_REVIEWER_PILOT')

input_prompt = streamlit.text_input('Input Prompt:', key='input')

upload_file = streamlit.file_uploader('Choose a PDF file to review:', type=['pdf'])

pdf_text = ""

if upload_file is not None:
    # Read the PDF from the uploaded file
    with fitz.open(stream=BytesIO(upload_file.read()), filetype="pdf") as doc:
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()  # Extract text from each page
    streamlit.text_area("PDF Content:", pdf_text, height=300)

submit = streamlit.button('Review this PDF as a copy editor with 10+ years of experience in reviewing technical content like user guides, release notes, and so on for software and hardware products.')

if submit:
    response = get_gemini_response(input_prompt, pdf_text)
    streamlit.subheader('The review comments on this PDF are:')
    streamlit.write(response)

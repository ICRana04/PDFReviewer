# to run file: streamlit run <filename>.py

import streamlit as streamlit
import pathlib
import textwrap
import os

from PIL import pdf

os.environ['GEMINI_API_KEY'] = '<YOUR_API_KEY>'

import google.generativeai as generativeai

generativeai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Function definition for generating the response

def get_gemini_response(input, pdf):
    model = generativeai.GenerativeModel('gemini-pro-vision')

    if input ="":
        response = model.generate_content([input, pdf])
    else:
        response = model.generate_content(pdf)
    return response.text

streamlit.set_page_config(page_title = 'AI DOC ReviewerBot')

streamlit.header('AI_DOCUMENT_REVIEWER_PILOT')

input = streamlit.text_input('Input Prompt :', key = 'input')

upload_file = streamlit.file_uploader('Choose a PDF file to review:', type = ['pdf'])

source_pdf_file = ""

if upload_file is not None:
    source_pdf_file = pdf.open(upload_file)
    streamlit.pdf(pdf, caption='Browser and select PDF to Upload', use_column_width = True)

submit = streamlit.button('Review this PDF as a copy editor with 10+ years of experience in reviewing technical content like user guide, release notes, and so on for software and hardware products.')

if submit:
    response = get_gemini_response(input, pdf)
    streamlit.subheader('The review PDF comments are:')
    streamlit.write(response)
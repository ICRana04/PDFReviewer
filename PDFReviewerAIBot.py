# to run file: streamlit run <filename>.py

import streamlit as streamlit
import os
import fitz  # PyMuPDF

os.environ['GEMINI_API_KEY'] = '<YOUR_API_KEY>'

import google.generativeai as generativeai

generativeai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Function definition for generating the response
def get_gemini_response(input_prompt, pdf_text):
    model = generativeai.GenerativeModel('gemini-1.5-pro')

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
    # Use fitz to read the PDF
    with fitz.open(upload_file) as doc:
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()  # Extract text from each page
    streamlit.text_area("PDF Content:", pdf_text, height=300)

submit = streamlit.button('Review this PDF as a copy editor with 10+ years of experience in reviewing technical content like user guides, release notes, and so on for software and hardware products.')

if submit:
    response = get_gemini_response(input_prompt, pdf_text)
    streamlit.subheader('The review PDF comments are:')
    streamlit.write(response)

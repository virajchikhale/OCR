import streamlit as st
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.protobuf.json_format import MessageToDict
from docx import Document
from data_extractor import DataExtractor
import io


from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
# api_key = st.secrets["GEMINI_API_KEY"]
import os

# Access secrets as environment variables
api_key = os.getenv("GEMINI_API_KEY")
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("VISION_API")


# Set up Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["private_key"]


def extract_text_from_pdf(content):
    """Extract text from a PDF file using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    request = {
        'requests': [{
            'input_config': types.InputConfig(content=content, mime_type='application/pdf'),
            'features': [{'type': vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
        }]
    }

    # Perform the OCR
    response = client.batch_annotate_files(requests=request['requests'])

    # Process the response
    text = ""
    for file_response in response.responses:
        if file_response.error.message:
            raise Exception(f"Error processing PDF: {file_response.error.message}")
        for page in file_response.responses:
            text += page.full_text_annotation.text

    
    extractor = DataExtractor(api_key)
    # print(text)
    # Extract structured data
    structured_data = extractor.extract_structured_data(text)

    return structured_data

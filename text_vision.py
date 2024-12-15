# -*- coding: utf-8 -*-
"""
The function `extract_text_from_pdf` extracts text from a PDF file using the Google Cloud Vision API
and then extracts structured data from the extracted text using a `DataExtractor` class.

:param content: The `content` parameter in the `extract_text_from_pdf` function is the content of
the PDF file that you want to extract text from using the Google Cloud Vision API. This content
should be passed as a byte string. You can read the content of a PDF file and pass it to this
function
:return: The function `extract_text_from_pdf` is returning structured data extracted from a PDF file
using the Google Cloud Vision API and a DataExtractor class.
"""


import os
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.protobuf.json_format import MessageToDict
from docx import Document
from data_extractor import DataExtractor
import io


from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
api_key = os.getenv('GEMINI_API_KEY')

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


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


from PIL import Image
import google.generativeai as genai
import json
import os


class DataExtractor:
    def __init__(self, api_key):
        """
        Initialize the Gemini-powered data extractor
        
        :param api_key: Google Gemini API key
        """
        # Configure the API key
        genai.configure(api_key=api_key)
        
        # Set up the model
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_structured_data(self, input_dict):
        """
        Use Gemini to extract structured data from the input dictionary
        
        :param input_dict: Input dictionary with raw data
        :return: Structured dictionary
        """
        # Prepare the prompt with clear instructions
        prompt = f"""
        Parse the following input data into a structured JSON format with these exact keys:
        {{
            "name": {{
                "first": "",
                "middle": "",
                "last": ""
            }},
            "permanent_address": {{
                "street_address": "",
                "city": "",
                "state": "",
                "zip_code": "",
                "country": ""
            }},
            "current_address": {{
                "street_address": "",
                "city": "",
                "state": "",
                "zip_code": "",
                "country": ""
            }},
            "personal_details": {{
                "DoB": "",
                "age": "",
                "gender": "",
                "passport": "",
                "mobile": "",
                "pan": "",
                "visa": "",
                "email": "",
                "eme_contact_name": "",
                "eme_contact_mobile": ""
            }}
        }}

        Input Data:
        {json.dumps(input_dict)}

        Instructions:
        1. Extract information precisely from the given text
        2. If a specific field cannot be found, leave it as an empty string
        3. Clean up any extra spaces or formatting
        4. Ensure names are properly split into first, middle, and last
        5. Return only the JSON object, no additional text
        """
        
        try:
            # Send the prompt to Gemini
            response = self.model.generate_content(prompt)
            
            # Try to parse the response as JSON
            try:
                # Remove any potential code block markers or extra text
                cleaned_response = response.text.strip('```json').strip('```').strip()
                return json.loads(cleaned_response)
            except json.JSONDecodeError:
                # If JSON parsing fails, print the raw response for debugging
                print("Failed to parse JSON. Raw response:")
                print(response.text)
                return None
        
        except Exception as e:
            print(f"An error occurred during data extraction: {e}")
            return None


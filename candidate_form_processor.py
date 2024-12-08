
import cv2
import pytesseract
from data_extractor import DataExtractor
import os

from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
api_key = os.getenv('GEMINI_API_KEY')


class CandidateFormProcessor:
    def __init__(self, form_image_path):
        self.form_image = cv2.imread(form_image_path)
        self.extracted_data = {}

    def preprocess_image(self):
        # Convert to grayscale
        gray = cv2.cvtColor(self.form_image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return threshold

    def extract_text_regions(self):
        # Define regions for key information extraction
        regions = {
            'name': (0, 700, 2480, 200),
            'permanent_address': (0, 900, 2480, 400),
            'Current_address': (0, 1300, 2480, 400),
            'personal_details': (0, 1700, 2480, 500)
            # 'zip_code': (620, 1210, 700, 100),
            # 'country': (200, 950, 2200, 400)
            # 'dob': (100, 500, 200, 50)
            # 'email': (300, 600, 300, 50)
        }
        
        extracted_info = {}
        for key, (x, y, w, h) in regions.items():
            roi = self.preprocess_image()[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi).strip()
            extracted_info[key] = text
        
        return extracted_info

    def validate_data(self, extracted_data):
        # Basic validation rules
        validations = {
            'name': lambda x: len(x) > 2,
            'email': lambda x: '@' in x,
            'dob': lambda x: len(x) == 10  # Assuming DD/MM/YYYY format
        }
        
        for field, validator in validations.items():
            if not validator(extracted_data.get(field, '')):
                print(f"Warning: Invalid {field}")
        
        return extracted_data

    def export_to_excel(self, data):
        df = pd.DataFrame([data])
        df.to_excel('candidate_data.xlsx', index=False)
        print("Data exported successfully!")

    def process_form(self):
        text_data = self.extract_text_regions()

        # print(text_data)
        # print('----------------')
        # print('----------------')

        # validated_data = self.validate_data(text_data)
        # self.export_to_excel(validated_data)

        extractor = DataExtractor(api_key)
    
        # Extract structured data
        structured_data = extractor.extract_structured_data(text_data)
        
        return structured_data
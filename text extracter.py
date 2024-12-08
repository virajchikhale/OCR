import pandas as pd
import numpy as np
import google.generativeai as genai
import json
import os
from resize import resizer
from candidate_form_processor import CandidateFormProcessor
from delete_files import DeleteFiles



def main():
    api_key = os.getenv('GEMINI_API_KEY')

    # print(api_key)
        
    resizer.resize_image('candidate_form.jpg', 'temp/output_fixed_size.jpg', new_width=2480, new_height=3508)
    processor = CandidateFormProcessor('temp/output_fixed_size.jpg')
    structured_data = processor.process_form()
    # Print the extracted data
    if structured_data:
        print("Extracted Structured Data:")
        print(json.dumps(structured_data, indent=2))
    else:
        print("Failed to extract data.")
    DeleteFiles.delete_all_files_in_folder('temp')
        

if __name__ == '__main__':
    main()
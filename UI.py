import streamlit as st
from PIL import Image
import pandas as pd
import pytesseract  # For text extraction from images
from resize import resizer
from candidate_form_processor import CandidateFormProcessor
from delete_files import DeleteFiles
from DatabaseManager import create_table, insert_candidate, fetch_candidates, search_candidates,delete_candidates


create_table()


# Initialize session state for storing candidate data
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = []

# Title of the app
st.title("Interview Form Data Extractor")

# Sidebar description
# st.sidebar.header("Options")
# st.sidebar.write("Upload interview forms and extract candidate details.")

# File uploader for interview form
uploaded_file = st.file_uploader("Choose an interview form image", type=["jpg", "jpeg", "png"])
delete_candidates()
if uploaded_file:
    # Display the uploaded image
    st.subheader("Uploaded Interview Form")
    image = Image.open(uploaded_file)
    st.image(image, caption="Interview Form", use_column_width=True)

    # api_key = os.getenv('GEMINI_API_KEY')

    # print(api_key)
        
    resizer.resize_image(image, 'temp/output_fixed_size.jpg', new_width=2480, new_height=3508)
    processor = CandidateFormProcessor('temp/output_fixed_size.jpg')
    structured_data = processor.process_form()

    # Extract text using OCR (Tesseract)
    # st.subheader("Extracted Data")
    try:
        st.text_area("Extracted Text", value=structured_data, height=200)

        
        st.subheader("Correct or Add Candidate Details")
        # name = st.text_input("Name")
        # age = st.number_input("Age", min_value=18, max_value=100, step=1)
        # position = st.text_input("Position Applied For")
        # contact = st.text_input("Contact Number")


        first_name = structured_data['name']['first']
        middle_name = structured_data['name']['middle']
        last_name = structured_data['name']['last']
        # perm_address = structured_data['permanent_address']
        perm_street = structured_data['permanent_address']['street_address']
        perm_city = structured_data['permanent_address']['city']
        perm_state = structured_data['permanent_address']['state']
        perm_zip = structured_data['permanent_address']['zip_code']
        perm_country = structured_data['permanent_address']['country']
        # curr_address = structured_data['current_address']
        curr_street = structured_data['current_address']['street_address']
        curr_city = structured_data['current_address']['city']
        curr_state = structured_data['current_address']['state']
        curr_zip = structured_data['current_address']['zip_code']
        curr_country = structured_data['current_address']['country']     
        # perm_country = structured_data['permanent_address']['country']

        # personal = structured_data['personal_details']
        dob = structured_data['personal_details']['DoB']
        age = structured_data['personal_details']['age']
        gender = structured_data['personal_details']['gender']
        passport = structured_data['personal_details']['passport']
        mobile = structured_data['personal_details']['mobile']
        pan = structured_data['personal_details']['pan']
        visa = structured_data['personal_details']['visa']
        email = structured_data['personal_details']['email']
        emergency_name = structured_data['personal_details']['eme_contact_name']
        emergency_mobile = structured_data['personal_details']['eme_contact_mobile']
        
        if st.button("Add Candidate to Database"):
            insert_candidate(first_name or "N/A", middle_name or "N/A", last_name or "N/A", dob or "N/A", age or "N/A", gender or "N/A", email, emergency_name, emergency_mobile)
            st.success("Candidate details added to the database!")
    except Exception as e:
        st.error("Error extracting data from the image. Please try again.",e)

    

# st.subheader("Candidate Details Table")
# df = pd.DataFrame(structured_data)
# st.dataframe(df)

st.subheader("Search Candidates")
search_placeholder = st.empty()
search_keyword = search_placeholder.text_input("Enter a name or position to search", key="search_input")

if search_keyword:
    results = search_candidates(search_keyword)
    if results:
        st.write(f"Search Results for '{search_keyword}':")
        search_df = pd.DataFrame(results, columns=["id","first_name", "middle_name", "last_name", "dob", "age", "gender", "passport_status", "mobile", "pan", "visa_status", "email", "emergency_contact_name", "emergency_contact_mobile"])
        for index, roww in search_df.iterrows():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"**{roww['first_name']} - {roww['last_name']} - {roww['mobile']} - {roww['email']}")
            with col2:
                if st.button(f"More Info", key=f"search_{roww['id']}"):
                    st.info(f"Details for **{roww['mobile']}**:\n\n"
                            f"- **Age:** {roww['email']}\n"
                            f"- **Position:** {roww['gender']}\n"
                            f"- **Contact:** {roww['pan']}")
        # st.dataframe(df)
    else:
        st.write(f"No candidates found for '{search_keyword}'.")

st.subheader("Candidate Details Table")
candidates = fetch_candidates()

if candidates:
    df = pd.DataFrame(candidates, columns=["id","first_name", "middle_name", "last_name", "dob", "age", "gender", "passport_status", "mobile", "pan", "visa_status", "email", "emergency_contact_name", "emergency_contact_mobile"])
    new_df = df[["id","first_name","last_name","mobile","email"]]
    # for index, row in df.iterrows():
    #         col1, col2 = st.columns([3, 2])
    #         with col1:
    #             st.write(f"**{row['first_name']} - {row['last_name']} - {row['mobile']} - {row['email']}")
    #         with col2:
    #             if st.button(f"More Info", key=f"search_{row['id']}"):
    #                 st.info(f"Details for **{row['mobile']}**:\n\n"
    #                         f"- **Age:** {row['email']}\n"
    #                         f"- **Position:** {row['gender']}\n"
    #                         f"- **Contact:** {row['pan']}")
    st.dataframe(new_df)
else:
    st.write("No candidate details found.")

# Footer
st.write("Developed using Streamlit and Tesseract OCR")

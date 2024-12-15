import streamlit as st
from PIL import Image
import pandas as pd
from resize import resizer
from delete_files import DeleteFiles
from DatabaseManager import create_table, insert_candidate, insert_into_education, fetch_candidates, search_candidates, get_candidates, get_education,insert_into_training, insert_into_certifications, insert_into_family, insert_into_reference, get_train,get_certification,get_family,get_reference
from text_vision import extract_text_from_pdf


create_table()

# function to get the details for search section
def show_details(index):
    st.markdown("---")
    result = get_candidates(index)
    edu_result = get_education(index)
    train_result = get_train(index)
    certification_result = get_certification(index)
    family_result = get_family(index)
    reference_result = get_reference(index)

    # print(result)
    personal_df = pd.DataFrame(result, columns=["candidate_id", "first_name", "middle_name", "last_name", "dob", "age", "gender", "passport", "mobile", "pan", "visa_status", "email","current_street", "current_city", "current_state", "current_zip", "current_country","permanent_street", "permanent_city", "permanent_state", "permanent_zip", "permanent_country","emergency_contact_name", "emergency_contact_number", "relocation_availability"])
    new_edu_df = pd.DataFrame(edu_result, columns=["sr_no", "school_university_name", "qualification", "percentage_or_cgpa", "pass_out_year"])
    new_train_df = pd.DataFrame(train_result, columns=["program", "contents", "organized_by", "duration"])
    new_cer_df = pd.DataFrame(certification_result, columns=["sr_no", "certification", "duration"])
    new_fam_df = pd.DataFrame(family_result, columns=["relation", "occupation_profession", "resident_location"])
    new_ref_df =pd.DataFrame(reference_result, columns=["name", "designation", "contact_no"])

    for index, personal in personal_df.iterrows():
        st.header(f"Details for _{personal['first_name']} {personal['middle_name']} {personal['last_name']}_")
        #permanant Address
        st.subheader("Permannet Address:", divider=True)
        st.write(f"Street Address: {personal['permanent_street']}")
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])  # Adjust column widths
        col1.write(f"City: {personal['permanent_city']}")
        col2.write(f"State: {personal['permanent_state']}")
        col3.write(f"Zip Code: {personal['permanent_zip']}")
        col4.write(f"Country: {personal['permanent_country']}")
        # Current Address
        st.subheader("Current Address:", divider=True)
        st.write(f"Street Address: {personal['current_street']}")
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])  # Adjust column widths
        col1.write(f"City: {personal['current_city']}")
        col2.write(f"State: {personal['current_state']}")
        col3.write(f"Zip Code: {personal['current_zip']}")
        col4.write(f"Country: {personal['current_country']}")
        # Personal Details
        st.subheader("Personal Details:", divider=True)
        col1, col2, col3 = st.columns([2, 2, 2])  # Adjust column widths
        col1.write(f"Date or Birth: {personal['dob']}")
        col2.write(f"Age: {personal['age']}")
        col3.write(f"Gender: {personal['gender']}")
        col1.write(f"Passport: {personal['passport']}")
        col2.write(f"Mobile: {personal['mobile']}")
        col3.write(f"PAN No: {personal['pan']}")
        col1, col2 = st.columns([2, 2])  # Adjust column widths
        col1.write(f"Email: {personal['email']}")
        col2.write(f"Visa: {personal['visa_status']}")
        col1.write(f"Emergency Name: {personal['emergency_contact_name']}")
        col2.write(f"Emergency Mobile: {personal['emergency_contact_number']}")

        # Educational Details
        st.subheader("Educational Details:", divider=True)
        st.dataframe(new_edu_df)

        # Training Details
        st.subheader("Training Details:", divider=True)
        st.dataframe(new_train_df)

        # Certification Details
        st.subheader("Certification Details:", divider=True)
        st.dataframe(new_cer_df)
        
        # Family Details
        st.subheader("Family Details:", divider=True)
        st.dataframe(new_fam_df)
        
        # References Details
        st.subheader("References Details:", divider=True)
        st.dataframe(new_ref_df)





    st.markdown("---")

# Initialize session state for storing candidate data
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = []

# Title of the app
st.title("Interview Form Data Extractor")


st.subheader("Search Candidates")
search_placeholder = st.empty()
search_keyword = search_placeholder.text_input("Enter a name or Email to search", key="search_input")


# Search section
if search_keyword:
    results = search_candidates(search_keyword)
    if results:
        st.write(f"Search Results for '{search_keyword}':")
        search_df = pd.DataFrame(results, columns=["candidate_id", "first_name", "middle_name", "last_name", "dob", "age", "gender", "passport", "mobile", "pan", "visa_status", "email",
            "current_street", "current_city", "current_state", "current_zip", "current_country",
            "permanent_street", "permanent_city", "permanent_state", "permanent_zip", "permanent_country",
            "emergency_contact_name", "emergency_contact_number", "relocation_availability"])
        # st.dataframe(search_df)
        for index, row in search_df.iterrows():
            col1, col2, col3, col4 = st.columns([2, 3, 1, 1])  # Adjust column widths
            col1.write(f"<div style='padding: 10px;'>{row['first_name']} {row['middle_name']} {row['last_name']}</div>", unsafe_allow_html=True)
            col2.write(f"<div style='padding: 10px;'>{row['email']}</div>", unsafe_allow_html=True)
            col3.write(f"<div style='padding: 10px;'>{row['mobile']}</div>", unsafe_allow_html=True)
            
            # Add a button in the last column for each row
            if col4.button("Details", key=f"view_{index}"):
                show_details(row['candidate_id'])
    else:
        st.write(f"No candidates found for '{search_keyword}'.")

# File uploader for interview form
uploaded_file = st.file_uploader("Upload a PDF file to add candidate", type="pdf")
    
if uploaded_file is not None:
    # Display the file name
    st.write(f"Uploaded file: {uploaded_file.name}")
    
    # Read and display the content of the PDF file (optional)
    try:
        with st.spinner("Reading the PDF..."):
            pdf_content = uploaded_file.read()
            structured_data = extract_text_from_pdf(pdf_content)
            st.success("PDF file uploaded successfully!")
            st.write(f"File size: {len(pdf_content)} bytes")
            first_name = structured_data['name']['first']
            middle_name = structured_data['name']['middle']
            last_name = structured_data['name']['last']
            st.write(f"PDF Uploaded: {first_name+" "+middle_name+" "+last_name} ")
            # st.text_area("Extracted Text", value=structured_data, height=200)
            print(structured_data)
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

    try:
        
        st.subheader("Correct or Add Candidate Details")

        first_name = structured_data['name']['first']
        middle_name = structured_data['name']['middle']
        last_name = structured_data['name']['last']
        name = first_name+" "+last_name
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
        relocation_availability = True

        education = structured_data['education_details']
        training = structured_data['training_details']
        certifications = structured_data['certifications_details']
        family = structured_data['family_details']
        reference = structured_data['reference_details']

        # adding candidate details to the Database
        if st.button("Add Candidate to Database"):
            Candidates = (first_name or "N/A", middle_name or "N/A", last_name or "N/A", dob or "N/A", age or "N/A", gender or "N/A", passport or "N/A", mobile or "N/A", pan or "N/A", visa or "N/A", email or "N/A", curr_street or "N/A", curr_city or "N/A", curr_state or "N/A", curr_zip or "N/A", curr_country or "N/A", perm_street or "N/A", perm_city or "N/A", perm_state or "N/A", perm_zip or "N/A", perm_country or "N/A", emergency_name or "N/A", emergency_mobile or "N/A", relocation_availability or "N/A")
            # print(Candidates)
            insert_candidate(Candidates)       
            # adding candidate educational details to the Database
            for i in range(0,len(education)):
                sr_no = i+1
                school_university_name = education[str(i+1)]['school_university_name']
                qualification = education[str(i+1)]['qualification']
                percentage_or_cgpa = education[str(i+1)]['percentage_or_cgpa']
                pass_out_year = education[str(i+1)]['pass_out_year']
                education_detail = (sr_no or "N/A", school_university_name or "N/A", qualification or "N/A", percentage_or_cgpa or "N/A", pass_out_year or "N/A")
                insert_into_education(education_detail)

            
            # adding candidate training details to the Database
            for i in range(0,len(training)):
                program = training[str(i+1)]['program']
                contents = training[str(i+1)]['contents']
                organized_by = training[str(i+1)]['organized_by']
                duration = training[str(i+1)]['duration']
                training_detail = (program or "N/A", contents or "N/A", organized_by or "N/A", duration or "N/A")
                insert_into_training(training_detail)

            
            # adding candidate certifications details to the Database
            for i in range(0,len(certifications)):
                sr_no = i+1
                certification = certifications[str(i+1)]['certification']
                duration = certifications[str(i+1)]['duration']
                certifications_detail = (sr_no or "N/A", certification or "N/A", duration or "N/A")
                insert_into_certifications(certifications_detail)  
            
            # adding candidate Family details to the Database   
            for i in range(0,len(family)):
                relation = family[str(i+1)]['relation']
                occupation_profession = family[str(i+1)]['occupation_profession']
                resident_loction = family[str(i+1)]['resident_loction']
                family_detail = (relation or "N/A", occupation_profession or "N/A", resident_loction or "N/A")
                insert_into_family(family_detail) 
            
            # adding candidate reference details to the Database   
            for i in range(0,len(reference)):
                name = reference[str(i+1)]['name']
                designation = reference[str(i+1)]['designation']
                contact_no = reference[str(i+1)]['contact_no']
                reference_detail = (name or "N/A", designation or "N/A", contact_no or "N/A")
                insert_into_reference(reference_detail)   
  

            # st.success("Candidate details added to the database!")
    except Exception as e:
        st.error("Error extracting data from the image. Please try again.",e)



# Details of all the candidates form reference table
st.subheader("Candidate Details Table")
candidates = fetch_candidates()

if candidates:
    df = pd.DataFrame(candidates, columns=["candidate_id", "first_name", "middle_name", "last_name", "dob", "age", "gender", "passport", "mobile", "pan", "visa_status", "email",
            "current_street", "current_city", "current_state", "current_zip", "current_country",
            "permanent_street", "permanent_city", "permanent_state", "permanent_zip", "permanent_country",
            "emergency_contact_name", "emergency_contact_number", "relocation_availability"])
    new_df = df[["candidate_id","first_name", "last_name", "mobile", "email"]]
    st.dataframe(new_df)
else:
    st.write("No candidate details found.")

# Footer
st.write("Developed using Streamlit, Gemini API and Google Vision API")

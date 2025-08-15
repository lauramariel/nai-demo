import streamlit as st
from components.api_endpoint import create_api_endpoint_uploader
from components.image_uploader import upload_image
from components.prompt_editor import edit_prompt
from utils.api_handler import analyze_image
from utils.image_processor import preprocess_image
from urllib.parse import urlparse
from utils.text_effects import typing_effect
from decouple import config

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def main():
    # Configure page with custom styling
    st.set_page_config(layout="wide", page_title="Healthcare Document Assistant", page_icon="🏥", menu_items=None)
    
    # Add custom CSS for styling
    st.markdown("""
        <style>
        /* General page styling */
        .stApp {
            background-color: #f0f4f8;
            color: #2c3e50;
        }

        /* Hide unnecessary tabs */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        /* Title styling */
        .main-title {
            font-size: 3.2rem !important;
            font-weight: 700 !important;
            color: #7cc0ff !important;
            margin-bottom: 0.5rem !important;
            text-align: center !important;
        }

        /* Configuration section styling */
        .config-section {
            background-color: #ffffff;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }

        /* Results section styling */
        .results-section {
            background-color: #ffffff;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            height: 100%;
        }
        
        /* File uploader styling */
        .stFileUploader {
            background-color: #f8f9fa !important;
            border: 2px dashed #7cc0ff !important;
            border-radius: 8px !important;
            padding: 10px !important;
        }
        
        .stFileUploader button {
            background-color: #e6f3ff !important;
            color: #2c3e50 !important;
            font-weight: bold !important;
        }

        /* Button styling */
        .stButton > button {
            width: 100%;
            background-color: #7cc0ff;
            color: #2c3e50;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #a8d5ff;
        }

        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #f8f9fa;
            color: #2c3e50;
            border: 1px solid #7cc0ff;
            border-radius: 5px;
            padding: 10px;
            caret-color: #0078d7;
        }

        /* Text area styling */
        .stTextArea textarea {
            background-color: #f8f9fa;
            color: #2c3e50;
            border: 1px solid #7cc0ff;
            caret-color: #0078d7;
        }

        /* Subheader styling */
        .stMarkdown h2, .stMarkdown h3 {
            color: #7cc0ff;
        }
        
        p, li {
            color: #34495e;
            line-height: 1.6;
        }
        
        /* Healthcare specific styling */
        .healthcare-header {
            color: #7cc0ff;
            font-weight: bold;
        }
        
        .key-info {
            background-color: #f1f8fe;
            padding: 15px;
            border-left: 4px solid #7cc0ff;
            margin: 10px 0;
            color: #2c3e50;
        }
        
        /* Analysis results styling */
        .analysis-results {
            background-color: #f8fcff;
            border-radius: 12px;
            margin: 15px 0;
            color: #2c3e50;
            box-shadow: 0 0 20px rgba(124, 192, 255, 0.15);
            line-height: 1.7;
            font-size: 1.05em;
        }
        
        /* Summary section styling */
        .analysis-results p:first-of-type {
            background-color: #e6f3ff;
            padding: 15px;
            border-radius: 8px;
            font-weight: 500;
            margin-bottom: 20px;
            border-left: 4px solid #7cc0ff;
        }
        
        /* Warning for illegible text */
        .text-extraction-warning {
            background-color: #fff4e5;
            color: #8a5700;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 600;
            border-left: 4px solid #f5a623;
        }
        
        .analysis-results h1, .analysis-results h2, .analysis-results h3 {
            color: #7cc0ff;
            margin-top: 18px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        .analysis-results ul, .analysis-results ol {
            margin-left: 25px;
            margin-bottom: 18px;
            padding-right: 10px;
        }
        
        .analysis-results li {
            margin-bottom: 8px;
        }
        
        .analysis-results p {
            margin-bottom: 15px;
        }
        
        .analysis-results strong, .analysis-results b {
            color: #4a6fa5;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>Healthcare Document Analysis Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; margin-bottom: 30px;'>Extract and analyze key information from medical documents, handwritten notes, and healthcare forms</p>", unsafe_allow_html=True)

    # Create two columns for layout with space between them
    col1, spacer, col2 = st.columns([0.95, 0.1, 0.95])

    with col1:
        # Start of configuration section
        with st.container():
            st.markdown('<div class="config-section">', unsafe_allow_html=True)
            st.markdown("<h3>API Configuration</h3>", unsafe_allow_html=True)
            base_url = "https://nai.tmelab.net/api/v1/chat/completions"
            api_url = st.text_input(
                "API Endpoint URL", 
                value=config('API_ENDPOINT', default='https://nai.tmelab.net/api/v1'),
                placeholder="Enter the API endpoint URL"
            )
            
            if api_url and not is_valid_url(api_url):
                st.error("Please enter a valid URL")
            
            model_name = st.text_input(
                "Endpoint Name", 
                placeholder="Enter the endpoint name",
                value="llama-vision"
            )

            api_key = st.text_input('API Key', type='password', value=config('API_KEY', default=''))

            # Document Upload Section
            st.markdown("<h3>Document Upload</h3>", unsafe_allow_html=True)
            st.markdown("<p>Upload medical documents, prescriptions, handwritten notes, or healthcare forms (JPG, PNG, PDF)</p>", unsafe_allow_html=True)
            
            # Add some space before the uploader
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            uploaded_image = upload_image()

            # Prompt Section
            # st.markdown("<h3>Prompt Configuration</h3>", unsafe_allow_html=True)
            
            # Default healthcare system prompt
            default_prompt = """

You are a medical AI assistant specialized in extracting critical information from healthcare documents. Your primary responsibility is PATIENT SAFETY through accurate information extraction.

## Instructions:
Analyze the provided healthcare document and extract ONLY information that is explicitly written and clearly visible. Do not interpret, estimate, round, or fill in any missing information. Present information exactly as it appears in the document using bullet points and precise formatting.

## Required Information Categories:

### 1. PATIENT DEMOGRAPHICS
- Full name, age, sex, date of birth
- Contact information (phone, address, email)
- Insurance information (carrier, member ID, group number)
- Medical record number if available

### 2. CLINICAL PRESENTATION
- **Chief complaint** (exact wording from document)
- **History of present illness** (detailed symptom description)
- **Symptom characteristics** (duration, frequency, triggers, quality)
- **Associated symptoms** and alleviating/aggravating factors
- **Review of systems** findings

### 3. VITAL SIGNS & MEASUREMENTS
- All vital signs with exact values and dates taken
- BMI and other measurements
- Oxygen saturation if documented

### 4. CURRENT MEDICATIONS & ALLERGIES
- **All current medications** (exact names, doses, frequencies)
- **All allergies** with specific reactions documented
- **Recent medication changes** or new prescriptions

### 5. MEDICAL HISTORY
- **Past medical history** (conditions with diagnosis years when available)
- **Surgical history** (procedures and years)
- **Family history** (specific conditions and relationships)
- **Social history** (smoking, alcohol, occupation, exercise habits)

### 6. DIAGNOSTIC RESULTS
- **Laboratory values** (exact values with units and dates)
- **Imaging results** (specific findings, not interpretations)
- **EKG findings** (exact technical findings)
- **Other diagnostic tests** with dates and results

### 7. CLINICAL ASSESSMENT & reasoning
- **Primary assessment/diagnosis** (exact wording from provider)
- **Secondary conditions** being managed
- **Risk factors** identified by provider
- **Clinical reasoning** for referral or treatment decisions
- **Differential diagnoses** if mentioned

### 8. URGENCY & CLINICAL DECISION-MAKING
- **Urgency level** with specific justification from document
- **Clinical reasoning** for urgency determination
- **Risk stratification** comments from provider
- **Specific questions** for consultant/specialist
- **Treatment already initiated** 

### 9. REFERRAL & FOLLOW-UP DETAILS
- **Specific referrals** requested (specialty, preferred provider)
- **Patient availability** and scheduling preferences
- **Activity restrictions** or precautions ordered
- **Follow-up requirements** and monitoring needs

### 10. ADDITIONAL CLINICAL NOTES
- **Provider observations** about patient status
- **Patient concerns** and anxiety levels
- **Compliance issues** or patient education needs
- **Copies sent to** (documentation trail)
- **Any additional clinical context** affecting care

## Output Format:
Structure your response using the exact headings above. Under each heading, use bullet points with concise, clinically relevant information. Avoid unnecessary narrative - focus on facts that impact clinical decision-making.

**Example formatting based on your sample:**
### PATIENT DEMOGRAPHICS
- Name: James Robert Thompson, Age: 59, Sex: Male
- DOB: 11/22/1965, MRN: WFM-789456
- Address: 856 Maple Ridge Lane, Raleigh, NC 27612
- Phone: (919) 555-0156, Email: j.thompson@email.com
- Insurance: Aetna PPO - Member ID: AET987654321, Group #: 7429-EMP

### CLINICAL PRESENTATION
- Chief complaint: "Intermittent chest pain for 6 weeks, worsening with exertion"
- History: 59-year-old male with 6-week history of substernal chest pressure, "squeezing" sensation lasting 5-10 minutes
- Triggers: Climbing stairs or brisk walking
- Associated symptoms: Mild shortness of breath, some improvement with sitting down
- Frequency: Episodes occurring 3-4 times per week

### VITAL SIGNS & MEASUREMENTS
- BP: 148/92 mmHg, HR: 78 bpm regular, Temp: 98.4°F
- Resp: 16/min, O2 Sat: 97% on room air, BMI: 32.1
- Date: Latest visit 06/12/2025

### CLINICAL ASSESSMENT & REASONING
- Assessment: "Chest pain, likely anginal equivalent - rule out CAD"
- Secondary: "Hypertension, suboptimally controlled; Type 2 DM with suboptimal glucose control; Dyslipidemia; Obesity"
- Risk factors: Multiple cardiac risk factors (diabetes, hypertension, dyslipidemia, family history, former smoking)

### URGENCY & CLINICAL DECISION-MAKING
- Urgency level: Routine (checked on form)
- Clinical reasoning: "Patient has multiple cardiac risk factors with new-onset exertional chest pain and EKG abnormalities. While troponin negative, symptoms are concerning for unstable angina or early CAD requiring prompt evaluation"
- Specific questions for consultant: "Cardiac stress testing vs. cardiac catheterization? Optimization of cardiac medications? Risk stratification for surgical procedures?"

### ADDITIONAL CLINICAL NOTES
- Provider observations: "Patient very anxious about cardiac symptoms since father's early MI. Has been avoiding physical activity due to fear of triggering symptoms"
- Family input: "Wife reports he seems more fatigued lately"
- Patient compliance: "Patient understands need for specialist evaluation and is compliant with medications"
- Activity restrictions: "Advised activity restriction pending cardiac clearance"

**Counter-examples of what NOT to do:**
-  "Blood pressure approximately 150/90" (when document shows 148/92)
-  "Patient is about 60 years old" (when document shows age 59)
-  "Cholesterol around 200" (when document shows 198 mg/dL)
-  Adding information not in the document
-  "Unable to read" should be "Unable to read from document"

## CRITICAL SAFETY REQUIREMENTS:
**MEDICAL ACCURACY IS PARAMOUNT - INCORRECT INFORMATION CAN CAUSE PATIENT HARM**

### Mandatory Rules:
1. **NEVER invent, estimate, or guess information** - Only extract what is explicitly written
2. **NEVER round numbers** - Copy all numerical values exactly as shown (e.g., if document shows "148/92 mmHg", write exactly "148/92 mmHg", not "150/90")
3. **NEVER approximate dates** - Use exact dates as written or state "Date not specified"
4. **NEVER interpret abbreviations** unless certain - Write exactly as shown
5. **NEVER fill in missing information** - If information is unclear or missing, write "Not specified" or "Unable to read"
6. **NEVER assume medication dosages** - Copy exact text including units (mg, mL, etc.)
7. **NEVER paraphrase medical conditions** - Use exact terminology from document

## Key Guidelines:
- **Extract only explicitly documented information**
- **Copy numerical values exactly as written**
- **Include specific dates exactly as shown**
- **Use exact medical terminology from document**
- **State when information is missing rather than guessing**
- **Preserve original formatting of critical values**

## Quality Checks:
Before finalizing your extraction, ensure you have:
- Verified all numbers match the source exactly
- Confirmed no information was invented or assumed
- Checked that unclear items are marked as such
- Ensured all medical values retain original precision
- Confirmed dates and times are exact copies

Now analyze the provided healthcare document and extract the information according to these guidelines."""
            
            # prompt = edit_prompt()
            
            # If prompt is empty, use the default healthcare prompt
            # if not prompt:
            
            prompt = default_prompt

            # Add space before button
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            # Submit Button
            submit_button = st.button("Analyze Document", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown("<h3>Analysis Results</h3>", unsafe_allow_html=True)
        st.markdown("<p>Key medical information extracted from your document will appear here</p>", unsafe_allow_html=True)
                
        # Process and display results
        if submit_button and api_url and model_name and api_key and uploaded_image and prompt:
            # Process both PDFs and images equally
            
            with st.spinner('Processing document...'):
                processed_file = preprocess_image(uploaded_image)
                
                if processed_file is None:
                    st.error("Failed to process the document. Please try uploading again.")
                    return

                api_endpoint = {
                    "url": api_url,
                    "model_name": model_name,
                    "api_key": api_key
                }

                result = analyze_image(api_endpoint, processed_file, prompt)

                if "error" in result:
                    st.error(result["error"])
                else:
                    try:
                        content = result["choices"][0]["message"]["content"]
                        
                        # Check for extraction warning indicators
                        formatted_content = content
                        if "PARTIAL TEXT EXTRACTION" in content:
                            formatted_content = content.replace("PARTIAL TEXT EXTRACTION", 
                                "<div class='text-extraction-warning'>PARTIAL TEXT EXTRACTION: Some text could not be fully extracted</div>")
                        elif "TEXT EXTRACTION NOT POSSIBLE" in content:
                            formatted_content = content.replace("TEXT EXTRACTION NOT POSSIBLE", 
                                "<div class='text-extraction-warning'>TEXT EXTRACTION NOT POSSIBLE: The handwritten text could not be reliably extracted</div>")
                        
                        with st.container():
                            st.markdown("<div class='analysis-results'>", unsafe_allow_html=True)
                            typing_effect(formatted_content)
                            st.markdown("</div>", unsafe_allow_html=True)
                    except (KeyError, IndexError) as e:
                        st.error("Unexpected API response format")

        elif submit_button:
            st.warning("Please fill in all fields before submitting.")
            
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

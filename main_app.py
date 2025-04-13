import streamlit as st
import base64
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Optional
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

# Load environment variables first
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="ID Magic: Automated ID Card Data Extraction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better card styling
st.markdown("""
    <style>
    .card {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    }
    .card h3 {
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize LangChain/OpenAI LLMs with proper error handling
try:
    llm_image = ChatOpenAI(model="gpt-4o-mini", max_tokens=1024)
    llm2 = ChatOpenAI(model="gpt-4o-mini")
except Exception as e:
    st.error(f"Failed to initialize AI models: {str(e)}")
    st.stop()

class IDCardData(BaseModel):
    """Structured output schema for the ID card data"""
    name: str = Field(description="Full name of the person")
    age: Optional[int] = Field(description="Age of the person", default=None)
    id_type: str = Field(
        description="Type of ID (passport, Aadhaar, driving license, pancard, voterid, company id, school id, other)"
    )
    id_number: Optional[str] = Field(description="ID number of the person", default=None)
    address: Optional[str] = Field(description="Complete address of the person", default=None)
    phone_number: Optional[str] = Field(description="Contact phone number", default=None)
    email: Optional[str] = Field(description="Email address", default=None)
    date_of_birth: Optional[str] = Field(description="Date of birth in DD/MM/YYYY format", default=None)

# Initialize structured output parser
llm_with_structured_output = llm2.with_structured_output(IDCardData)

# Sidebar information
with st.sidebar:
    st.title("About ID Magic")
    st.info(
        "ID Magic uses advanced AI to automatically extract and structure data from your ID cards. "
        "Simply upload your image, and let the magic reveal the hidden details."
    )
    st.markdown("### Supported ID Types")
    st.markdown("""
        - Passport
        - Aadhaar Card
        - Driving License
        - PAN Card
        - Voter ID
        - Company ID
        - School ID
    """)

# Main content
st.title("ID Magic: Automated ID Card Data Extraction")
st.markdown("**Unlock the information hidden in your IDs—instantly!**")

def load_image_as_base64(file) -> str:
    """Convert uploaded image to base64 string"""
    try:
        return base64.b64encode(file.read()).decode("utf-8")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def display_card(title: str, content: any) -> None:
    """Display information in a styled card"""
    if content is not None and content != "":
        card_html = f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# Image upload section
uploaded_file = st.file_uploader(
    "Upload your ID card image",
    type=["png", "jpg", "jpeg"],
    help="Supported formats: PNG, JPG, JPEG"
)

if uploaded_file:
    try:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded ID Card", use_column_width=True)
        
        # Process button
        if st.button("Process ID Card", type="primary"):
            # Convert image to base64
            image_base64 = load_image_as_base64(uploaded_file)
            if not image_base64:
                st.stop()
                
            # Prepare message for OCR extraction
            image_message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": "Extract all text and relevant information from this ID card image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    },
                ]
            )

            # Extract text from image
            with st.spinner("Extracting text from image..."):
                try:
                    response = llm_image.invoke([image_message])
                    extracted_text = StrOutputParser().invoke(response.content)
                    
                    # Show extracted text in expandable section
                    with st.expander("View Extracted Text"):
                        st.text_area("Raw OCR Result", value=extracted_text, height=200)
                except Exception as e:
                    st.error(f"Text extraction failed: {str(e)}")
                    st.stop()

            # Process extracted text for structured data
            with st.spinner("Analyzing and structuring data..."):
                try:
                    structured_data = llm_with_structured_output.invoke(extracted_text)
                except Exception as e:
                    st.error(f"Data structuring failed: {str(e)}")
                    st.stop()

            # Display structured output
            st.subheader("📄🧑🏿‍🦽‍➡️ Extracted Information")
            col1, col2 = st.columns(2)

            with col1:
                display_card("Name", structured_data.name)
                display_card("Age", structured_data.age)
                display_card("ID Type", structured_data.id_type)
                display_card("ID Number", structured_data.id_number)

            with col2:
                display_card("Address", structured_data.address)
                display_card("Phone Number", structured_data.phone_number)
                display_card("Email", structured_data.email)
                display_card("Date of Birth", structured_data.date_of_birth)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

else:
    st.info("👆 Upload an ID card image to begin the extraction process")

# Footer
st.markdown("---")
st.markdown(
    "*Note: All processing is done securely. No data is stored or retained after processing.*",
    help="Your privacy is our priority"
)

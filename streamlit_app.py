import streamlit as st
import base64
from pathlib import Path
from PIL import Image
import io
from Main_OCR import OcrChain
import time

# Set page configuration
st.set_page_config(
    page_title="Miny-Gemini-OCR",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .col_01{
        border: 1px dashed #4a90e2;
        border-radius: 10px;    
    }  
    .col_02{
        border: 1px dashed #4a90e2;
        border-radius: 10px;   
        margin-bottom : 1rem;    
             
    }                
    .upload-text {
        text-align: center;
        padding: 2rem;
        border: 2px dashed #4a90e2;
        border-radius: 10px;
        margin-bottom:1rem    
    }
    .results-area {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    model = st.selectbox(
        "Select Model",
        ["gemma3:4b-it-q4_K_M"],
        index=0,
        help="Choose the model for OCR processing"
    )
    
    base_url = st.text_input(
        "Ollama Server URL",
        value="http://localhost:11434",
        help="Enter the Ollama server URL"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Adjust the model's temperature (higher = more creative)"
    )
    
    st.divider()
    
    # About section in sidebar
    st.markdown("### About")
    st.markdown("""
        This app uses Gemini Vision model for OCR tasks.
        Upload an image and get the extracted text in seconds!
    """)

# Main content
st.title("🔍 Miny-Gemini-OCR")
st.markdown("#### Transform Images to Text with AI")

# Create two columns for the main content
col1, col2 = st.columns([1, 1],border=True)

with col1:
    # # with
    # st.markdown("### Upload Image")
    st.markdown("""
            <div class="col_01" align="center">
                <h3>📸 Upload the image</h3>
            </div>
         """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Supported formats: PNG, JPG, JPEG"
    )
    
    # Display upload area
    if not uploaded_file:
        st.markdown("""
            <div class="upload-text">
                <h3>📸 Drop your image here</h3>
                <p>or click to browse</p>
            </div>
        """, unsafe_allow_html=True)

with col2:
    # st.markdown("### ")
    st.markdown("""
            <div class="col_02" align="center">
                <h3>Results</h3>
            </div>
         """, unsafe_allow_html=True)
    # st.markdown("""
    #         <div class="upload-text" algin="center">
    #             <p> Results will show here.</p>
    #         </div>
    #     """, unsafe_allow_html=True)

# Preview and Process
if uploaded_file:
    with col1:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Process button
        process = st.button("🔍 Extract Text", type="primary")
    
    with col2:
        # st.markdown("### Results")
        
        if process:
            try:
                # Show processing status
                with st.spinner("Processing image..."):
                    # Save the uploaded file temporarily
                    temp_path = Path("temp_image.png")
                    image.save(temp_path)
                    
                    # Create OCR chain and process
                    ocr_chain = OcrChain(
                        model=model,
                        base_url=base_url,
                        temperature=temperature
                    )
                    
                    # Process the image
                    result = ocr_chain.invoke(str(temp_path))
                    
                    # Delete temporary file
                    temp_path.unlink()
                    
                    # Display results in a nice format
                    st.markdown('<div class="results-area">', unsafe_allow_html=True)
                    st.markdown("#### Extracted Text:")
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add download button for results
                    st.download_button(
                        label="📥 Download Results",
                        data=result,
                        file_name="ocr_results.txt",
                        mime="text/plain",
                        use_container_width= True, 
                        type="primary"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.markdown("""
                    Please make sure:
                    - Ollama server is running
                    - The model is properly loaded
                    - The image is clear and readable
                """)
        else:
            st.info("Click 'Extract Text' to process the image")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit and Gemini Vision model",
    help="GitHub: MalakaSupun/Miny-Gemini-OCR"
)


import streamlit as st
import requests
import json
import time
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="🦐 Shrimp Farm Detection",
    page_icon="🦐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .upload-section {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    .result-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .download-button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "https://028f-34-80-68-219.ngrok-free.app"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🦐 Shrimp Farm Detection System</h1>
        <p>Upload aerial images to detect and analyze shrimp farms</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("📊 System Info")

        # Check API health
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("🟢 API Connected")
            else:
                st.error("🔴 API Error")
        except:
            st.error("🔴 API Disconnected")

        st.markdown("---")
        st.markdown("""
        ### 📋 Instructions:
        1. Upload an aerial image
        2. Click 'Detect Shrimp Farms'
        3. View results and download files

        ### 📁 Output Files:
        - Original Image
        - Detection Overlay
        - JSON Coordinates
        - GeoJSON File
        - Shapefile
        """)

    # Main content - Input section
    st.markdown("### 📤 Upload Image")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an aerial image...",
        type=['png', 'jpg', 'jpeg', 'tiff', 'tif'],
        help="Upload aerial images in PNG, JPG, JPEG, TIFF formats"
    )

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Image info
        st.info(f"📏 Image Size: {image.size[0]} x {image.size[1]} pixels")

        # Predict button
        if st.button("🔍 Detect Shrimp Farms", type="primary", use_container_width=True):
            with st.spinner("🔄 Processing image... This may take a few minutes."):
                try:
                    # Prepare file for API
                    files = {"image": uploaded_file.getvalue()}

                    # Make API request
                    response = requests.post(
                        f"{API_BASE_URL}/predict",
                        files={"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    )

                    if response.status_code == 200:
                        results = response.json()
                        st.session_state.results = results
                        st.success("✅ Detection completed successfully!")
                    else:
                        st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")

                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")

    # Results section - displayed below input
    st.markdown("### 📊 Results")

    if 'results' in st.session_state and st.session_state.results.get('success'):
        results = st.session_state.results['results']

        # Display polygon count
        st.metric(
            label="🦐 Detected Shrimp Farms",
            value=results['polygon_count']
        )

        # Display result images
        tab1, tab2 = st.tabs(["🖼️ Original", "🎯 Detection"])

        with tab1:
            try:
                # Method 1: If API returns base64 encoded image
                if 'original_image_base64' in results:
                    import base64
                    from io import BytesIO
                    image_data = base64.b64decode(results['original_image_base64'])
                    image = Image.open(BytesIO(image_data))
                    st.image(image, caption="Original Image", use_container_width=True)

                # Method 2: If API provides download URL
                elif 'original_image_url' in results:
                    st.image(results['original_image_url'], caption="Original Image", use_container_width=True)

                # Method 3: Construct URL from filename (most common case)
                elif 'original_image' in results:
                    file_name = os.path.basename(results['original_image'])
                    image_url = f"{API_BASE_URL}/download/{file_name}"
                    try:
                        # Try to fetch and display the image
                        img_response = requests.get(image_url, timeout=10)
                        if img_response.status_code == 200:
                            from io import BytesIO
                            image = Image.open(BytesIO(img_response.content))
                            st.image(image, caption="Original Image", use_container_width=True)
                        else:
                            st.error(f"Could not load image from: {image_url}")
                            st.markdown(f"[⬇️ Download Original Image]({image_url})")
                    except Exception as img_error:
                        st.error(f"Error fetching image: {str(img_error)}")
                        st.markdown(f"[⬇️ Download Original Image]({image_url})")

                else:
                    st.info("Original image not available")

            except Exception as e:
                st.error(f"Error loading original image: {str(e)}")
                st.info("Original image preview not available")

        with tab2:
            try:
                # Method 1: If API returns base64 encoded image
                if 'detected_image_base64' in results:
                    import base64
                    from io import BytesIO
                    image_data = base64.b64decode(results['detected_image_base64'])
                    image = Image.open(BytesIO(image_data))
                    st.image(image, caption="Detection Results", use_container_width=True)

                # Method 2: If API provides download URL
                elif 'detected_image_url' in results:
                    st.image(results['detected_image_url'], caption="Detection Results", use_container_width=True)

                # Method 3: Construct URL from filename
                elif 'detected_image' in results:
                    file_name = os.path.basename(results['detected_image'])
                    image_url = f"{API_BASE_URL}/download/{file_name}"
                    try:
                        # Try to fetch and display the image
                        img_response = requests.get(image_url, timeout=10)
                        if img_response.status_code == 200:
                            from io import BytesIO
                            image = Image.open(BytesIO(img_response.content))
                            st.image(image, caption="Detection Results", use_container_width=True)
                        else:
                            st.error(f"Could not load image from: {image_url}")
                            st.markdown(f"[⬇️ Download Detection Image]({image_url})")
                    except Exception as img_error:
                        st.error(f"Error fetching image: {str(img_error)}")
                        st.markdown(f"[⬇️ Download Detection Image]({image_url})")

                else:
                    st.info("Detection image not available")

            except Exception as e:
                st.error(f"Error loading detection image: {str(e)}")
                st.info("Detection image preview not available")

        # Download section
        st.markdown("### 📥 Download Files")

        download_col1, download_col2 = st.columns(2)

        with download_col1:
            if st.button("📄 Download JSON", use_container_width=True):
                file_name = os.path.basename(results['json_file'])
                st.markdown(f"[⬇️ Download JSON]({API_BASE_URL}/download/{file_name})")

            if st.button("🗺️ Download GeoJSON", use_container_width=True):
                file_name = os.path.basename(results['geojson_file'])
                st.markdown(f"[⬇️ Download GeoJSON]({API_BASE_URL}/download/{file_name})")

        with download_col2:
            if results['shapefile'] and st.button("📊 Download Shapefile", use_container_width=True):
                file_name = os.path.basename(results['shapefile'])

                st.info("Shapefile components (.shp, .shx, .dbf, etc.) are included in the ZIP file.")


            if st.button("📦 Download All (ZIP)", use_container_width=True):
                file_name = os.path.basename(results['zip_file'])
                st.markdown(f"[⬇️ Download ZIP]({API_BASE_URL}/download/{file_name})")
    else:
        st.info("👆 Upload an image and click 'Detect Shrimp Farms' to see results here.")

if __name__ == "__main__":
    main()

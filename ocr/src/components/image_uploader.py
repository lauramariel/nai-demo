def upload_image():
    import streamlit as st
    from PIL import Image

    st.header("Upload Image for OCR")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # To read file as bytes:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_container_width=True)
        st.write("")
        st.success("Image uploaded successfully!")

        return uploaded_file
    return None

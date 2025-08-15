def upload_image():
    import streamlit as st
    from PIL import Image
    import io
    import fitz  # PyMuPDF

    uploaded_file = st.file_uploader("Choose an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file is not None:
        # To read file as bytes:
        if uploaded_file.type.startswith('image'):
            image = Image.open(uploaded_file)
            # Calculate max width and height to fit on screen
            max_width = 400
            # Maintain aspect ratio
            width, height = image.size
            aspect_ratio = width / height
            new_height = int(max_width / aspect_ratio)
            
            # Display image with controlled size
            st.image(image, caption='Uploaded Image', width=max_width)
            st.success("Image uploaded successfully!")
        elif uploaded_file.type == "application/pdf":
            try:
                # Get PDF bytes
                pdf_bytes = uploaded_file.getvalue()
                
                # Open the PDF with PyMuPDF
                pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                # Get the first page
                first_page = pdf_document[0]
                
                # Render page to an image (PNG)
                pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                
                # Display the first page as preview
                st.image(Image.open(io.BytesIO(img_bytes)), caption=f"PDF Preview: {uploaded_file.name}", width=400)
                st.success(f"PDF uploaded: {uploaded_file.name} ({pdf_document.page_count} pages)")
                
                # Close the document
                pdf_document.close()
            except Exception as e:
                st.error(f"Error previewing PDF: {str(e)}")
                st.success(f"PDF uploaded: {uploaded_file.name}")

        return uploaded_file
    return None

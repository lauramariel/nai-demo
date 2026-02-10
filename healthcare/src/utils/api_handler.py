def analyze_image(api_endpoint, file_bytes, prompt):
    """
    Send document analysis request to the API endpoint for processing.
    Args:
        api_endpoint (dict): Contains url, model_name, and api_key
        file_bytes (bytes): File data in bytes (image or PDF)
        prompt (str): Prompt for the document analysis
    Returns:
        dict: JSON response from the API
    """
    import requests
    import base64
    import json
    import io
    import fitz  # PyMuPDF

    # Ensure URL ends with /chat/completions
    url = api_endpoint['url']
    if not url.endswith('/chat/completions'):
        url = url.rstrip('/') + '/chat/completions'

    # Prepare headers with authentication
    headers = {
        'Authorization': f'Bearer {api_endpoint["api_key"]}',
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        # Check if it's a PDF file
        is_pdf = False
        if file_bytes[:4] == b'%PDF':
            is_pdf = True
        
        # For PDFs, convert first page to image
        if is_pdf:
            try:
                # Open the PDF with PyMuPDF
                pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
                
                # Get the first page
                first_page = pdf_document[0]
                
                # Render page to an image with higher resolution
                pix = first_page.get_pixmap(matrix=fitz.Matrix(3, 3))
                img_data = pix.tobytes("jpeg")
                
                # Use the converted image instead of PDF
                file_b64 = base64.b64encode(img_data).decode()
                
                # Close the document
                pdf_document.close()
            except Exception as e:
                return {"error": f"PDF conversion failed: {str(e)}"}
        else:
            # For images, just use as is
            file_b64 = base64.b64encode(file_bytes).decode()
        
        # Always use image/jpeg content type for API compatibility
        content_type = "image/jpeg"
        
        # Create message payload with structured content
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{content_type};base64,{file_b64}"
                        }
                    }
                ]
            }
        ]

        # Prepare payload
        payload = {
            "model": api_endpoint["model_name"],
            "messages": messages,
            "max_tokens": 1024,
            "stream": False,
            "temperature": 0.1
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse API response: {str(e)}"}

    except Exception as e:
        return {"error": f"Image processing failed: {str(e)}"}
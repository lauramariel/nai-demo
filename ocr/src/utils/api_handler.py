def analyze_image(api_endpoint, image, prompt):
    """
    Send image analysis request to the API endpoint for OCR processing.
    Args:
        api_endpoint (dict): Contains url, model_name, and api_key
        image (bytes): Image data in bytes
        prompt (str): Prompt for the OCR analysis
    Returns:
        dict: JSON response from the API
    """
    import requests
    import base64
    import json
    import filetype

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
        # Convert image to base64 and create content
        image_b64 = base64.b64encode(image).decode()

        # Detect image type
        kind = filetype.guess(image)
        if kind is None:
            mime_type = 'application/octet-stream'  # fallback
        else:
            mime_type = kind.mime

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
                        "image_url": {"url": f"data:{mime_type};base64,{image_b64}"}
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
            "temperature": 0.3
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
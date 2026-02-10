# Optical Character Recognition Streamlit Application

This project is a simple Streamlit application that allows users to test Optical Character Recognition (OCR) using an API endpoint. The application provides features for uploading an API endpoint, uploading an image, editing a prompt, and analyzing the image based on the prompt.

## Project Structure

```
ocr-streamlit-app
├── src
│   ├── main.py                # Entry point of the Streamlit application
│   ├── components              # Contains UI components for the application
│   │   ├── __init__.py        # Initializes the components package
│   │   ├── api_endpoint.py     # Handles API endpoint upload and submission
│   │   ├── image_uploader.py   # Manages image uploads
│   │   └── prompt_editor.py     # Allows users to edit prompts
│   ├── utils                   # Contains utility functions
│   │   ├── __init__.py        # Initializes the utils package
│   │   ├── api_handler.py      # Interacts with the API for OCR
│   │   └── image_processor.py  # Preprocesses images for analysis
│   └── config                 # Configuration settings
│       └── settings.py        # Contains default values and API keys
├── requirements.txt            # Lists project dependencies
├── .gitignore                  # Specifies files to ignore in Git
└── README.md                   # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ocr-streamlit-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run src/main.py
   ```

## Usage

- Upload your API endpoint using the provided uploader.
- Upload an image that you want to analyze.
- Edit the prompt as needed.
- Click the submit button to analyze the image based on the prompt.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
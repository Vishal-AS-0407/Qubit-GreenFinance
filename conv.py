import requests
import base64
import os

def convert_pdf_to_txt(uploaded_file):
    """
    Converts an uploaded PDF to text using ConvertAPI.
    """
    api_key = ""
    url = "https://v2.convertapi.com/convert/pdf/to/txt"

    # Encode the uploaded file in base64
    pdf_base64 = base64.b64encode(uploaded_file.read()).decode("utf-8")

    # Prepare the payload
    payload = {
        "Parameters": [
            {
                "Name": "File",
                "FileValue": {
                    "Name": uploaded_file.name,
                    "Data": pdf_base64
                }
            },
            {
                "Name": "StoreFile",
                "Value": True
            }
        ]
    }

    # Set headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Send POST request
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        file_url = result['Files'][0]['Url']
        # Download the text content
        file_response = requests.get(file_url)
        if file_response.status_code == 200:
            return file_response.content.decode("utf-8")
        else:
            raise Exception(f"Error downloading text file: {file_response.status_code}")
    else:
        raise Exception(f"PDF to text conversion failed: {response.status_code}, {response.text}")

import os
import requests
from azure.storage.blob import BlobServiceClient, BlobClient
from dotenv import load_dotenv
from azure.storage.blob import ContentSettings

# Load environment variables from .env file
load_dotenv()

# Azure Blob Storage credentials
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_CONTAINER_NAME')
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Azure DALL·E credentials
OPENAI_API_KEY = os.getenv('AZURE_OPENAI_KEY')
OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

def generate_image_from_prompt(prompt: str):
    """
    Generate an image using Azure DALL·E based on the user's prompt.

    :param prompt: The prompt for image generation
    :return: The image file (binary content) from DALL·E
    """
    headers = {
        'api-key': f'{OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"  # You can change the size as needed
    }

    response = requests.post(OPENAI_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        image_data = requests.get(image_url).content
        return image_data
    else:
        raise Exception(f"Failed to generate image: {response.text}")

def upload_to_blob(file_data, blob_name: str,content_type="image/png"):
    """
    Upload the generated image to Azure Blob Storage.

    :param file_data: Binary image data
    :param blob_name: The name of the blob (file) in the Azure container
    :return: The public URL of the uploaded image
    """
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the image to the blob
    blob_client.upload_blob(file_data, blob_type="BlockBlob", overwrite=True, content_settings=ContentSettings(content_type=content_type))

    # Make the blob public
    container_client = blob_service_client.get_container_client(container_name)
    container_client.set_container_access_policy(signed_identifiers={}, public_access="blob")


    # Return the public URL of the uploaded blob
    public_url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net/{container_name}/{blob_name}"
    return public_url

# Dalle Project

This project is a Django-based web application that generates images from text prompts using Azure OpenAI and stores them in Azure Blob Storage.

## Features

- Generate images from text prompts
- Store generated images in Azure Blob Storage
- REST API for image generation

## Requirements

- Python 3.8+
- Django 4.1.7
- Azure account with Blob Storage and OpenAI services

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/G00SEBUMPS/dalle-prompt.git
    cd dalle
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables for Azure services:
    ```sh
    export AZURE_STORAGE_CONNECTION_STRING='your_connection_string'
    export AZURE_CONTAINER_NAME='your_container_name'
    export AZURE_OPENAI_KEY='your_openai_key'
    export AZURE_OPENAI_ENDPOINT='your_openai_endpoint'
    ```

5. Run database migrations:
    ```sh
    python manage.py migrate
    ```

6. Start the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Use the REST API to generate images by sending a POST request to `/generate_image` with a JSON body containing the `prompt` field.

## Running Tests

To run the tests, use the following command:
```sh
python manage.py test
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

For any inquiries, please contact [positive.vaipsi@gmail.com](mailto:positive.vaipsi@gmail.com).

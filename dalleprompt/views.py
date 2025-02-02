from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import traceback
import uuid
from .azure.blob_helper import generate_image_from_prompt, upload_to_blob

class GenerateImageView(APIView):
    def post(self, request):
        """
        Endpoint to generate an image based on the user prompt, store it in Azure Blob, and return the image URL.
        """
        prompt = request.data.get('prompt')  # Get the prompt from the user

        if not prompt:
            return JsonResponse({"error": "Prompt is required."}, status=400)

        try:
            # Generate the image using Azure DALL·E
            image_data = generate_image_from_prompt(prompt)
            # Create a unique blob name using UUID to avoid collisions
            blob_name = f"generated_image_{uuid.uuid4()}.png"

            # Upload the generated image to Azure Blob Storage
            public_url = upload_to_blob(image_data, blob_name)

            return JsonResponse({"image_url": public_url}, status=200)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

class HealthCheckView(APIView):
    def get(self, request):
        """
        Endpoint to check the health status of the server.
        """
        return JsonResponse({"status": "ok"}, status=200)
    
class UploadImageToAzureBlob(APIView):
    def post(self, request):
        """
        Endpoint to upload an image to Azure Blob Storage.
        """
        image_file = request.FILES.get('image_file')  # Get the image file from the request

        if not image_file:
            return JsonResponse({"error": "Image file is required."}, status=400)

        try:
            # Create a unique blob name using UUID to avoid collisions
            blob_name = f"uploaded_image_{uuid.uuid4()}.png"

            # Upload the image to Azure Blob Storage
            public_url = upload_to_blob(image_file.read(), blob_name)

            return JsonResponse({"image_url": public_url}, status=200)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)
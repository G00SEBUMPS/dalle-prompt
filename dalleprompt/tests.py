from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
import uuid

class GenerateImageViewTests(APITestCase):
    @patch('dalleprompt.azure.blob_helper.generate_image_from_prompt')
    @patch('dalleprompt.azure.blob_helper.upload_to_blob')
    def test_generate_image_success(self, mock_upload_to_blob, mock_generate_image_from_prompt):
        mock_generate_image_from_prompt.return_value = b'image_data'
        mock_upload_to_blob.return_value = 'http://example.com/generated_image.png'

        url = reverse('generate_image')
        data = {'prompt': 'a beautiful sunset'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image_url', response.data)
        self.assertEqual(response.data['image_url'], 'http://example.com/generated_image.png')

    def test_generate_image_no_prompt(self):
        url = reverse('generate_image')
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Prompt is required.')

class HealthCheckViewTests(APITestCase):
    def test_health_check(self):
        url = reverse('health_check')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'ok')

class UploadImageToAzureBlobTests(APITestCase):
    @patch('dalleprompt.azure.blob_helper.upload_to_blob')
    def test_upload_image_success(self, mock_upload_to_blob):
        mock_upload_to_blob.return_value = 'http://example.com/uploaded_image.png'

        url = reverse('upload_image')
        with open('test_image.png', 'rb') as image_file:
            response = self.client.post(url, {'image_file': image_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image_url', response.data)
        self.assertEqual(response.data['image_url'], 'http://example.com/uploaded_image.png')

    def test_upload_image_no_file(self):
        url = reverse('upload_image')
        response = self.client.post(url, {}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Image file is required.')
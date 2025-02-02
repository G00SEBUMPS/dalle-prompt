from django.urls import path
from .views import GenerateImageView,HealthCheckView,UploadImageToAzureBlob

urlpatterns = [
    path('generate-image/', GenerateImageView.as_view(), name='generate_image'),
    path('health-check/', HealthCheckView.as_view(), name='health_check'),
    path('upload-image/', UploadImageToAzureBlob.as_view(), name='upload_image'),
]
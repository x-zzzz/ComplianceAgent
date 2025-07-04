from django.urls import path
from .views import PiiDetectView

urlpatterns = [
    path('detect/', PiiDetectView.as_view(), name='pii-detect'),
]

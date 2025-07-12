from django.urls import path
from .views import PiiDetectView, desensitize_view

urlpatterns = [
    path('detect/', PiiDetectView.as_view(), name='pii-detect'),
    path('desensitize/', desensitize_view, name='pii-desensitize'),
]

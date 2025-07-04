from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from .langchain_agent import detect_pii_and_risk
from .models import PiiDetectionRecord
from .serializers import PiiDetectionRecordSerializer

logger = logging.getLogger(__name__)

class PiiDetectView(APIView):
    def post(self, request):
        text = str(request.data.get("text", ""))
        #text = request.data.get("text", "")
        logger.info(f"Type of input text: {type(text)}")  # 应该是 <class 'str'>

        logger.info(f"Received PII detection request. Text length: {len(text)}")
        result = detect_pii_and_risk(text)
        logger.info(f"Detection result: {result}")
        # Save result
        record = PiiDetectionRecord.objects.create(
            text=text,
            detected_entities=result["entities"],
            risk_level=result["risk_level"]
        )
        serializer = PiiDetectionRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

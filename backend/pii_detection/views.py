from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from .langchain_agent import detect_pii_and_risk
from .desensitize import simple_desensitize
from rest_framework.decorators import api_view

@api_view(["POST"])
def desensitize_view(request):
    """
    脱敏处理API，输入：text, entities（可选，若无则自动检测）
    """
    text = request.data.get("text", None)
    entities = request.data.get("entities", None)
    if not text:
        return Response({"error": "请提供待脱敏文本"}, status=status.HTTP_400_BAD_REQUEST)
    # 若未指定entities，则自动检测
    if not entities:
        from .knowledge_utils import load_knowledge_base
        knowledge_base_prompt = load_knowledge_base()
        detect_result = detect_pii_and_risk(text, knowledge_base_prompt)
        # 收集所有实体
        entities = []
        for detail in detect_result.get("details", []):
            entities.extend(detail.get("entities", []))
    # 脱敏
    desensitized_text = simple_desensitize(text, entities)
    return Response({
        "original_text": text,
        "entities": entities,
        "desensitized_text": desensitized_text
    }, status=status.HTTP_200_OK)
from .models import PiiDetectionRecord
from .serializers import PiiDetectionRecordSerializer


from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from django.core.files.uploadedfile import UploadedFile
import io
import docx
import PyPDF2

logger = logging.getLogger(__name__)

class PiiDetectView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def extract_text_from_file(self, uploaded_file: UploadedFile) -> str:
        name = uploaded_file.name.lower()
        if name.endswith('.txt'):
            return uploaded_file.read().decode('utf-8', errors='ignore')
        elif name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            return '\n'.join([p.text for p in doc.paragraphs])
        elif name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
            return text
        else:
            raise ValueError('Unsupported file type')

    def post(self, request):
        text = request.data.get("text", None)
        file = request.FILES.get('file', None)
        extracted_text = None
        if file:
            try:
                extracted_text = self.extract_text_from_file(file)
                logger.info(extracted_text)
            except Exception as e:
                logger.error(f"File parse error: {e}")
                return Response({"error": "文件解析失败: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif text:
            extracted_text = text
        else:
            return Response({"error": "请上传文件或输入文本"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"PII检测请求，文本长度: {len(extracted_text)}")
        # 动态加载知识库内容，转为 prompt
        from .knowledge_utils import load_knowledge_base
        knowledge_base_prompt = load_knowledge_base()
        result = detect_pii_and_risk(extracted_text, knowledge_base_prompt)
        logger.info(f"检测结果: {result}")
        record = PiiDetectionRecord.objects.create(
            text=extracted_text,
            detected_entities=result.get("entities", []),
            risk_level=result.get("risk_level", "未知")
        )
        serializer = PiiDetectionRecordSerializer(record)
        # 返回原文内容，便于前端展示
        # 直接返回 deepseek summary 字段内容，全部顶层展开
        from .knowledge_lookup import find_knowledge_explanation
        summary = result.get("summary", {})
        overall_reason = summary.get("overall_reason", "")
        knowledge_explanation = find_knowledge_explanation(overall_reason)
        return Response({
            "total_entities": summary.get("total_entities", 0),
            "risk_level": summary.get("risk_level", "未知"),
            "overall_reason": overall_reason,
            "overall_reason_explanation": knowledge_explanation,
            "details": result.get("details", []),
            "raw_response": result.get("raw_response"),
            "text": extracted_text
        }, status=status.HTTP_201_CREATED)

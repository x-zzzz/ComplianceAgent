from django.db import models



class PiiDetectionRecord(models.Model):
    text = models.TextField()
    detected_entities = models.JSONField()
    risk_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PII Detection at {self.created_at} (Risk: {self.risk_level})"

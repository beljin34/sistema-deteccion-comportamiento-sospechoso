from rest_framework import serializers
from .models import SuspiciousActivity

class ActivitySerializer(serializers.ModelSerializer):
    """Serializador para actividades sospechosas"""
    
    class Meta:
        model = SuspiciousActivity
        fields = [
            'id',
            'timestamp',
            'activity_type',
            'confidence',
            'location',
            'video_url',
            'description'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def validate_confidence(self, value):
        """Validar que confidence esté entre 0 y 1"""
        if not 0 <= value <= 1:
            raise serializers.ValidationError(
                "La confianza debe estar entre 0 y 1"
            )
        return value

class VideoUploadSerializer(serializers.Serializer):
    """Serializador para carga de videos"""
    video = serializers.FileField()
    location = serializers.CharField(max_length=255)
    
    def validate_video(self, value):
        if value.size > 100 * 1024 * 1024:  # 100MB
            raise serializers.ValidationError(
                "El archivo no puede exceder 100MB"
            )
        return value

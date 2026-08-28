from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
import time

from .models import SuspiciousActivity
from .serializers import ActivitySerializer, VideoUploadSerializer
from .tasks import process_video_analysis

class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar actividades sospechosas"""
    queryset = SuspiciousActivity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ['activity_type', 'location']
    ordering_fields = ['timestamp', 'confidence']
    ordering = ['-timestamp']
    
    @action(detail=False, methods=['post'])
    def analyze_video(self, request):
        """
        Endpoint para cargar y analizar un video.
        Detecta comportamientos sospechosos usando IA.
        """
        serializer = VideoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        video_file = serializer.validated_data['video']
        location = serializer.validated_data['location']
        
        # Procesar video de forma asíncrona
        task = process_video_analysis.delay(
            video_path=str(video_file),
            location=location,
            user_id=request.user.id
        )
        
        return Response(
            {
                'task_id': task.id,
                'status': 'processing',
                'message': 'El video está siendo procesado'
            },
            status=status.HTTP_202_ACCEPTED
        )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas de las actividades detectadas"""
        total = SuspiciousActivity.objects.count()
        by_type = SuspiciousActivity.objects.values('activity_type').count()
        avg_confidence = SuspiciousActivity.objects.values('activity_type').annotate(
            avg_conf=models.Avg('confidence')
        )
        
        return Response({
            'total_activities': total,
            'by_activity_type': by_type,
            'average_confidence': list(avg_confidence)
        })
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Obtiene detalles completos de una actividad"""
        activity = self.get_object()
        serializer = self.get_serializer(activity)
        return Response(serializer.data)

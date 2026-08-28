from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class SuspiciousActivity(models.Model):
    """Modelo para registrar actividades sospechosas detectadas"""
    
    ACTIVITY_TYPES = (
        ('loitering', 'Merodeando'),
        ('running', 'Corriendo'),
        ('falling', 'Cayendo'),
        ('fighting', 'Peleando'),
        ('theft', 'Robo'),
        ('vandalism', 'Vandalismo'),
        ('unknown', 'Desconocida'),
    )
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='Nivel de confianza de la detección (0-1)'
    )
    location = models.CharField(max_length=255)
    video_url = models.URLField()
    description = models.TextField(blank=True)
    frame_count = models.IntegerField(default=0)
    processing_time = models.FloatField(default=0, help_text='Tiempo de procesamiento en segundos')
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['activity_type', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.activity_type} - {self.location} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
    
    def confidence_percentage(self):
        """Retorna confianza como porcentaje"""
        return round(self.confidence * 100, 2)

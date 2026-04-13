from django.db import models

class ProcessedDocument(models.Model):
    original_filename = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('image', 'Image')])

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.display_name} ({self.upload_date.strftime('%d-%m-%Y')})"
    
    
#     python manage.py makemigrations docqa
# python manage.py migrate
from django.db import models

# Create your models here.
from core.models import Website
class Masthead(models.Model):
    website = models.OneToOneField(Website, on_delete=models.CASCADE)
    welcome_text = models.CharField(max_length=120)
    masthead_text = models.CharField(max_length=120)
    motto_title = models.CharField(max_length=120)
    motto_description = models.TextField()
    background_image = models.ImageField(upload_to='masthead_backgorund')
    class Meta:
        db_table='t_websitemasthead'
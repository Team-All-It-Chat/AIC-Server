from django.db import models
from accounts.models import *

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    
    writer = models.ForeignKey(to=Member, on_delete=models.CASCADE, blank=False)
    
    title = models.CharField(max_length=30)   
    content = models.TextField()
    
    tag1 = models.CharField(max_length=10,null=True, blank=True)
    tag2 = models.CharField(max_length=10,null=True, blank=True)
    
    image = models.ImageField(null=True, blank=True)
    
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
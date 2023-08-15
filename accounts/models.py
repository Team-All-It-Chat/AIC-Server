from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser
# Create your models here.

def korean_validator(value):
    if not all('\uac00' <= char <= '\ud7a3' for char in value):
        raise validators.ValidationError("한글만 입력 가능합니다.")   

class Member(AbstractUser):  
    
    name = models.CharField(max_length=8, validators=[korean_validator])
     
    kor_univ = models.CharField(max_length=20)
    kor_major = models.CharField(max_length=20)
    
    kor_email = models.EmailField()
    
    is_mentor = models.BooleanField(default=False)
    
    refresh_token = models.CharField(max_length=100)
        
    # 멘토 사용자만   
    continent = models.CharField(max_length=20, blank=True)
    contry = models.CharField(max_length=20, blank=True)    
    
    
    foreign_univ = models.CharField(max_length=100, blank=True)
    foreign_major = models.CharField(max_length=20, blank=True)
    
    foreign_email = models.EmailField(blank=True)
    exchangeSemester = models.CharField(max_length=10, blank=True)    
    exchangeDuration = models.CharField(max_length=10, blank=True)
    
    total_score = models.IntegerField(null=True, blank=True)
    
    chat_count = models.IntegerField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    profile = models.IntegerField(null=True, blank=True)
    
    tag1 = models.CharField(max_length=20, null=True, blank=True)  
    tag2 = models.CharField(max_length=20, null=True, blank=True)        
    tag3 = models.CharField(max_length=20, null=True, blank=True)
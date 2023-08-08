from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser
# Create your models here.

def korean_validator(value):
    if not all('\uac00' <= char <= '\ud7a3' for char in value):
        raise validators.ValidationError("한글만 입력 가능합니다.")

class Profile(models.Model):    
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=8, validators=[korean_validator])
     
    kor_univ = models.CharField(max_length=20)
    kor_major = models.CharField(max_length=20)
    
    kor_email = models.EmailField()
    
    is_mento = models.BooleanField(default=False)
    
    refresh_token = models.CharField(max_length=100)
        
    # 멘토 사용자만   
    continent = models.CharField(max_length=20, blank=True)
    contry = models.CharField(max_length=20, blank=True)    
    
    foreign_univ = models.CharField(max_length=20, blank=True)
    foreign_major = models.CharField(max_length=20, blank=True)
    
    foreign_email = models.EmailField(blank=True)
    
    exchangeSemester = models.CharField(max_length=10, blank=True)
    
    CHOICE = (
        ('1학기', '1학기'),
        ('1년', '1년'),
    )
    
    exchangeDuration = models.CharField(max_length=10, choices=CHOICE, blank=True)

class Member(AbstractUser):
    id = models.AutoField(primary_key=True)    
    profile = models.ForeignKey(to=Profile , on_delete=models.CASCADE)  
        
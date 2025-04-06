from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    ADMIN = "admin"
    USERS = "users"
    
    Roles = (
        (USERS, "Users"),
        (ADMIN, "Admin"),
    )
    
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles, default=USERS)
    profile_image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  
        blank=True,
    )
    
    def __str__(self):
        return f"{self.phone_number}"

        
        
    
        
        
        
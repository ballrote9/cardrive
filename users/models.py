from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users (AbstractUser):
    middle_name = models.CharField(null= True, blank= True, verbose_name= "Отчество", max_length= 20 )
    image = models.ImageField(upload_to = "users_images", blank= True, null= True, verbose_name= "Аватар")
    passport_num = models.CharField(unique= True, blank= True, null= True, verbose_name= "Серия и номер паспорта", max_length= 10 )
    drive_license_num = models.CharField(unique= True, blank = True, null= True, verbose_name= "Серия и номер водительской лицензии", max_length= 10 )
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
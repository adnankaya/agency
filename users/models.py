from django.db import models
from django.contrib.auth.models import AbstractUser, User
from core.models import Base


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone_number = models.CharField(max_length=24)

    class Meta:
        db_table = 't_profile'


class SocialAccount(Base):
    # TODO
    pass

from django.db import models
from django.contrib.auth.models import AbstractUser, User
from core.models import Base


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone_number = models.CharField(max_length=24)
    title = models.CharField(max_length=60, null=True)
    has_team = models.BooleanField(default=False)

    class Meta:
        db_table = 't_profile'

    def __str__(self) -> str:
        return f"Profile {self.user.username}"


class SocialAccount(Base):
    slug = models.SlugField(max_length=24)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='socialaccounts')
    url = models.URLField()

    class Meta:
        db_table = 't_socialaccount'
        unique_together = [['slug', 'user']]

    def __str__(self) -> str:
        return f"{self.slug} {self.user.username}"

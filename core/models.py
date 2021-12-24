from django.db import models


class Base(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = 'objects'


class Website(models.Model):
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=60, default='demosite')
    attributes = models.JSONField(null=True)
    logo = models.FileField(upload_to='logos', default='default.jpg')
    mails = models.ManyToManyField('Mail')
    phones = models.ManyToManyField('Phone')

    class Meta:
        db_table = 't_website'

    def __str__(self) -> str:
        return self.name


class Mail(Base):
    email = models.EmailField()
    slug = models.SlugField(max_length=24, unique=True)
    display = models.BooleanField(default=True)

    class Meta:
        db_table = 't_mail'

    def __str__(self) -> str:
        return f"Mail {self.email}"


class Phone(Base):
    number = models.CharField(max_length=24)
    slug = models.SlugField(max_length=24, unique=True)
    display = models.BooleanField(default=True)

    class Meta:
        db_table = 't_phone'

    def __str__(self) -> str:
        return f"Phone {self.slug} {self.number}"

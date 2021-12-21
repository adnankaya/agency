from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.models import Base
from core.utils import generate_slug


class Image(Base):
    class Status(models.TextChoices):
        ACTIVE = 'A', _('Active')
        PASSIVE = 'P', _('Passive')

    height = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=1, choices=Status.choices,
                              default=Status.ACTIVE)
    label = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True)

    class Meta:
        abstract = True
        ordering = ('order',)


class Privacy(Base):
    body = models.TextField()

    class Meta:
        db_table = 't_privacy'


class Terms(Base):
    body = models.TextField()

    class Meta:
        db_table = 't_terms'


class About(Base):
    mission = models.TextField()
    vision = models.TextField()

    class Meta:
        db_table = 't_about'


class Address(Base):
    '''info has phone numbers, email addresses, full address'''
    full_address = models.TextField()

    class Meta:
        db_table = 't_address'


class Service(Base):
    name = models.CharField(max_length=240)
    description = models.TextField()
    slug = models.CharField(max_length=250, unique=True)

    class Meta:
        db_table = 't_service'
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.name)
        super(Service, self).save()
    
    def get_absolute_url(self):
        return reverse('company:service-detail',
                       args=[
                           self.slug
                       ])


class ServiceImage(Image):
    image = models.ImageField(height_field="height", width_field="width",
                              upload_to='service_images')
    service = models.ForeignKey('Service', on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_service_image'

    def __str__(self):
        return "%s - %s - %s - %s" % (
            self.service_id, self.status,
            self.image, self.order
        )


class AboutImage(Image):
    image = models.ImageField(height_field="height", width_field="width",
                              upload_to='about_images')
    about = models.ForeignKey('About', on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_about_image'

    def __str__(self):
        return "%s - %s - %s - %s" % (
            self.about_id, self.status,
            self.image, self.order
        )

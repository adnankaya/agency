from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.models import Base, Website
from core.utils import generate_slug
from datetime import date


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
    full_address = models.TextField()
    website = models.ForeignKey(Website, on_delete=models.CASCADE,
    related_name='addresses')
    display = models.BooleanField(default=True)

    class Meta:
        db_table = 't_address'

    def __str__(self) -> str:
        return self.full_address


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
        super(Service, self).save(*args, **kwargs)

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


class Milestone(Base):
    title = models.CharField(max_length=120)
    body = models.TextField()
    date_in = models.DateField(default=date.today)
    image = models.ImageField(upload_to='milestone_images')
    about = models.ForeignKey(About, related_name='milestones',
                              on_delete=models.CASCADE)

    class Meta:
        db_table = 't_milestone'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        super(Milestone, self).save(*args, **kwargs)


class Client(Base):
    website = models.URLField()
    image = models.ImageField(upload_to='clients_images')

    class Meta:
        db_table = 't_client'

    def __str__(self) -> str:
        return self.website


class ContactMessage(Base):
    full_name = models.CharField(max_length=64)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        db_table = 't_contactmessage'

    def __str__(self) -> str:
        return self.message

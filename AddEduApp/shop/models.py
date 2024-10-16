from django.db import models

# Create your models here.


class BusterAbstract(models.Model):
    """ Buster abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Buster(BusterAbstract):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    cost = models.IntegerField(default=30)
    picture = models.ImageField(upload_to='busters/', help_text="Изображение бустера")

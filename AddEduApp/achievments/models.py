from django.db import models


class Achievements(models.Model):
    title = models.CharField(max_length=255)
    requirement = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    pic = models.ImageField(upload_to='achievements/', help_text="Фото ачивки", blank=True, null=True,
                            default='default_pics/achievment.png')
    reward = models.PositiveIntegerField()


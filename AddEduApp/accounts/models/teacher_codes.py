from django.db import models


class TeacherCode(models.Model):
    code = models.CharField(max_length=255)
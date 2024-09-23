from django.db import models


class SchoolName(models.Model):
    name = models.CharField(max_length=255)
    

class TeacherCode(models.Model):
    code = models.CharField(max_length=255)
    school = models.ForeignKey(SchoolName, on_delete = models.SET_NULL, null=True)

class AdminCode(models.Model):
    code = models.CharField(max_length=255)
    school = models.ForeignKey(SchoolName, on_delete = models.SET_NULL, null=True)
    is_adm = models.BooleanField(default=True)


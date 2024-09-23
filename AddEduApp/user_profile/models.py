import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models.user import User
from shop.models import Buster
from achievments.models import Achievements


class AbstractProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, help_text="Введите имя пользователя")
    last_name = models.CharField(max_length=255, help_text="Введите фамилию пользователя")
    surname = models.CharField(max_length=255, help_text="Введите отчество пользователя", blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', help_text="Фото пользователя", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractStatistics(models.Model):
    coins_collected = models.PositiveIntegerField(help_text="Монет собрано", default=0)
    rain_repelled = models.PositiveIntegerField(help_text="Атак дождя отражено", default=0)
    drought_repelled = models.PositiveIntegerField(help_text="Атак засухи отражено", default=0)
    ufo_repelled = models.PositiveIntegerField(help_text="Атак НЛО отражено", default=0)

    class Meta:
        abstract = True


class TreeStatistics(AbstractStatistics):
    tree = models.OneToOneField('Tree', on_delete=models.CASCADE, related_name='statistics')
    ufo_repulsed = models.PositiveIntegerField(help_text="Нло отбито", default=0)
    flood_repulsed = models.PositiveIntegerField(help_text="Наводнений отбито", default=0)
    drought_repulsed = models.PositiveIntegerField(help_text="Засух отбито", default=0)
    coins_collected = models.PositiveIntegerField(help_text="Монет заработано c этого дерева", default=0)


class PlayerStatistics(AbstractStatistics):
    trees_planted = models.PositiveIntegerField(help_text="Деревьев посажено", default=0)
    coins_collected = models.PositiveIntegerField(help_text="Монет заработано", default=0)


class Tree(models.Model):
    COLLECTED_COINS = 20

    EVENTS = (
        (0, 'UFO'),
        (1, 'Drought'),
        (2, 'Flood')
    )
    STAGES = (
        (1, 'FIRST STAGE'),
        (2, 'SECOND STAGE'),
        (3, 'THIRD STAGE'),
        (4, 'MONEY COLLECT STAGE'),
    )

    planting_date = models.DateTimeField(help_text="Дата посадки дерева", auto_now_add=True)
    stage = models.PositiveIntegerField(help_text="Стадия роста дерева", default=0, choices=STAGES)
    # Возможно было бы логичней вынести поля ниже в отдельную модель
    event = models.PositiveIntegerField(help_text="Следующий катаклизм", null=True, choices=EVENTS)
    start_time = models.DateTimeField(help_text="Время начала негативного ивента", null=True)
    duration = models.DurationField(default=datetime.timedelta(minutes=5), help_text="Длительность негативного ивента")


class CounterOfBusters(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    buster = models.ForeignKey(Buster, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(help_text='Количество бустеров у студента', default=0)


class StudentProfile(AbstractProfile):
    balance = models.IntegerField(help_text="Введите баланс DanceCoin", default=0)
    energy = models.IntegerField(help_text="Введите баланс энергии", default=0)
    achievements = models.ManyToManyField(Achievements, related_name='profile')
    busters = models.ManyToManyField(Buster, help_text="Список бустеров", related_name='profile',
                                     through=CounterOfBusters)
    tree = models.OneToOneField(Tree, on_delete=models.SET_NULL, null=True)
    statistics = models.OneToOneField(PlayerStatistics, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name } {self.last_name}'

    class Meta:
        ordering = ('last_name', 'first_name')


class MentorProfile(AbstractProfile):
    def __str__(self):
        return f'{self.first_name } {self.last_name}'


class Group(models.Model):
    name = models.CharField(max_length=255, help_text='Название группы')
    students = models.ManyToManyField('StudentProfile')
    mentors = models.ManyToManyField('MentorProfile')

    def __str__(self):
        return self.name


class Attendance(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance')
    dates = ArrayField(models.DateField())

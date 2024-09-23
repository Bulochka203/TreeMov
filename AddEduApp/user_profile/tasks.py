import asyncio
import datetime
import random
from time import sleep
import dramatiq
from .models import StudentProfile
from .utilities import get_delay
from .models import Tree


def time_to_seconds(m=0, h=0, d=0):
    return 60 * m + 60 ** 2 * h + 60 ** 2 * 24 * d


STAGE_CHANGE_TIME = time_to_seconds(0.5, 0, 0)
# STAGE_CHANGE_TIME = time_to_seconds(0, 8, 0) # 8 часов в секундах


@dramatiq.actor
def tree_progress(student_pk):
    student = StudentProfile.objects.get(pk=student_pk)
    tree = student.tree
    print(tree.stage)
    start = 1
    if tree.stage > 1:
        start = tree.stage

    for i in range(start, 5):
        tree.stage = i
        tree.save()
        print(f'Stage: {tree.stage}')
        if i < 4:
            sleep(STAGE_CHANGE_TIME)
    print('Дерево выросло, можно собрать урожай')
    set_event.send_with_options(args=(student_pk, random.choice(Tree.EVENTS)[0]), delay=get_delay(True))


@dramatiq.actor
def set_event(student_pk, event_id):
    print(f'Все ивенты: {Tree.EVENTS}')
    print(f'Начало ивента {event_id}')
    t = datetime.datetime.now() + datetime.timedelta(minutes=5)
    print(f'Конец ивента через 5 минут, в {t.hour}:{t.minute}')
    student = StudentProfile.objects.get(pk=student_pk)
    tree = student.tree
    tree.event = event_id
    tree.start_time = datetime.datetime.now()
    tree.save()
    print(tree.stage)

from .models import Tree, TreeStatistics
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Tree, weak=False)
def create_tree_statistics(sender, instance, created, **kwargs):
    if created:
        TreeStatistics.objects.create(tree=instance)




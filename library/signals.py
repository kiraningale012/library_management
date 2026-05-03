from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowRequest

@receiver(post_save, sender=BorrowRequest)
def update_copies(sender, instance, **kwargs):
    if instance.status == 'APPROVED':
        instance.book.available_copies -= 1
        instance.book.save()
    if instance.status == 'RETURNED':
        instance.book.available_copies += 1
        instance.book.save()
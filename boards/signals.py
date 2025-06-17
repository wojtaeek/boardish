from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from boards.models import Element


@receiver(post_save, sender=Element)
def update_widget(sender, instance, created, **kwargs):
    print(f"THE THING DID UPDATE id: {instance.id}")
    if created:
        print("THE THING WAS CREATED")
        channel_layer = get_channel_layer()
        group_name = f"board-update-{instance.board.id}"
        event = {
            "type": "instance_created",
            "id": instance.order,
            "x": instance.x,
            "y": instance.y,
            "w": instance.w,
            "h": instance.h,
            "content": instance.content,
            "kind": instance.type,
        }
        async_to_sync(channel_layer.group_send)(group_name, event)
    if not created:
        print("THE THING WAS UPDATED")
        channel_layer = get_channel_layer()
        group_name = f"board-update-{instance.board.id}"
        print(f"THE THINGS' GROUP: {group_name}")
        event = {
            "type": "instance_updated",
            "id": instance.order,
            "x": instance.x,
            "y": instance.y,
            "w": instance.w,
            "h": instance.h,
            "content": instance.content,
            "kind": instance.type,
        }
        async_to_sync(channel_layer.group_send)(group_name, event)


@receiver(post_delete, sender=Element)
def delete_widget(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_name = f"board-update-{instance.board.id}"
    event = {
        "type": "instance_deleted",
        "id": instance.order,
    }
    async_to_sync(channel_layer.group_send)(group_name, event)

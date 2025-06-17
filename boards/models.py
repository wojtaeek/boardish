from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Board(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    user = models.ManyToManyField(User, related_name="boards", through="UserBoard")

    def __str__(self):
        return self.title


class UserBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]


class Element(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="elements")
    order = models.PositiveIntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField(default=1)
    h = models.IntegerField(default=1)

    ELEMENT_TYPES = [
        ("button", "Button"),
        ("text", "Text"),
        ("image", "Image"),
        ("clock", "Clock"),
        ("paint", "Paint"),
        ("custom", "Custom"),
    ]
    type = models.CharField(max_length=50, choices=ELEMENT_TYPES, default="custom")

    data = models.JSONField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)  # tu wszystko upchać
    # image = models.ImageField(upload_to="board_images")

    def __str__(self):
        return f"Element {self.id} ({self.type}) at ({self.x}, {self.y})"

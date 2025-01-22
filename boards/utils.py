from django.db.models import Max
from boards.models import UserBoard, Element


def get_max_order(user) -> int:
    existing_films = UserBoard.objects.filter(user=user)
    if not existing_films.exists():
        return 1
    else:
        current_max = existing_films.aggregate(max_order=Max("order"))["max_order"]
        return current_max + 1


def get_max_order_elements(board) -> int:
    existing_elements = Element.objects.filter(board=board)
    if not existing_elements.exists():
        return 1
    else:
        current_max = existing_elements.aggregate(max_order=Max("order"))["max_order"]
        return current_max + 1


def reorder(user):
    existing_films = UserBoard.objects.filter(user=user)
    if not existing_films.exists():
        return
    number_of_films = existing_films.count()
    new_ordering = range(1, number_of_films + 1)

    for order, user_film in zip(new_ordering, existing_films):
        user_film.order = order
        user_film.save()

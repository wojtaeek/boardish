from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.http.response import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from boards.models import Board, Element, UserBoard
from boards.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from boards.utils import get_max_order, reorder
from django.views.generic import ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


class IndexView(TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class BoardList(LoginRequiredMixin, ListView):
    template_name = "boards.html"
    model = UserBoard
    paginate_by = settings.PAGINATE_BY
    context_object_name = "boards"

    def get_template_names(self):
        if self.request.htmx:
            return "partials/board-list-elements.html"
        return "boards.html"

    def get_queryset(self):
        return UserBoard.objects.prefetch_related("board").filter(
            user=self.request.user
        )


def index(request):
    boards = Board.objects.all()
    print(Board.objects.get.all())
    return render(request, "index.html", {"boards": boards})


def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse(
            "<div id='username-error' class='error'>This username already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='username-error' class='success'>This username is available</div>"
        )


@require_POST
def update_grid(request):
    data = json.loads(request.body)
    print("Received data:", data)  # This logs to the console
    return JsonResponse({"status": "success", "received_data": data})


@login_required
def board_view(request, pk):
    board_id = get_object_or_404(UserBoard, id=pk).board_id
    board = get_object_or_404(Board, id=board_id)
    elements = board.elements.order_by("order")

    for element in elements:
        match element.type:
            case "button":
                element.content = f"<button>{element.content}</button>"
            case "text":
                element.content = f"<textarea>{element.content}</textarea>"
            case "image":
                element.content = f"<img src='{element.content}' />"

    serialized_elements = [
        {
            "id": element.order,
            "x": element.x,
            "y": element.y,
            "w": element.w,
            "h": element.h,
            "content": element.content,
        }
        for element in elements
    ]

    return render(
        request,
        "partials/board-detail.html",
        {
            "board": board,
            "serialized_elements": serialized_elements,
        },
    )


@csrf_exempt
def save_board(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        board = get_object_or_404(Board, id=pk)

        # Clear existing elements and replace with new data
        # board.elements.all().delete() #man do i not like this

        for item in data:
            Element.objects.create(
                board=board,
                order=item.get("order", 0),
                x=item.get("x", 0),
                y=item.get("y", 0),
                w=item.get("w", 1),
                h=item.get("h", 1),
                content=item.get("content", ""),
                type=item.get("type", "custom"),
                data=item.get("data", None),
            )

        return JsonResponse({"status": "success"})

    return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required
def board_list(request):
    boards = UserBoard.objects.filter(user=request.user).order_by("order")
    return render(request, "partials/board-list.html", {"boards": boards})


@login_required
def create_board(request):
    board_pks_order = request.POST.getlist("board_order")
    title = request.POST.get("boardtitle")
    if Board.objects.filter(title=title).exists():
        messages.error(request, f"{title} already exists")
        boards = UserBoard.objects.filter(user=request.user).order_by("order")
        return render(request, "partials/board-list.html", {"boards": boards})
    else:
        board = Board.objects.create(title=title)
        UserBoard.objects.create(
            board=board, user=request.user, order=get_max_order(request.user)
        )

        boards = UserBoard.objects.filter(user=request.user)
        messages.success(request, f"Created {title}")
        # check if said title exists
        paginator = Paginator(boards, settings.PAGINATE_BY)
        page_number = len(board_pks_order) / settings.PAGINATE_BY
        page_obj = paginator.get_page(page_number)
        context = {"boards": boards, "page_obj": page_obj}

        return render(request, "partials/board-list.html", context)


@login_required
def add_board(request):
    title = request.POST.get("boardtitle")

    board = Board.objects.get_or_create(title=title)[0]

    if not UserBoard.objects.filter(board=board, user=request.user).exists():
        UserBoard.objects.create(
            board=board, user=request.user, order=get_max_order(request.user)
        )

    boards = UserBoard.objects.filter(user=request.user)
    messages.success(request, f"Added {title} to list of boards")
    board_pks_order = request.POST.getlist("board_order")
    paginator = Paginator(boards, settings.PAGINATE_BY)
    page_number = len(board_pks_order) / settings.PAGINATE_BY
    page_obj = paginator.get_page(page_number)
    context = {"boards": boards, "page_obj": page_obj}

    return render(request, "partials/board-list.html", context)


def sort(request):
    board_pks_order = request.POST.getlist("board_order")
    boards = []
    updated_boards = []

    # fetch user's films in advance (rather than once per loop)
    userboards = UserBoard.objects.prefetch_related("board").filter(user=request.user)

    for idx, board_pk in enumerate(board_pks_order, start=1):
        # find instance w/ the correct PK
        userboard = next(u for u in userboards if u.pk == int(board_pk))

        # add changed movies only to an updated_films list
        if userboard.order != idx:
            userboard.order = idx
            updated_boards.append(userboard)

        boards.append(userboard)

    # bulk_update changed UserFilms's 'order' field
    UserBoard.objects.bulk_update(updated_boards, ["order"])

    paginator = Paginator(boards, settings.PAGINATE_BY)
    page_number = len(board_pks_order) / settings.PAGINATE_BY
    page_obj = paginator.get_page(page_number)
    context = {"boards": boards, "page_obj": page_obj}

    return render(request, "partials/board-list.html", context)


@login_required
def detail(request, pk):
    userboard = get_object_or_404(UserBoard, pk=pk)
    context = {"userboard": userboard}
    return render(request, "partials/board-detail.html", context)


@login_required
def boards_partial(request):
    boards = UserBoard.objects.filter(user=request.user)
    return render(request, "partials/board-list.html", {"boards": boards})


@require_http_methods(["DELETE"])
@login_required
def delete_board(request, pk):
    ...
    # remove the film from the user's list
    UserBoard.objects.get(pk=pk).delete()

    reorder(request.user)

    # return template fragment with all the user's films
    boards = UserBoard.objects.filter(user=request.user).order_by("order")
    board_pks_order = request.POST.getlist("board_order")
    paginator = Paginator(boards, settings.PAGINATE_BY)
    page_number = len(board_pks_order) / settings.PAGINATE_BY
    page_obj = paginator.get_page(page_number)
    context = {"boards": boards, "page_obj": page_obj}

    return render(request, "partials/board-list.html", context)


@login_required
def search_board(request):
    search_text = request.POST.get("search")

    # look up all films that contain the text
    # exclude user films
    userboards = UserBoard.objects.filter(user=request.user)
    results = Board.objects.filter(title__icontains=search_text).exclude(
        title__in=userboards.values_list("board__title", flat=True)
    )
    context = {"results": results}
    return render(request, "partials/search-results.html", context)


def clear(request):
    return HttpResponse("")


# elements
@login_required
def update_element(request):
    board_id = request.POST.get("pk")
    board = get_object_or_404(Board, id=board_id)
    order = request.POST.get("id")
    element = get_object_or_404(Element, order=order, board=board)
    element.x = request.POST.get("x")
    element.y = request.POST.get("y")
    element.w = request.POST.get("w")
    element.h = request.POST.get("h")
    element.save()

    return HttpResponse(status=204)  # this works TvT


@login_required
@require_http_methods(["DELETE"])
def delete_element(request):
    id = request.GET.get("id")
    pk = request.GET.get("pk")
    element = get_object_or_404(Element, order=id, board=pk)
    element.delete()
    return HttpResponse(status=204)

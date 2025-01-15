from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from boards.models import Board, Element, UserBoard
from boards.forms import RegisterForm
from django.contrib.auth.decorators import login_required


def index(request):
    boards = Board.objects.all()
    print(Board.objects.get.all())
    return render(request, "index.html", {"boards": boards})


@require_POST
def update_grid(request):
    data = json.loads(request.body)
    print("Received data:", data)  # This logs to the console
    return JsonResponse({"status": "success", "received_data": data})


class IndexView(TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


def board_view(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    elements = board.elements.order_by("order")

    serialized_elements = []
    for element in elements:
        serialized_elements.append(
            {
                "id": element.id,
                "x": element.x,
                "y": element.y,
                "w": element.w,
                "h": element.h,
                "content": element.content or "",
            }
        )

    return render(
        request,
        "board_view.html",
        {
            "board": board,
            "serialized_elements": serialized_elements,
        },
    )


@login_required
def board_list(request):
    boards = Board.objects.filter(user=request.user).order_by("id")
    return render(request, "board_list.html", {"boards": boards})

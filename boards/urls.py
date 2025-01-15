from django.urls import path, re_path
from django.contrib import admin
from boards import views
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.IndexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("board/", views.board_list, name="board_list"),
    path("board/<int:board_id>/", views.board_view, name="board_view"),
    # re_path(r"^$", lambda request: redirect("/index/", permanent=True)),
]

htmx_patterns = [
    path("update-grid/", views.update_grid, name="update_grid"),
]

urlpatterns += htmx_patterns

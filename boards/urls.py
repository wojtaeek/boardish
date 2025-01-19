from django.urls import path
from django.contrib import admin
from boards import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.IndexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("board/", views.board_list, name="board_list"),
    path("board/<int:board_id>/", views.board_view, name="board_view"),
    # re_path(r"^$", lambda request: redirect("/index/", permanent=True)),
    path("boards/", views.BoardList.as_view(), name="board-list"),
]

htmx_patterns = [
    path("update-grid/", views.update_grid, name="update_grid"),
    path("add-board/", views.add_board, name="add-board"),
    path("sort/", views.sort, name="sort"),
    path("board-list-partial", views.board_list, name="board-list-partial"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("delete-board/<int:pk>/", views.delete_board, name="delete-board"),
    path("search-board/", views.search_board, name="search-board"),
]

urlpatterns += htmx_patterns

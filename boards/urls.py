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
    path("boards/", views.BoardList.as_view(), name="board-list"),
    # re_path(r"^$", lambda request: redirect("/index/", permanent=True)),
]

htmx_patterns = [
    path("check_username/", views.check_username, name="check-username"),
    path("update-grid/", views.update_grid, name="update_grid"),
    path("create-board/", views.create_board, name="create-board"),
    path("add-board/", views.add_board, name="add-board"),
    path("sort/", views.sort, name="sort"),
    path("board-list-partial", views.boards_partial, name="board-list-partial"),
    path("delete-board/<int:pk>/", views.delete_board, name="delete-board"),
    path("search-board/", views.search_board, name="search-board"),
    path("clear/", views.clear, name="clear"),
    path("detail/<int:pk>/", views.board_view, name="detail"),
    path("detail/<int:pk>/save/", views.save_board, name="save-board"),
    path("update-element/", views.update_element, name="update_element"),
    path("delete-element/", views.delete_element, name="delete_element"),
    path("add-widget/<int:pk>/", views.add_widget, name="add-widget"),
]

urlpatterns += htmx_patterns

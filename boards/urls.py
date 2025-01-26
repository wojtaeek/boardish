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
    path("boards/", views.BoardList.as_view(), name="board-list"),
    re_path(r"^$", lambda request: redirect("/index/", permanent=True)),
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
    path("boards/<int:pk>/", lambda request, pk: redirect("board-list")),
    path("update-element/", views.update_element, name="update_element"),
    path("delete-element/", views.delete_element, name="delete_element"),
    path("add-widget/<int:pk>/", views.add_widget, name="add-widget"),
    path(
        "update-textarea-content/",
        views.update_textarea_content,
        name="update-textarea-content",
    ),
    path("upload-image/", views.upload_image, name="upload-image"),
]

urlpatterns += htmx_patterns

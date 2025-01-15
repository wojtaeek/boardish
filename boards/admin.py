from django.contrib import admin
from .models import User, Board, UserBoard, Element
from django.contrib.auth.admin import UserAdmin


# --- Custom User Admin ---
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


# --- Inline for UserBoard (many-to-many relationship between User and Board) ---
class UserBoardInline(admin.TabularInline):
    model = UserBoard
    extra = 1  # Number of empty rows to display by default


# --- Board Admin ---
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")
    inlines = [UserBoardInline]  # Only UserBoardInline here


# --- Element Admin ---
@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("id", "board", "type", "x", "y", "w", "h", "order")
    list_filter = ("board", "type")  # Filter by board and type
    search_fields = ("id", "content")
    ordering = ["board", "order"]  # Order elements by board and their order field


# --- UserBoard Admin ---
@admin.register(UserBoard)
class UserBoardAdmin(admin.ModelAdmin):
    list_display = ("user", "board", "order")
    list_filter = ("user", "board")
    ordering = ("order",)

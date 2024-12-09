from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.display_new_entry_form, name="display_new_entry_form"),
    path("new/create", views.create_new_entry, name="create_new_entry"),
    path("random", views.random_entry, name="random_entry"),
    path("<str:entry_name>/edit_entry", views.edit_entry, name="edit_entry"),
    path("<str:entry_name>/edit", views.edit_display, name="edit_display"),
    path("<str:entry_name>", views.entry_page, name="entry_page")
]

from django.urls import path, re_path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    # added the wiki/ to get a similar route trail as instructed in assignment

    path("wiki/<str:title>", views.singlepage, name="singlepage"),
    path("editEntry/<str:title>", views.editEntry, name="editEntry"),
    # In once tried to re_path and regex my way to the editEntry page from singlepage
    #
    # re_path(r'^editEntry/(?P<slug>[\w-])', views.editEntry, name="editEntry"),
    path("randomPage", views.randomPage, name= "randomPage"),
    path("NewEntry", views.NewPage, name="NewPage")
    
    # path("wiki/search", views.search, name="search")
]

from django.urls import path
from . import views


app_name = 'books'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('datatables/books', views.BooksDataTablesView.as_view(), name='books_datatables'),
    path('editor/books', views.BooksEditorView.as_view(), name='books_editor'),   
]

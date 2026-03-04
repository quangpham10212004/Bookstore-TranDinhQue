from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('book/<int:book_id>/review/', views.add_review_view, name='add_review'),
    path('category/<int:category_id>/', views.category_books_view, name='category_books'),
]

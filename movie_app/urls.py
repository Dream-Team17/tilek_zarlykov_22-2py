from django.urls import path
from movie_app.views import movies_view, movie_detail_view, directors_view, director_detail_view, reviews_view, review_detail_view

urlpatterns = [
    path('movies', movies_view),
    path('movies/<int:id>/', movie_detail_view),
    path('directors/', directors_view),
    path('directors/<int:id>/', director_detail_view),
    path('reviews/', reviews_view),
    path('reviews/<int:id>/', review_detail_view),
]


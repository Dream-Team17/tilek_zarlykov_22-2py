from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Movie, Director, Review
from movie_app.serializers import (MovieSerializer,
                                   DirectorSerializer,
                                   ReviewSerializer,
                                   MovieReviewSerializer,
                                   MovieCreateSerializer,
                                   MovieUpdateSerializer,
                                   DirectorValidateSerializer,
                                   DirectorUpdateSerializer,
                                   ReviewValidateSerializer)
from rest_framework import status
# Create your views here.

@api_view(['GET', 'POST'])
def movies_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = MovieCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"errors": serializer.errors})
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director = serializer.validated_data.get('director')
        movie = Movie.objects.create(title=title, description=description, duration=duration, director_id=director)

        return Response(data={'message':'Data recieved',
                              'movie': MovieSerializer(movie).data},
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, **kwargs):
    try:
        movie = Movie.objects.get(id=kwargs["id"])
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"message": "Movie not found!"})
    if request.method == 'GET':
        serializer = MovieSerializer(movie, many=False)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data={"message": "Movie was deleted"},
                        status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = MovieUpdateSerializer(data=request.data,
                                           context={"id": movie.id})
        serializer.is_valid(raise_exception=True)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director')
        movie.save()
        return Response(data={"message": "Data were changed!",
                         'movie': MovieSerializer(movie).data},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def directors_view(request, **kwargs):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(data=serializer.data)
    elif request.method == "POST":
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        director = Director.objects.create(name=name)
        return Response({"message": "Director was created!",
                         'director': DirectorSerializer(director).data},
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, **kwargs):
    try:
        director = Director.objects.get(id=kwargs["id"])
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"message": "Director not found!"})
    if request.method == 'GET':
        director = Director.objects.get(id=kwargs['id'])
        serializer = DirectorSerializer(director, many=False)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(data={"message": "Director was deleted!"},
                        status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = DirectorValidateSerializer(data=request.data,
                                                context={"id": director.id})
        serializer.is_valid(raise_exception=True)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data={"message": "Director was changed!",
                              "director": DirectorSerializer(director).data},
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def reviews_view(request, **kwargs):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.get('text')
        movie = serializer.validated_data.get('movie')
        review = Review.objects.create(text=text, movie_id=movie)
        return Response(data={"message": "Review was created!",
                         "review": ReviewSerializer(review).data},
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, **kwargs):
    try:
        review = Review.objects.get(id=kwargs['id'])
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"message": "Review not found!"})
    if request.method == 'GET':
        review = Review.objects.get(id=kwargs['id'])
        serializer = ReviewSerializer(review, many=False)
        return Response(data=serializer.data)
    elif request.method =='DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Review was deleted!"})
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.movie_id = serializer.validated_data.get('movie')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={"message": "Review was changed!",
                              "review": ReviewSerializer(review).data})

@api_view(['GET'])
def movies_reviews_view(request):
    if request.method == 'GET':
        movie = Movie.objects.all()

        serializer = MovieReviewSerializer(movie, many=True)
        return Response(data=serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Movie, Director, Review
from movie_app.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, MovieReviewSerializer
from rest_framework import status
# Create your views here.

@api_view(['GET', 'POST'])
def movies_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director = request.data.get('director')
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
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director')
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
        name = request.data.get('name')
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
        director.name = request.data.get('name')
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
        text = request.data.get('text')
        movie = request.data.get('movie')
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
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie')
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

from rest_framework import serializers
from movie_app.models import Movie, Director, Review

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'director', 'duration', )

class DirectorSerializer(serializers.ModelSerializer):
    count_movie = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ('id', 'name', 'count_movie')

    def get_count_movie(self, directors):
        r = directors.movie.all()
        return len(r)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'movie', 'grade')

class ReviewStrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text')

class MovieReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewStrSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('title', 'reviews', 'rating')

    def get_rating(self, movie):
        r = [review.grade for review in movie.reviews.all()]
        return sum(r) / len(r) if r else None


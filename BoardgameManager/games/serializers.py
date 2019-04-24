from rest_framework import serializers
from .models import BoardGame, BoardGameCategory, BoardGameMechanic, \
                    BoardGameFamily, BoardGameStatistics, BoardGameRank, \
                    BoardGamePlayerSuggestions, Collection, CollectionBoardGame
from django.contrib.auth.models import User

class BoardGameCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardGameCategory
        fields = ['name']


class BoardGameMechanicSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardGameMechanic
        fields = ['name']

class BoardGameFamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardGameFamily
        fields = ['name']


class BoardGameRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardGameRank
        fields = ['subtype', 'rank']


class BoardGameStatisticsSerializer(serializers.ModelSerializer):

    sub_ranks = BoardGameRankSerializer(many=True)

    class Meta:
        model = BoardGameStatistics
        fields = ['num_ratings', 'avg_rating', 'bayesian_avg_rating', 'avg_weight', 'rank', 'sub_ranks']

class BoardGamePlayerSuggestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardGamePlayerSuggestions
        fields = ['recommended', 'best']

class BoardGameSerializer(serializers.ModelSerializer):

    categories = BoardGameCategorySerializer(many=True)
    mechanics = BoardGameMechanicSerializer(many=True)
    families = BoardGameFamilySerializer(many=True)
    statistics = BoardGameStatisticsSerializer(required=True)
    player_suggestions = BoardGamePlayerSuggestionsSerializer(required=True)

    class Meta:
        model = BoardGame
        fields = ['bgg_id', 'image_link', 'thumbnail', 'name', 'description',
                  'year_published', 'min_players', 'max_players', 'play_time',
                  'min_play_time', 'max_play_time', 'is_expansion', 'categories',
                  'mechanics', 'families', 'statistics', 'player_suggestions']


class CollectionBoardGameSerializer(serializers.ModelSerializer):

    boardgame = BoardGameSerializer(required=True)

    class Meta:
        model = CollectionBoardGame
        fields = ['boardgame', 'num_plays', 'rating', 'date_purchased']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

class CollectionSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)
    boardgames = CollectionBoardGameSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['user', 'boardgames']


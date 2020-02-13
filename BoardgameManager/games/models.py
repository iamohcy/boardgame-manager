from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# https://boardgamegeek.com/xmlapi2/thing?id=266192&stats=1

# https://docs.djangoproject.com/en/1.7/ref/models/instances/#creating-objects
class BoardGameManager(models.Manager):

    def create_boardgame(self, bgg_game):

        # Create board game in database
        ddb_boardgame = self.create(
            bgg_id=bgg_game.id,
            name=bgg_game.name,
            image_link=bgg_game.image,
            thumbnail = bgg_game.thumbnail,
            description = bgg_game.description,
            year_published = bgg_game.year,
            min_players = bgg_game.min_players,
            max_players = bgg_game.max_players,
            play_time = bgg_game.playing_time,
            min_play_time = bgg_game.minplaytime,
            max_play_time = bgg_game.maxplaytime,
            is_expansion = bgg_game.expansion,
        )

        ddb_boardgame_stats = BoardGameStatistics.objects.create(
            boardgame = ddb_boardgame,
            num_ratings = bgg_game.users_rated,
            avg_rating = bgg_game.rating_average,
            avg_weight = bgg_game.stats["averageweight"],
            bayesian_avg_rating = bgg_game.rating_bayes_average,
            rank = bgg_game.bgg_rank,
        )

        # TODO CALCULATE PLAYER_SUGGESTIONS STATS
        player_suggestions_dict = {}
        bgg_player_suggestions = bgg_game.player_suggestions

        recommended = []
        best = []

        # If a game has more recommended/best votes than not recommended, then
        # it's recommended. If it has more best than recommended votes, it's best
        # at that player count
        for ps in bgg_player_suggestions:
            player_count = ps.numeric_player_count

            if (ps.recommended + ps.best) > ps.not_recommended:
                recommended.append(player_count)

                if ps.best > ps.recommended:
                    best.append(player_count)


        ddb_boardgame_player_suggestions = BoardGamePlayerSuggestions.objects.create(
            boardgame = ddb_boardgame,
            recommended = recommended,
            best = best,
        )

        # Create mechanic objects if they don't already exist, otherwise
        # just link them
        if bgg_game.mechanics:
            for mechanic_name in bgg_game.mechanics:
                try:
                    # Board game already in database
                    ddb_mechanic = BoardGameMechanic.objects.get(pk=mechanic_name)
                except:
                    ddb_mechanic = BoardGameMechanic.objects.create(
                        name = mechanic_name,
                    )
                ddb_boardgame.mechanics.add(ddb_mechanic)

        # Create categories objects if they don't already exist, otherwise
        # just link them
        if bgg_game.categories:
            for category_name in bgg_game.categories:
                try:
                    # Board game already in database
                    ddb_category = BoardGameCategory.objects.get(pk=category_name)
                except:
                    ddb_category = BoardGameCategory.objects.create(
                        name = category_name,
                    )
                ddb_boardgame.categories.add(ddb_category)

        # Create mechanic objects if they don't already exist, otherwise
        # just link them
        if bgg_game.families:
            for family_name in bgg_game.families:
                try:
                    # Board game already in database
                    ddb_family = BoardGameFamily.objects.get(pk=family_name)
                except:
                    print (family_name)
                    ddb_family = BoardGameFamily.objects.create(
                        name = family_name,
                    )
                ddb_boardgame.families.add(ddb_family)

        for bgg_rank in bgg_game.ranks:
            print("Creating bgg_rank of name " + bgg_rank.name)
            ddb_rank = BoardGameRank.objects.create(
                bg_stats = ddb_boardgame_stats,
                subtype = bgg_rank.name,
                rank = bgg_rank.value
            )

        return ddb_boardgame

class BoardGameCategory(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class BoardGameMechanic(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class BoardGameFamily(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

# Create your models here.
class BoardGame(models.Model):
    bgg_id = models.IntegerField(primary_key=True)

    image_link = models.URLField()
    thumbnail = models.URLField()
    name = models.TextField()

    description = models.TextField()
    year_published = models.IntegerField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    play_time = models.IntegerField()
    min_play_time = models.IntegerField()
    max_play_time = models.IntegerField()

    is_expansion = models.BooleanField(default=False)

    categories = models.ManyToManyField(BoardGameCategory)
    mechanics = models.ManyToManyField(BoardGameMechanic)
    families = models.ManyToManyField(BoardGameFamily)

    objects = BoardGameManager()

    def __str__(self):
        return self.name

class BoardGameStatistics(models.Model):
    boardgame = models.OneToOneField(BoardGame, on_delete=models.CASCADE, related_name='statistics')
    num_ratings = models.IntegerField()
    avg_rating = models.FloatField(null=True)
    avg_weight = models.FloatField(null=True)
    bayesian_avg_rating = models.FloatField(null=True)
    rank = models.IntegerField(null=True)

class BoardGamePlayerSuggestions(models.Model):
    boardgame = models.OneToOneField(BoardGame, on_delete=models.CASCADE, related_name='player_suggestions')
    recommended = ArrayField(models.IntegerField(blank=True))
    best = ArrayField(models.IntegerField(blank=True))

# TODO handle ranks
class BoardGameRank(models.Model):
    bg_stats = models.ForeignKey(BoardGameStatistics, on_delete=models.CASCADE, related_name='sub_ranks')
    subtype = models.CharField(max_length=100)
    rank = models.IntegerField(null=True)

# Contains user rating and other details about a game
class Collection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # boardgames = models.ForeignKey(CollectionBoardGame)

class CollectionBoardGame(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='boardgames')
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    # name = models.TextField()
    num_plays = models.IntegerField()
    num_votes = models.IntegerField()
    rating = models.FloatField(null=True) # not all games will have been rated
    date_purchased = models.DateField(blank=True, null=True, verbose_name="Date of Purchase")


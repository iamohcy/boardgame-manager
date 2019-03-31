from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField

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
            bayesian_avg_rating = bgg_game.rating_bayes_average,
            rank = bgg_game.bgg_rank,
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
                ddb_mechanic.boardgames.add(ddb_boardgame)

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
                ddb_category.boardgames.add(ddb_boardgame)

        # Create mechanic objects if they don't already exist, otherwise
        # just link them
        if bgg_game.families:
            for family_name in bgg_game.families:
                try:
                    # Board game already in database
                    ddb_family = BoardGameFamily.objects.get(pk=family_name)
                except:
                    ddb_family = BoardGameFamily.objects.create(
                        name = family_name,
                    )
                ddb_family.boardgames.add(ddb_boardgame)

        for bgg_rank in bgg_game.ranks:
            print("Creating bgg_rank of name " + bgg_rank.name)
            ddb_rank = BoardGameRank.objects.create(
                bg_stats = ddb_boardgame_stats,
                subtype = bgg_rank.name,
                rank = bgg_rank.value
            )

        return ddb_boardgame

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
    boardgame_category = models.ManyToManyField('BoardGameCategory')
    boardgame_mechanic = models.ManyToManyField('BoardGameMechanic')
    boardgame_family = models.ManyToManyField('BoardGameFamily')

    is_expansion = models.BooleanField(default=False)

    objects = BoardGameManager()

    def __str__(self):
        return self.name

class BoardGameCategory(models.Model):
    boardgames = models.ManyToManyField(BoardGame)
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

class BoardGameMechanic(models.Model):
    boardgames = models.ManyToManyField(BoardGame)
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

class BoardGameFamily(models.Model):
    boardgames = models.ManyToManyField(BoardGame)
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

class BoardGameStatistics(models.Model):
    boardgame = models.OneToOneField(BoardGame, on_delete=models.CASCADE)
    num_ratings = models.IntegerField()
    avg_rating = models.FloatField(null=True)
    bayesian_avg_rating = models.FloatField(null=True)
    rank = models.IntegerField(null=True)

# TODO handle ranks
class BoardGameRank(models.Model):
    bg_stats = models.ForeignKey(BoardGameStatistics, on_delete=models.CASCADE)
    subtype = models.CharField(max_length=60)
    rank = models.IntegerField(null=True)

# Contains user rating and other details about a game
class Collection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # boardgames = models.ForeignKey(CollectionBoardGame)

class CollectionBoardGame(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    # name = models.TextField()
    num_plays = models.IntegerField()
    rating = models.FloatField(null=True) # not all games will have been rated
    date_purchased = models.DateField(blank=True, null=True, verbose_name="Date of Purchase")


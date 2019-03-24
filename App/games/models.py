from django.db import models
from django.contrib.auth.models import User

# https://boardgamegeek.com/xmlapi2/thing?id=266192&stats=1

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
    playing_time = models.IntegerField()
    minplay_time = models.IntegerField()
    maxplay_time = models.IntegerField()
    boardgame_category = models.ManyToManyField('BoardGameCategory')
    boardgame_mechanic = models.ManyToManyField('BoardGameMechanic')
    boardgame_family = models.ManyToManyField('BoardGameFamily')


    def __str__(self):
        return self.name

class BoardGameCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BoardGameMechanic(models.Model):
    mechanic_id = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BoardGameFamily(models.Model):
    family_id = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BoardGameStatistics(models.Model):

    board_game = models.OneToOneField(BoardGame, on_delete=models.CASCADE, primary_key=True)
    avg_rating = models.FloatField()
    bayesian_avg_rating = models.FloatField()
    rank = models.IntegerField()

class FamilyRank(models.Model):
    bg_stats = models.ForeignKey(BoardGameStatistics, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    rank = models.IntegerField()

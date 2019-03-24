from django.db import models
from django.contrib.auth.models import User
from games.models import BoardGame

# Create your models here.
class Profile(models.Model):
    # verification_code = models.CharField(max_length=60)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bgg_username = models.CharField(max_length = 30)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")

    # avatar = models.CharField(max_length = 255)
    # stats = models.OneToOneField(Stats)
    # level = models.IntegerField()
    # exp = models.IntegerField()

    def __unicode__(self):
        return self.user.username + ": " + self.contact_email

class Collection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    boardgames = models.ManyToManyField(BoardGame)

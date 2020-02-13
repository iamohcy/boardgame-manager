# Generated by Django 2.1.7 on 2020-02-13 16:20

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardGame',
            fields=[
                ('bgg_id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_link', models.URLField()),
                ('thumbnail', models.URLField()),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('year_published', models.IntegerField()),
                ('min_players', models.IntegerField()),
                ('max_players', models.IntegerField()),
                ('play_time', models.IntegerField()),
                ('min_play_time', models.IntegerField()),
                ('max_play_time', models.IntegerField()),
                ('is_expansion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BoardGameCategory',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BoardGameFamily',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BoardGameMechanic',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BoardGamePlayerSuggestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), size=None)),
                ('best', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), size=None)),
                ('boardgame', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player_suggestions', to='games.BoardGame')),
            ],
        ),
        migrations.CreateModel(
            name='BoardGameRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtype', models.CharField(max_length=100)),
                ('rank', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BoardGameStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_ratings', models.IntegerField()),
                ('avg_rating', models.FloatField(null=True)),
                ('avg_weight', models.FloatField(null=True)),
                ('bayesian_avg_rating', models.FloatField(null=True)),
                ('rank', models.IntegerField(null=True)),
                ('boardgame', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='games.BoardGame')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionBoardGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_plays', models.IntegerField()),
                ('num_votes', models.IntegerField()),
                ('rating', models.FloatField(null=True)),
                ('date_purchased', models.DateField(blank=True, null=True, verbose_name='Date of Purchase')),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.BoardGame')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boardgames', to='games.Collection')),
            ],
        ),
        migrations.AddField(
            model_name='boardgamerank',
            name='bg_stats',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_ranks', to='games.BoardGameStatistics'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='categories',
            field=models.ManyToManyField(to='games.BoardGameCategory'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='families',
            field=models.ManyToManyField(to='games.BoardGameFamily'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='mechanics',
            field=models.ManyToManyField(to='games.BoardGameMechanic'),
        ),
    ]

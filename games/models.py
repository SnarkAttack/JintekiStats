from __future__ import unicode_literals

from django.db import models

class GameManager(models.Manager):
    def store_game(self, runner_name, runner_id, runner_score, corp_name, corp_id, corp_score, winner, win_type, game_date, exact_match):
        game = self.get_or_create(runner_name=runner_name, runner_id=runner_id, runner_score=runner_score,
                                    corp_name=corp_name, corp_id=corp_id, corp_score=corp_score, winner=winner,
                                    win_type=win_type, game_date=game_date, exact_match=exact_match)
        return game

# Create your models here.
class Game(models.Model):
    runner_name = models.CharField(max_length=32, default=None, null=True)
    runner_id = models.IntegerField(default=0)
    runner_score = models.IntegerField(default=0)
    corp_name = models.CharField(max_length=32, default=None, null=True)
    corp_id = models.IntegerField(default=0)
    corp_score = models.IntegerField(default=0)
    winner = models.BooleanField(default=True)
    win_type = models.IntegerField(default=0)
    game_date = models.DateTimeField('date played')
    exact_match = models.IntegerField(default=1)

    objects = GameManager()

class IdentityManager(models.Manager):
    def register_id(self, code, title, faction_code, side_code):
        identity = self.get_or_create(code=code, title=title, faction_code=faction_code, side_code=side_code)
        return identity

class Identity(models.Model):
    code = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=128)
    faction_code = models.CharField(max_length=32)
    side_code = models.CharField(max_length=6)

    objects = IdentityManager()

class JintekiUsernameManager(models.Manager):
    def register_username(self, jinteki_username, site_username):
        new_username = self.get_or_create(jinteki_username=jinteki_username, site_username=site_username)
        return new_username

class JintekiUsername(models.Model):
    jinteki_username = models.CharField(max_length=32)
    site_username = models.CharField(max_length=32)

    objects = JintekiUsernameManager()

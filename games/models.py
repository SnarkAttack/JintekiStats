from __future__ import unicode_literals

from django.db import models

class GameManager(models.Manager):
    def store_game(self, player_side, runner_id, runner_score, corp_id, corp_score, winner, win_type, game_date, online, exact_match):
        game = self.get_or_create(player_side=player_side, runner_id=runner_id, runner_score=runner_score,
                                    corp_id=corp_id, corp_score=corp_score, winner=winner,
                                    win_type=win_type, game_date=game_date, online=online, exact_match=exact_match)
        return game

class PlayerGameManager(models.Manager):
    def store_game(self, player_side, player_id, player_score, opp_id, opp_score, winner, win_type, game_date, online, exact_match):
        game = self.get_or_create(player_side=player_side, runner_id=runner_id, runner_score=runner_score,
                                    corp_id=corp_id, corp_score=corp_score, winner=winner,
                                    win_type=win_type, game_date=game_date, online=online, exact_match=exact_match)
        return game

# Create your models here.
class Game(models.Model):
    player_side = models.BooleanField(default=True)
    runner_id = models.IntegerField(default=0)
    runner_score = models.IntegerField(default=0)
    corp_id = models.IntegerField(default=0)
    corp_score = models.IntegerField(default=0)
    winner = models.BooleanField(default=True)
    win_type = models.IntegerField(default=0)
    game_date = models.DateField('date played')
    online = models.BooleanField(default=False)
    exact_match = models.IntegerField(default=1)

    objects = GameManager()

class PlayerGame(models.Model):
    player_side = models.BooleanField(default=True)
    player_id = models.IntegerField(default=0)
    player_score = models.IntegerField(default=0)
    opp_id = models.IntegerField(default=0)
    opp_score = models.IntegerField(default=0)
    winner = models.BooleanField(default=True)
    win_type = models.IntegerField(default=0)
    game_date = models.DateTimeField('date played')
    online = models.BooleanField(default=False)
    exact_match = models.IntegerField(default=1)

    objects = PlayerGameManager()

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

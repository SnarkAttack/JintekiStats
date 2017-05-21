from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
from django.urls import reverse
from django.utils import timezone
import urllib2
import json
import datetime
import pytz
from tzlocal import get_localzone
import re

from ..models import Game
from ..forms import GameLogForm, GameLogJintekiTextForm

class GameLogger(View):

    def post(self, request):
        data = request.POST
        print data
        winner = True if data['winner'] == 'True' else False
        runner_name = request.user.username if data['player_side'] == 'True' else data['opponent_username']
        corp_name = data['opponent_username'] if data['player_side'] == 'True' else request.user.username

        (game, created) = Game.objects.store_game(
                win_type=int(data['win_type']),
                winner=winner,
                corp_id=int(data['corp_id']),
                runner_name=runner_name,
                corp_score=int(data['corp_score']),
                runner_id=int(data['runner_id']),
                runner_score=int(data['runner_score']),
                game_date=datetime.datetime.now(),
                corp_name=corp_name,
                #online=online,
                exact_match=1
        )
        if created:
            game.save()
            return HttpResponseRedirect(reverse("games:list_games"))
        else:
            (retry_game, retry_created) = Game.objects.store_game(
                    win_type=int(data['win_type']),
                    winner=winner,
                    corp_id=int(data['corp_id']),
                    runner_name=runner_name,
                    corp_score=int(data['corp_score']),
                    runner_id=int(data['runner_id']),
                    runner_score=int(data['runner_score']),
                    game_date=datetime.datetime.now(),
                    corp_name=corp_name,
                    #online=online,
                    exact_match=game.exact_match+1
            )
            if retry_created:
                game.save()
                return HttpResponseRedirect(reverse("games:list_games"))
            else:
                return HttpResponseRedirect(reverse("games:list_games"))

@login_required(login_url=settings.LOGIN_URL)
def record_game(request):
    # get_ids()
    game_log_form = GameLogForm()
    game_log_jinteki_text_form = GameLogJintekiTextForm()
    context = {'game_log_form': game_log_form, 'game_log_jinteki_text_form': game_log_jinteki_text_form}
    return render(request, 'games/record_game.html', context)

class GameLoggerFullText(View):

    def post(self, request):
        data = request.POST

        stats = gather_stats(data['full_text'])

        (game, created) = Game.objects.store_game(
                win_type=int(stats['win_type']),
                winner=stats['winner'],
                corp_id=int(data['corp_id']),
                runner_name=stats['runner_name'],
                corp_score=int(stats['corp_score']),
                runner_id=int(data['runner_id']),
                runner_score=int(stats['runner_score']),
                game_date=datetime.datetime.now(),
                corp_name=stats['corp_name'],
                runner_credits = stats['runner_click_for_credit'],
                corp_credits = stats['corp_click_for_credit'],
                runner_draws = stats['runner_draws'],
                corp_draws = stats['corp_draws'],
                runner_installs = stats['installed_run'],
                corp_installs = stats['installed_corp'],
                runner_mulligan = stats['runner_mulligan'],
                corp_mulligan = stats['corp_mulligan'],
                runs = stats['runs'],
                turns = stats['turns'],
                deck_name = data['deck_name'],
                #online=online,
                exact_match=1
        )
        if created:
            game.save()
            return HttpResponseRedirect(reverse("games:list_games"))
        else:
            (retry_game, retry_created) = Game.objects.store_game(
                    win_type=int(stats['win_type']),
                    winner=stats['winner'],
                    corp_id=int(data['corp_id']),
                    runner_name=stats['runner_name'],
                    corp_score=int(stats['corp_score']),
                    runner_id=int(data['runner_id']),
                    runner_score=int(stats['runner_score']),
                    game_date=datetime.datetime.now(),
                    corp_name=stats['corp_name'],
                    runner_credits = stats['runner_click_for_credit'],
                    corp_credits = stats['corp_click_for_credit'],
                    runner_draws = stats['runner_draws'],
                    corp_draws = stats['corp_draws'],
                    runner_installs = stats['installed_run'],
                    corp_installs = stats['installed_corp'],
                    runner_mulligan = stats['runner_mulligan'],
                    corp_mulligan = stats['corp_mulligan'],
                    runs = stats['runs'],
                    turns = stats['turns'],
                    deck_name = data['deck_name'],
                    #online=online,
                    exact_match=game.exact_match+1
            )
            if retry_created:
                game.save()
                return HttpResponseRedirect(reverse("games:list_games"))
            else:
                return HttpResponseRedirect(reverse("games:list_games"))


def scoring_action(line):
    if "scores" in line or "steals" in line or ("as an agenda" in line and "force" not in line):
        return True
    else:
        return False

def gather_stats(game_log):

    stats = {'corp_name': "", 'runner_name': "", 'runner_click_for_credit': 0,
                'runner_draws': 0, 'runner_played': {}, 'corp_played': {}, 'installed_run': 0,
                'installed_corp': 0, 'corp_click_for_credit': 0, 'corp_uses': {}, 'corp_draws': 0,
                'runner_score': 0, 'corp_score': 0, 'runner_agendas': {},
                'corp_agendas': {}, 'runner_uses': {}, 'pumps': {}, 'endTurn': {},
                'runs': 0, "ICE": {}, 'server': {}, 'rez': {}, 'advanceCount': 0, 'winner': None,
                "turns": 0, 'win_type': -1, 'runner_mullgan': True, 'corp_mulligan': True}

    game_text = []
    for line in game_log.split('\n'):
        #if playerName in line or scoring_action(line) or "wins the game" in line:
        game_text.append(line.rstrip())
        if "wins the game" in line:
            break

        (runner_name, corp_name, runner_mulligan, corp_mulligan) = getPlayers(game_text)

    return getStats(game_text, runner_name, corp_name, runner_mulligan, corp_mulligan, stats)

def getPlayers(game_text):
    corp_name = ""
    runner_name = ""
    corp_mulligan = False
    runner_mulligan = False
    for line in game_text:
        if 'takes a mulligan.' in line:
            if corp_name is "":
                corp_name = line[:-len(' takes a mulligan.')]
                corp_mulligan = True
            else:
                runner_name = line[:-len(' takes a mulligan.')]
                runner_mulligan = True
                break
        elif 'keeps their hand.' in line:
            if corp_name is "":
                corp_name = line[:-len(' keeps their hand.')]
            else:
                runner_name = line[:-len(' keeps their hand.')]
                break

    return (runner_name, corp_name, runner_mulligan, corp_mulligan)

def getStats(game_text, runner_name, corp_name, runner_mulligan, corp_mulligan, stats):
    stats['runner_name'] = runner_name
    stats['corp_name'] = corp_name
    stats['runner_mulligan'] = runner_mulligan
    stats['corp_mulligan'] = corp_mulligan
    for line in game_text:
        if line.startswith("!"):
            continue
        if "spends  to gain 1 ." in line:
            if runner_name in line:
                stats['runner_click_for_credit'] = stats.get('runner_click_for_credit', 0) + 1
            else:
                stats['corp_click_for_credit'] = stats.get('corp_click_for_credit', 0) + 1
        elif " spends  to draw " in line:
            if runner_name in line:
                stats['runner_draws'] = stats.get('runner_draws', 0) + 1
            else:
                stats['corp_draws'] = stats.get('corp_draws', 0) + 1
        elif "to install a card in" in line:
            #server = re.search(r'(ICE protecting|a card in) ([()&\w\s]+)\.$', line, re.UNICODE)
            #server_name = re.sub(r'\s\(new\sremote\)', '', server.group(2))
            stats['installed_corp'] = stats.get('installed_corp', 0) + 1
        elif "to install ICE protecting" in line:
            #server = re.search(r'(ICE protecting|a card in) ([()&\w\s]+)\.$', line, re.UNICODE)
            #server_name = re.sub(r'\s\(new\sremote\)', '', server.group(2))
            stats['installed_corp'] = stats.get('installed_corp', 0) + 1
        elif "to install " in line and "uses" not in line:
            print
            #card_name = re.search(r' to install ([&"\.\'!:\w\s-]+\.$)', line, re.UNICODE)
            stats['installed_run'] = stats.get('installed_run', 0) + 1
        # elif 'uses' in line or 'to use' in line:
        #     print line
        #     if runner_name in line:
        #         card_name = re.search(r' (uses|to use) ([&"\.\'!:\w\s-]+?) to', line, re.UNICODE)
        #         stats['runner_uses'][card_name.group(2)] = stats['runner_uses'].get(card_name.group(2), 0) + 1
        #     else:
        #         card_name = re.search(r' (uses|to use) ([&"\.\'!:\w\s-]+?) to', line, re.UNICODE)
        #         stats['corp_uses'][card_name.group(2)] = stats['corp_uses'].get(card_name.group(2), 0) + 1
        # elif 'increase the strength of' in line:
        #     card_name = re.search(r'(increase the strength) of ([&"\'!:\w\s-]+?) to', line, re.UNICODE)
        #     stats['pumps'][card_name.group(2)] = stats['pumps'].get(card_name.group(2), 0) + 1
        # elif " to play " in line or " plays " in line :
        #     if runner_name in line:
        #         card_name = re.search(r' (to play|plays) ([&"\.\'!:\w\s-]+)\.$', line, re.UNICODE)
        #         stats['runner_played'][card_name.group(2)] = stats['runner_played'].get(card_name.group(2), 0) + 1
        #     else:
        #         card_name = re.search(r' (to play|plays) ([&"\.\'!:\w\s-]+)\.$', line, re.UNICODE)
        #         stats['corp_played'][card_name.group(2)] = stats['corp_played'].get(card_name.group(2), 0) + 1
        # elif 'rezzes' in line or 'to rez' in line:
        #     card_name = re.search(r'(rezzes|to rez) ([&"\.\'!:\w\s-]+)\.$', line, re.UNICODE)
        #     stats['rez'][card_name.group(2)] = stats['rez'].get(card_name.group(2), 0) + 1
        elif "started their turn" in line:
            run_count = re.search(r'started their turn ([\d]+)', line, re.UNICODE)
            stats['turns'] = int(run_count.group(1))
        elif "to make a run" in line:
            #run_info = re.search(r'(to make a) run on ([&\w\s]+)', line, re.UNICODE)
            stats['runs'] = stats.get('runs', 0) + 1
        elif scoring_action(line):
            if runner_name in line:
                point_value = re.search(r' (scores|steals) ([&"\'!:\w\s-]+) and gains ([\d]+) agenda point', line, re.UNICODE)
                if point_value is None:
                    point_value = re.search(r'(adds) ([&"\'!:\w\s-]+) to their score area as an agenda worth ([\d-]+) agenda point', line, re.UNICODE)
                stats['runner_score'] += int(point_value.group(3))
                stats['runner_agendas'][point_value.group(2)] = stats['runner_agendas'].get(point_value.group(2), 0) + 1
                if stats['runner_agendas'] >= 7:
                    stats['winner'] = True
                    stats['win_type'] = 0
            else:
                point_value = re.search(r' (scores|steals) ([&"\'!:\w\s-]+) and gains ([\d]+) agenda point', line, re.UNICODE)
                if point_value is None:
                    point_value = re.search(r'(adds) ([&"\'!:\w\s-]+) to their score area as an agenda worth ([\d-]+) agenda point', line, re.UNICODE)
                stats['corp_score'] += int(point_value.group(3))
                stats['corp_agendas'][point_value.group(2)] = stats['corp_agendas'].get(point_value.group(2), 0) + 1
                if stats['corp_agendas'] >= 7:
                    stats['winner'] = False
                    stats['win_type'] = 0
        elif 'flatlined' in line:
            stats['winner'] = False
            stats['win_type'] = 1
        elif 'is decked' in line:
            stats['winner'] = True
            stats['win_type'] = 2
        elif 'concedes' in line:
            if runner_name in line:
                stats['winner'] = False
            else:
                stats['winner'] = True
            stats['win_type'] = 3
        else:
            continue

    return stats

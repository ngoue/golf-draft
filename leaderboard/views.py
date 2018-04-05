from django.shortcuts import render
from . import models
import requests, json

# Create your views here.
def index(request):
    players = load_players()
    drafters = models.Drafter.objects.all()

    for d in drafters:
        d.players = filter(lambda p: p.id == d.player1 or p.id == d.player2 or p.id == d.player3, players)
        d.players = sorted(d.players, key=lambda p: (p.to_par_error, not p.position, p.to_par_i))
        d.score = sum([ p.to_par_i for p in d.players[:-1] ])
        d.score_error = bool(list(filter(lambda p: p.to_par_error, d.players[:-1])))

    drafters = sorted(drafters, key=lambda d: (d.score_error, d.score))

    return render(request, 'index.html', {'drafters': drafters})


def load_players():
    raw_list = requests.get('http://www.masters.com/en_US/scores/feeds/scores.json').json().get("data", {}).get("player", [])
    players = []
    for player_data in raw_list:
        players.append(Player(player_data))
    return players


def sort_players(players):
    players = sorted(players, key=lambda p: p.to_par_error)
    players = sorted(players, key=lambda p: not p.position)
    players = sorted(players, key=lambda p: p.to_par_i)
    return players


class Player:
    def __init__(self, data):
        self.id = int(data["id"])
        self.image_id = str(self.id).zfill(5)
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.position = data["pos"]
        self.status = data["status"]
        self.to_par_s = data["topar"]
        self.to_par_error = False
        self.total_error = False
        try:
            self.to_par_i = int(data["topar"]) if data["topar"].upper() != "E" else 0
            # Double it if the player was cut... That way the score accounts for four rounds instead of two
            if self.status == "C":
                self.to_par_i *= 2
                self.to_par_s = "{}{}".format('+' if self.to_par_i > 0 else '', self.to_par_i if self.to_par_i != 0 else 'E')
        except ValueError:
            self.to_par_i = 0
            self.to_par_error = True
        try:
            self.total = int(data["total"]) if data["total"] != "" else 0
        except ValueError:
            self.total = 0
            self.total_error = True

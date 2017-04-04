from django.shortcuts import render
from . import models
import requests, json

# Create your views here.
def index(request):
    players = load_players()
    drafters = models.Drafter.objects.all()

    for d in drafters:
        d.players = filter(lambda p: p.id == d.player1 or p.id == d.player2 or p.id == d.player3, players)
        d.players = sorted(d.players, key=lambda p: p.to_par_i)
        d.score = sum([ p.to_par_i for p in d.players[:-1] ])

    drafters = sorted(drafters, key=lambda d: d.score)

    return render(request, 'index.html', {'drafters': drafters})


def load_players():
    raw_list = json.loads(requests.get('http://www.usopen.com/en_US/scores/feeds/scores.json').text)["data"]["player"]
    players = []
    for player_data in raw_list:
        players.append(Player(player_data))
    return players


class Player:
    def __init__(self, data):
        self.id = int(data["id"])
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.position = data["pos"]
        self.status = data["status"]
        self.to_par_s = data["topar"]
        try:
            self.to_par_i = int(data["topar"]) if data["topar"].upper() != "E" else 0
            # Double it if the player was cut... That way the score accounts for four rounds instead of two
            if self.status == "C":
                self.to_par_i *= 2
                self.to_par_s = "{}{}".format('+' if self.to_par_i > 0 else '', self.to_par_i if self.to_par_i != 0 else 'E')
        except ValueError:
            self.to_par_i = -999
        try:
            self.total = int(data["total"]) if data["total"] != "" else 0
        except ValueError:
            self.total = -999

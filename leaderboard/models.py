from django.db import models

# Create your models here.
class Drafter(models.Model):
    name = models.CharField(max_length=250)
    player1 = models.IntegerField()
    player2 = models.IntegerField()
    player3 = models.IntegerField()

    def __str__(self):
        return self.name

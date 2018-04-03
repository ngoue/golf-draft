from django.db import models

# Create your models here.
class Drafter(models.Model):
    name = models.CharField(max_length=250)
    player1 = models.IntegerField(blank=True, null=True)
    player2 = models.IntegerField(blank=True, null=True)
    player3 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

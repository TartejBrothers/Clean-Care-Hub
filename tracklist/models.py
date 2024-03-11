from django.db import models


class Tracklist(models.Model):
    email = models.EmailField()
    description = models.CharField(max_length=1000)
    deadline = models.DateTimeField()

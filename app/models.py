from django.db import models

# Create your models here.
class Entry(models.Model):
    source_id = models.CharField(max_length=70,  primary_key=True)
    time = models.CharField(max_length=30)
    viewers = models.IntegerField()
    name_id = models.CharField(max_length=40)
    name_display = models.CharField(max_length=40)
    source = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    preview = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    status = models.IntegerField()

    def __str__(self):
        return self.source_id

class Game_table(models.Model):
    source_id_game = models.CharField(max_length=100,  primary_key=True)
    entry = models.ManyToManyField(Entry, blank=True, related_name='Game_table')
    game = models.CharField(max_length=40)

    def __str__(self):
        return self.source_id_game

class Language_table(models.Model):
    source_id_language = models.CharField(max_length=100,  primary_key=True)
    entry = models.ManyToManyField(Entry, blank=True, related_name='Language_table')
    language = models.CharField(max_length=30)

    def __str__(self):
        return self.source_id_language

class Favorites_table(models.Model):
    prefix = 'favorites'
    source_id_user = models.CharField(max_length=100,  primary_key=True)
    source_id = models.CharField(max_length=80)
    entry = models.ManyToManyField(Entry, blank=True, related_name='Favorites_table')
    user = models.CharField(max_length=30)

    def __str__(self):
        return self.source_id_user

class Recent_table(models.Model):
    prefix = 'recent'
    source_id_user = models.CharField(max_length=100,  primary_key=True)
    source_id = models.CharField(max_length=80)
    entry = models.ManyToManyField(Entry, blank=True, related_name='Recent_table')
    user = models.CharField(max_length=30)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.source_id_user


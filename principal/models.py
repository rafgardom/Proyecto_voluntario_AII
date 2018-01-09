from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    user_name = models.CharField("Nombre de usuario", unique=True, max_length= 20)
    name = models.CharField(max_length= 100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    address = models.CharField(max_length=300)

    #Relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_notices = models.ManyToManyField("Noticia")
    favourite_teams = models.ManyToManyField("Equipo")
    friends = models.ForeignKey("Usuario", null=True)

    def __unicode__(self):
        return self.user_name

class Noticia(models.Model):
    title = models.CharField(max_length= 100)
    body = models.TextField()
    moment = models.DateTimeField()
    url = models.TextField()

    def __unicode__(self):
        return self.url

class Equipo(models.Model):
    name = models.CharField(max_length= 100)
    image = models.TextField()
    country = models.CharField(max_length= 100)

    #Relationships
    sport = models.ForeignKey("Deporte", on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

class Deporte(models.Model):
    name = models.CharField(max_length= 100, unique=True)

    def __unicode__(self):
        return self.name
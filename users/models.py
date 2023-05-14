
from django.db import models
from django.db.models import TextChoices


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class UserRoles(TextChoices):
    MEMBER = "member", "Пользователь"
    ADMIN = "admin", "Админ"
    MODERATOR = "moderator", "Модератор"


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    age = models.PositiveIntegerField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username

    def serialize(self):
        return {
        'id' : self.id,
        'username' : self.username,
        'first_name' : self.first_name,
        'last_name' : self.last_name,
        'age' : self.age,
        'locations': [loc.name for loc in self.locations.all()],
        'role' : self.role
        }

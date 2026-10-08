from django.db import models
from django.contrib.auth.models import User


class Dealer(models.Model):
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    zip = models.CharField(max_length=20)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    def __str__(self):
        return self.full_name


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="models"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.make.name} {self.name}"


class Review(models.Model):
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    review = models.TextField()
    sentiment = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dealer.full_name} - {self.user.username}"

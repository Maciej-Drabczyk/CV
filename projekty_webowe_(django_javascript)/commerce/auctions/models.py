from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image_url = models.CharField(max_length=200)
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    date = models.DateTimeField()
    category = models.CharField(max_length=50)
    watchlisted_by = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title} of {self.owner}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    offer = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.owner} on {self.listing}: {self.offer}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=100)
    date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.owner} on {self.listing}"
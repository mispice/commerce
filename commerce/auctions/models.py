from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class auctionlisting(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.FloatField()
    Product_Image = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    auctionlisting = models.ForeignKey(auctionlisting,on_delete=models.CASCADE,related_name="watchlist")

class listing_comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    auctionlisting = models.ForeignKey(auctionlisting,on_delete=models.CASCADE,related_name="comment")
    comment = models.CharField(max_length = 500)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}:{self.comment} on {self.date_created}" 

class bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    auctionlisting = models.ForeignKey(auctionlisting,on_delete =  models.CASCADE, related_name="bid")
    bid= models.FloatField()
    highestbid = models.BooleanField(default = False)
    winningbid = models.BooleanField(default = False)

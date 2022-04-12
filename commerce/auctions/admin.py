from django.contrib import admin

from .models import auctionlisting,User,watchlist,listing_comment,bid
# Register your models here.

admin.site.register(auctionlisting)
admin.site.register(User)
admin.site.register(watchlist)
admin.site.register(listing_comment)
admin.site.register(bid)
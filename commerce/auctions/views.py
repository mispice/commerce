from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import User,auctionlisting,bid,watchlist,listing_comment
from django.db.models import Q


def index(request):
    if request.user.is_authenticated:
        currentbid = bid.objects.all()
        for a_bid in currentbid:
            if a_bid.winningbid == True:
                closed_listing_id = a_bid.auctionlisting.id
        auction_listing = auctionlisting.objects.exclude(user = request.user).exclude(pk= int(closed_listing_id))
    else:
        currentbid = bid.objects.all()
        for a_bid in currentbid:
            if a_bid.winningbid == True:
                closed_listing_id = a_bid.auctionlisting.id
        auction_listing = auctionlisting.objects.exclude(pk=int(closed_listing_id))
    return render(request,"auctions/index.html",{
            "listings": auction_listing
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create_listing(request):
    if request.method =="POST":
        if request.POST.get('title') and request.POST.get('description') and request.POST.get('starting_bid') and request.POST.get('product_images') and request.POST.get('category'):
            auction_listing = auctionlisting()
            auction_listing.user = request.user
            auction_listing.title =request.POST.get('title')
            auction_listing.description =request.POST.get('description')
            auction_listing.starting_bid =float(request.POST.get('starting_bid'))
            auction_listing.product_images = request.POST.get('Product_Image')
            auction_listing.category =request.POST.get('category')
            auction_listing.save()
            return render(request,"auctions/create_listing.html",{
                "message": "Item Created Successfully"
            })
    return render(request,"auctions/create_listing.html",{
    })

@login_required(login_url="login")
def listing_page(request,listing_id):
    currentbids = bid.objects.all()
    auction_listing= auctionlisting.objects.get(pk=int(listing_id))
    comment = listing_comment.objects.filter(auctionlisting = auction_listing)
    for bidvalue in currentbids:
        if bidvalue.highestbid == True and bidvalue.auctionlisting.id == listing_id:
            highest_bid = bidvalue.bid
        else:
            highest_bid = 0
    if auctionlisting.objects.filter(id=listing_id).exists():
        listing = auctionlisting.objects.get(pk=int(listing_id))
        return render(request,"auctions/listing_page.html",{
        "listing":listing,
        "highestbid": highest_bid,
        "comments": comment
        })
    else:
        return render(request,"auctions/listing_page.html",{})

def watchlist_create(request,listing_id):
    listing = auctionlisting.objects.all()
    watch_list = watchlist()
    watch_list.user = request.user
    watch_list.auctionlisting = auctionlisting.objects.get(pk=int(listing_id))
    watch_list.save()
    return render(request,"watchlist.html",{
        "watch_list":listing
    })
@login_required(login_url="login")
def watchlist_display(request):
    watch_list = watchlist.objects.filter(user=request.user)
    return render(request,"auctions/watchlist.html",{
        "watch_list": watch_list
    })

def remove_watchlist(request,listing_id):
    watchlist_item = watchlist.objects.get(pk=int(listing_id))
    watchlist_item.delete()
    messages.success(request,"Item removed successfully")
    return HttpResponseRedirect(reverse("watchlist_display"))

def placebid(request,listing_id):
    if request.method == "POST":
        auction_listing = auctionlisting.objects.get(pk=int(listing_id))
        item_bid =  bid()
        currentbids = bid.objects.all()
        bid_item = float(request.POST['bid'])
        if bid_item > auction_listing.starting_bid and not currentbids:
            item_bid.user = request.user
            item_bid.bid = bid_item
            item_bid.auctionlisting = auctionlisting.objects.get(pk=int(listing_id))
            item_bid.highestbid = True
            item_bid.save()
            messages.success(request,'Bid Placed successfully')
            return HttpResponseRedirect(reverse("listing_page.html"))
        elif bid_item > auction_listing.starting_bid and currentbids:
            for item in currentbids:
                # print(item.bid)
                if item.highestbid == True:
                    if bid_item> item.bid:
                        item.highestbid= False
                        item_bid.user = request.user
                        item_bid.bid = bid_item
                        item_bid.auctionlisting = auctionlisting.objects.get(pk=int(listing_id))
                        item_bid.highestbid = True
                        item.save()
                        item_bid.save()
                        messages.success(request,'Bid Placed successfully')
                    elif bid_item < item.bid:
                        messages.warning(request,f'Place bid should be greater than {item.bid}')
                        return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": auction_listing.id}))
        elif bid_item < auction_listing.starting_bid:
            messages.warning(request,f'Placed bid should be greater than {auction_listing.starting_bid}')
            return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": auction_listing.id}))
    return HttpResponseRedirect(reverse("listing_page", args=[auction_listing.id]))     

@login_required(login_url="login")
def your_listings(request):
    auction_listing = auctionlisting.objects.filter(user = request.user)
    return render(request,"auctions/your_listings.html",{
        "listings": auction_listing
    })
def close_bid(request,listing_id):
    if request.method == "POST":
        currentbids = bid.objects.all()
        auction_listing = auctionlisting.objects.get(pk=int(listing_id))
        for a_bid in currentbids:
            if a_bid.highestbid == True and a_bid.auctionlisting.id == listing_id:
                a_bid.winningbid = True
                auction_listing.active = False
                a_bid.save()
                auction_listing.save()
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url ="login")
def notifications(request):
    wonbid = bid.objects.all()
    for bids in wonbid:
        if bids.winningbid == True and bids.user == request.user:
            notification = f"Congratulations you won the bid for {bids.auctionlisting.title}"
    return render(request,"auctions/notifications.html",{
        "notification": notification
    })

def comments(request,listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        auction_listing = auctionlisting.objects.get(pk=int(listing_id))
        listingcomment = listing_comment()
        listingcomment.user = request.user
        listingcomment.comment = comment
        listingcomment.auctionlisting = auction_listing
        print(auction_listing.title)
        listingcomment.save()
        messages.success(request, 'comment added successfully')
    return HttpResponseRedirect(reverse("listing_page", args=[auction_listing.id]))


def categories(request):
    if request.user.is_authenticated:
        currentbid = bid.objects.all()
        for a_bid in currentbid:
            if a_bid.winningbid == True:
                closed_listing_id = a_bid.auctionlisting.id
        auction_listing = auctionlisting.objects.exclude(user = request.user).exclude(pk= int(closed_listing_id))
    else:
        currentbid = bid.objects.all()
        for a_bid in currentbid:
            if a_bid.winningbid == True:
                closed_listing_id = a_bid.auctionlisting.id
        auction_listing = auctionlisting.objects.exclude(pk=int(closed_listing_id))
    return render(request,"auctions/categories.html",{
            "categories": auction_listing
    })

def categorical_listing(request):
    if request.method == "POST":
        category_pressed = request.POST["categorybutton"]
        if request.user.is_authenticated:
            currentbid = bid.objects.all()
            for a_bid in currentbid:
                if a_bid.winningbid == True:
                    closed_listing_id = a_bid.auctionlisting.id
            auction_listing = auctionlisting.objects.exclude(user = request.user).exclude(pk= int(closed_listing_id)).filter().exclude(~Q(category= category_pressed))
        else:
            currentbid = bid.objects.all()
            for a_bid in currentbid:
                if a_bid.winningbid == True:
                    closed_listing_id = a_bid.auctionlisting.id
            auction_listing = auctionlisting.objects.exclude(pk=int(closed_listing_id)).exclude(~Q(category= category_pressed))
        return render(request,"auctions/categorical_listing.html",{
            "listings": auction_listing
        })
    

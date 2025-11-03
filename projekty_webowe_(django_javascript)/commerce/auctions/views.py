from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
import datetime

from .models import User

class CreateForm(forms.Form):
    title = forms.CharField(label="Listing Title", max_length=100)
    description = forms.CharField(label="Listing Description", max_length=250)
    image_url = forms.CharField(label="Image URL", max_length=200)
    price = forms.FloatField(label="Starting price")
    category = forms.CharField(max_length=50)

class BidForm(forms.Form):
    bid = forms.IntegerField(label="Bid:")

class CommentForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":"2", "cols": "100"}), required=True)


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "filter": False
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
    
def create(request):
    # Creating new listing
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            url = form.cleaned_data["image_url"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            owner = request.user
            date = datetime.datetime.now()

            # Saving listing
            listing = Listing(title=title, description=description, image_url=url, price=price, owner=owner, date=date, category=category)
            listing.save()
            return render(request, "auctions/create.html", {
                "form": CreateForm()
            })

    return render(request, "auctions/create.html", {
        "form": CreateForm()
    })

def listing(request, id):
    # Checking if request method was 'POST'
    if request.method == "POST":
        # Check if bid was placed
        form_bid = BidForm(request.POST)
        if form_bid.is_valid():
            bid = form_bid.cleaned_data["bid"]
            listing = Listing.objects.filter(pk=id).first()

            # Check if bid was high enough
            if bid > listing.price:

                # Change price on a listing
                bidding = Bid(listing=listing, offer=bid, owner = request.user)
                bidding.save()
                listing.price = bid
                listing.save(update_fields=["price"])

        # Check if comment was created
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid():
            # Create comment and add it to the listing
            content = form_comment.cleaned_data["content"]
            listing = Listing.objects.filter(pk=id).first()
            owner = request.user
            date = datetime.datetime.now()
            comment = Comment(listing=listing, owner=owner, date=date, content=content)
            comment.save()

    # Dispaly listing details
    watchlisted = None
    if Listing.objects.filter(id=id).first():
        listing = Listing.objects.get(id=id)
        Bids_Quantity = listing.bids.count()

        # Check if user is logged and check if listing is watchlisted
        if request.user.is_authenticated:
            if listing.watchlisted_by.all().filter(pk=request.user.id).first():
                watchlisted = True
            else:
                watchlisted = False

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watchlisted": watchlisted,
                "bids": Bids_Quantity,
                "bidform": BidForm(),
                "commentForm": CommentForm()
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids": Bids_Quantity,
                "bidform": BidForm(),
                "commentForm": CommentForm()
            })
    return HttpResponseRedirect(reverse("index"))

def categories(request):
    # Creating list of categories based on all listings
    categories = {}
    listings = Listing.objects.all()
    for listing in listings:
        if listing.category in categories.keys():
            categories[listing.category] = categories[listing.category] + 1
        else:
            categories[listing.category] = 1
    return render(request, 'auctions/categories.html', {
        "list": categories
    })
    
def category(request, name):
    # Return listings that have certain category
    listings = Listing.objects.filter(category=name)
    return render(request, 'auctions/index.html', {
        "filter": True,
        "category": name,
        "listings": listings
    })

def watchlist(request):
    # If user is logged returns listings that are watchlisted
    if request.user.is_authenticated:
        listings = request.user.watchlist.all()
        return render(request, 'auctions/index.html', {
            "filter": False,
            "listings": listings,
            "watchlist": True
        })
    else:
        return HttpResponseRedirect(reverse("index"))
    
def watchlisting(request, id):
    # Change status of watchlisting listing
    if request.user.is_authenticated:
        if Listing.objects.filter(pk=id).first():
            listing = Listing.objects.get(pk=id)
            if listing.watchlisted_by.filter(pk=request.user.id).first():
                listing.watchlisted_by.remove(request.user)
            else:
                listing.watchlisted_by.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


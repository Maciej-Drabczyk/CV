from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post


def index(request):
    username = ""
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "network/index.html", {
        "value": username
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def new_post(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        content = data.get("content", "")
        post = Post(
            creator=user,
            content=content 
        )
        post.save()
        return JsonResponse({"message": "Post sent successfully."}, status=201)
    
def posts(request):
    posts = Post.objects.all()
    posts = posts.order_by("-date").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import User, Post


def index(request):
    posts = Post.objects.all()
    posts = posts.order_by('-date').all()
    if(request.user.is_authenticated):
        likes = request.user.liked.filter()
         
        likes = set()
        for post in posts:
            if request.user.liked.filter(id=post.id):
                likes.add(post.id)

        return render(request, "network/index.html", {
            "posts": [post.serialize() for post in posts],
            "likes": likes
        })
    return render(request, "network/index.html", {
        "posts": [post.serialize() for post in posts]
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


@login_required
@csrf_exempt
def new_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")
        new_post = Post(
            creator=request.user,
            content=content,
        )
        new_post.save()
        return JsonResponse({"message": "Posted successfully"})
    return HttpResponseRedirect(reverse('index'))

@login_required
@csrf_exempt
def like_toggle(request):
    if request.method == "POST":
        data = json.loads(request.body)
        toggle = data.get("toggle", False)
        post_id = data.get("id", 0)
        if(Post.objects.filter(id=post_id).first()):
            user = request.user
            post = Post.objects.filter(id=post_id).first()
            if(toggle):
                post.liked_by.add(user)
                return JsonResponse({
                    post.id: post.count_likes(),
                    "message": "Post successfully liked"})
            else:
                post.liked_by.remove(user)
                return JsonResponse({
                    post.id: post.count_likes(),
                    "message": "Post successfully disliked"})
        return JsonResponse({"message": "Error"})
    return JsonResponse({"message": "Error"})

def profile(request, name):
    if name == "":
        return HttpResponseRedirect(reverse('index'))
    if User.objects.filter(username=name).first():
        user = User.objects.get(username=name)
        user_posts = Post.objects.filter(creator=user).all()
        user_posts = user_posts.order_by('-date').all()
        if(request.user.is_authenticated):
            
            is_user_equal_profile = True
            if(request.user != user):
                is_user_equal_profile = False

            likes = set()
            for post in user_posts:
                if request.user.liked.filter(id=post.id):
                    likes.add(post.id)
                    
            return render(request, "network/profile.html", {
                "profile_followed": user.check_follow(request.user.username),
                "is_user_equal_profile": is_user_equal_profile,
                "id": user.id,
                "username": user.username,
                "followers_count": user.count_follows(),
                "followings_count": user.count_followings(),
                "posts": [post.serialize() for post in user_posts],
                "likes": likes
            })

        return render(request, "network/profile.html", {
            "id": user.id,
            "username": user.username,
            "followers_count": user.count_follows(),
            "followings_count": user.count_followings(),
            "posts": [post.serialize() for post in user_posts]
        })
    return HttpResponseRedirect(reverse('index'))

@login_required
@csrf_exempt
def follow_toggle(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile_name = data.get("profile", "")
        toggle = data.get("toggle", False)
        if(User.objects.filter(username=profile_name).first()):
            user = request.user
            profile = User.objects.filter(username=profile_name).first()
            if(toggle):
                profile.followers.add(user)
                return JsonResponse({
                    "count": profile.count_follows(),
                    "message": "Profile followed successfully"
                })
            else:
                profile.followers.remove(user)
                return JsonResponse({
                    "count": profile.count_follows(),
                    "message": "Profile unfollowed successfully"
                })
        return JsonResponse({"message": "Error"})
    return JsonResponse({"message": "Error"})

@login_required
def following(request):
    user = request.user
    followed = User.objects.filter(followers__id=user.id)
    followed_posts = Post.objects.filter(creator__in=followed).all()
    followed_posts = followed_posts.order_by('-date').all()
    likes = set()
    for post in followed_posts:
        if request.user.liked.filter(id=post.id):
            likes.add(post.id)
    return render(request, "network/following.html", {
        "posts": [post.serialize() for post in followed_posts],
        "likes": likes
    })

@login_required
@csrf_exempt
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get("post_id", 0)
        new_content = data.get("new_content", "")

        if(post_id == 0 or new_content == ""):
            return JsonResponse({"message": "Error"})

        user = request.user
        if(Post.objects.filter(id=post_id).first()):
            post = Post.objects.get(id=post_id)

            if(post.creator != user):
                return JsonResponse({"message": "Error"})
            
            post.content = new_content
            post.save()
            return JsonResponse({"message": "Post edited successfully"})

        return JsonResponse({"message": "Error"})
    return HttpResponseRedirect(reverse('index'))
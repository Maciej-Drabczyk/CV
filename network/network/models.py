from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="followings", blank=True)

    def check_follow(self, name):
        if self.followers.filter(username=name).first():
            return True
        else:
            return False

    def count_follows(self):
        return self.followers.count()
    
    def count_followings(self):
        return self.followings.count()
    
    def get_likes(self):
        posts = self.posts.all()
        posts = posts.filter(liked_by=self).all()
        return posts
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": self.count_follows(),
            "followings": self.count_followings()
        }


class Post(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField("User", related_name="liked", blank=True)

    def count_likes(self):
        return self.liked_by.count()
    
    def get_likes(self, user):
        likes = self.liked_by.all()
        if (likes.filter(username=user).first() != None):
            return True
        return False
    
    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "content": self.content,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.count_likes
        }
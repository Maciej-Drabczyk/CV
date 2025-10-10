from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count


class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="liked_posts", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "content": self.content,
            "date": self.date.strftime("%b %d %Y, %I:%M %p")
        }
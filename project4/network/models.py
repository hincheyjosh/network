
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone



class User(AbstractUser):
    following = models.ManyToManyField("self", related_name='follows', blank=True, symmetrical=False)

    def count_following(self):
        return self.following.count()

    def count_followers(self):
        return User.objects.filter(following=self).count()




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    body = models.TextField(max_length=200, null=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def total_likes(self):
        return self.likes.count()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=CASCADE)
    followee = models.ForeignKey(User,related_name='+',  on_delete=CASCADE)





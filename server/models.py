from django.db import models
from django.contrib.postgres.fields import ArrayField


class Location(models.Model):
    name = models.CharField(max_length=500)
    lat = models.IntegerField()
    lng = models.IntegerField()

    class Meta:
        db_table = "location"

    def __str__(self):
        return f'{self.name}'

class User(models.Model):
    email = models.CharField(max_length=500)
    fullname = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    avatarurl = models.CharField(max_length=500, null=True)
    bio = models.CharField(max_length=500, null=True)
    notificationToken = models.CharField(max_length=500, null=True)
    followers = models.ManyToManyField("self", through='UserFollowers', blank=True)
    following = models.ManyToManyField("self", through='UserFollowing', blank=True)
    locationsFollowing = models.ManyToManyField(Location, through="UserLocations")

    class Meta:
        db_table = "user"

    def __str__(self):
        return f'{self.fullname}'


class UserFollowers(models.Model):
    user = models.ForeignKey(User, db_column='userId_1', on_delete=models.CASCADE, related_name='followedUser')
    user2 = models.ForeignKey(User, db_column='userId_2', on_delete=models.CASCADE, related_name='follower2')

    class Meta:
        db_table = "user_followers_user"


class UserFollowing(models.Model):
    user = models.ForeignKey(User, db_column='userId_1', on_delete=models.CASCADE, related_name='followingUser')
    user2 = models.ForeignKey(User, db_column='userId_2', on_delete=models.CASCADE, related_name='following2')

    class Meta:
        db_table = "user_following_user"


class UserLocations(models.Model):
    user = models.ForeignKey(User, db_column='userId', on_delete=models.CASCADE, related_name='userLocation')
    location = models.ForeignKey(Location, db_column='locationId', on_delete=models.CASCADE)

    class Meta:
        db_table = "location_user_followers_user"


class Dialog(models.Model):
    members = ArrayField(models.IntegerField())
    users = models.ManyToManyField(User, through="DialogToUser")

    class Meta:
        db_table = "dialog"


class DialogToUser(models.Model):
    user = models.ForeignKey(User, db_column="userId", related_name="dialogOfUser", on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, db_column="dialogId", on_delete=models.CASCADE)

    class Meta:
        db_table = "dialog_users_user"


class Notification(models.Model):
    sendTo = models.IntegerField()
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userId")

    class Meta:
        db_table = "notification"

    def __str__(self):
        return f'{self.message} for {self.user}'


class Account(models.Model):
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=500)

    class Meta:
        db_table = "account"

    def __str__(self):
        return f'{self.email}'

class Message(models.Model):
    message = models.CharField(max_length=500, null=True)
    attachment = models.CharField(max_length=500, null=True)
    date = models.CharField(max_length=500, null=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, db_column="dialogId")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userId")

    class Meta:
        db_table = "message"

    def __str__(self):
        return f'{self.message} of {self.user}'


class Photo(models.Model):
    isAnonymous = models.BooleanField(null=True, default=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', db_column="userId")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, db_column="locationId")
    savedUsers = models.ManyToManyField(User, related_name='photosSaved', through="PhotoToUser")

    class Meta:
        db_table = "photo"


class PhotoToUser(models.Model):
    user = models.ForeignKey(User, db_column="userId", related_name="photoOfUser", on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, db_column="photoId", on_delete=models.CASCADE)

    class Meta:
        db_table = "photo_saved_users_user"


class Comment(models.Model):
    text = models.CharField(max_length=500)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, db_column="photoId")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userId")

    class Meta:
        db_table = "comment"

    def __str__(self):
        return f'{self.text} of {self.user}'


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', db_column="commentId")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photos', db_column="photoId")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', db_column="userId")

    class Meta:
        db_table = "like"

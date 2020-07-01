from django.contrib import admin
from .models import Comment, Location, Like, Dialog, User, Photo, Account, Notification, Message

# Register your models here.
admin.site.register(Comment)
admin.site.register(Location)
admin.site.register(Like)
admin.site.register(Dialog)
admin.site.register(User)
admin.site.register(Account)
admin.site.register(Photo)
admin.site.register(Notification)
admin.site.register(Message)

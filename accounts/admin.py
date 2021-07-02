from django.contrib import admin
from .models import User, Student, Union, FriendRequest
# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Union)
admin.site.register(FriendRequest)

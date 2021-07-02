import uuid

from accounts.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.urls import reverse
from django.utils.text import slugify

# from .signals import delete_post_image , resize_post_image
from .utils import number, incrementor
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Create your models here.


def upload_post_to(instance, filename):
    return f'post_image/{instance.user.username}/{filename}'


class PostManager(models.Manager):
    def get_posts(self, status: bool = False):
        return (
            self.get_queryset()
                .select_related("user", "user__profile")
                .prefetch_related("likes__profile", "comment_set__user__profile")
                .filter(archived=status)
        )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=False, null=True)
    image = models.FileField(null=True, blank=True, upload_to='post_images/', )
    filetype = models.CharField(max_length=10, blank=True, null=True)
    # likes = models.ManyToManyField(User, related_name="likes", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} : {self.text[:10]}"

    @property
    def image_url(self):
        if self.image == '':
            image = ''
        else:
            image = self.image.url
        return image

    def save(self, *args, **kwargs):
        self.slug = slugify(self.text[:5] + str(number()))
        if not self.image:
            self.image = ""
        if not self.text:
            self.text = ""
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]

    # to find url for each post
    def get_absolute_url(self):
        return reverse('student:detail', args=[self.slug])


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} : {self.user}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    sub_com = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


# post_delete.connect(delete_post_image, sender=Post)
# post_save.connect(resize_post_image, sender=Post)


class Room(models.Model):
    room_name = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    user1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user2')


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='m_from_user')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='m_to_user')
    message_type = models.CharField(max_length=10, default='text')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    message = models.TextField('message')
    # msg_img = models.ImageField(upload_to='msg_img/', height_field=None, width_field=None, blank=True, null=True)
    vid_img = models.FileField(upload_to='vid_img/', blank=True, null=True)
    # aud_img = models.FileField(upload_to='aud_img/', blank=True, null=True)
    # pdf_img = models.FileField(upload_to='pdf_img/', blank=True, null=True)




# class MessageModel(models.Model):
#     """
#     This class represents a chat message. It has a owner (user), timestamp and
#     the message body.
#
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user',
#                       related_name='m_from_user', db_index=True)
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='recipient',
#                            related_name='m_to_user', db_index=True)
#     timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False,
#                               db_index=True)
#     body = models.TextField('body')
#
#     def __str__(self):
#         return str(self.id)
#
#     def characters(self):
#         """
#         Toy function to count body characters.
#         :return: body's char number
#         """
#         return len(self.body)
#
#     def notify_ws_clients(self):
#         """
#         Inform client there is a new message.
#         """
#         notification = {
#             'type': 'recieve_group_message',
#             'message': '{}'.format(self.id)
#         }
#
#         channel_layer = get_channel_layer()
#         print("user.id {}".format(self.user.id))
#         print("user.id {}".format(self.recipient.id))
#
#         async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
#         async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)
#
#     def save(self, *args, **kwargs):
#         """
#         Trims white spaces, saves the message and notifies the recipient via WS
#         if the message is new.
#         """
#         new = self.id
#         self.body = self.body.strip()  # Trimming whitespaces from the body
#         super(MessageModel, self).save(*args, **kwargs)
#         if new is None:
#             self.notify_ws_clients()
#
#     # Meta
#     class Meta:
#         app_label = 'student'

import base64
import os.path
import re

from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import OuterRef, Exists
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Student, Union, User, FriendRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView, DeleteView

from .models import Post, Comment, SubComment, Like, Room, Message
from .forms import CreatePostForm, ProfileUpdateForm1, ProfileUpdateForm2, ProfileBgForm


# Create your views here.
# yt_link = re.compile(r'(https?://)?(www\.)?((youtu\.be/)|(youtube\.com/watch/?\?v=))([A-Za-z0-9-_]+)', re.I)
# yt_embed = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{0}" frameborder="0" ' \
#            'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> '
#
#
# def convert_ytframe(text):
#     """ to convert in to iframe """
#     return yt_link.sub(lambda match: yt_embed.format(match.groups()[5]), text)


class UserHomeView(LoginRequiredMixin, View):
    template_name = 'student/studenthome.html'

    def get(self, request: WSGIRequest) -> HttpResponse:
        post_form = CreatePostForm()
        union = User.objects.filter(is_union=True)
        sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
        rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)
        post = Post.objects.all()
        my_post = Post.objects.filter(user=request.user)
        friends = request.user.user_set.all()
        friends_pk = [f.pk for f in friends]
        req_pk = [f.to_user.pk for f in sent_friend_requests]
        rec_pk = [f.from_user.pk for f in rec_friend_requests]
        numb = req_pk + friends_pk + rec_pk  # numb is all other users
        numb.append(request.user.pk)
        student = User.objects.filter(is_union=False, is_superuser=False).exclude(pk__in=numb)

        lu = request.user
        po = ''
        for po in post:
            po.liked = Like.objects.filter(user=lu, post=po) and True or False
            # text = po.text
            # po.yt = convert_ytframe(text)  # converting to iframe not used in project

        context = {"post_form": post_form, 'student': student, 'union': union,
                   'po': po, 'post': post, 'sent_friend_requests': sent_friend_requests,
                   'rec_friend_requests': rec_friend_requests, 'friends': friends}

        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        post_form = CreatePostForm(request.POST, request.FILES)
        if not post_form.is_valid():
            messages.warning(self.request, 'Enter some text or Choose any file')
            return redirect('student:home')
        elif post_form.is_valid():
            obj = post_form.save(commit=False)
            file = post_form.cleaned_data.get('image')
            filetype = 'text'
            if file:
                file = file.name
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff', '.raw')):
                    filetype = 'image'
                elif file.endswith(('.mp4', '.mov', '.wmv', '.avi', '.mkv', '.webm', '.flv')):
                    filetype = 'video'
                else:
                    filetype = 'other'
            obj.user = request.user
            obj.filetype = filetype
            obj.save()
            return redirect('student:home')


class SinglePostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'student/single_post.html'

    def get_context_data(self, **kwargs):
        context = super(SinglePostDetailView, self).get_context_data(**kwargs)
        context['post'] = kwargs['object']
        context['other_posts'] = Post.objects.all().order_by('-id')[:5][::-1]
        return context


class SinglePostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [
        "text",
    ]
    success_url = reverse_lazy("student:home")


class SinglePostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("student:home")


class SingleUserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'student/single_user.html'

    def get_context_data(self, **kwargs):
        context = super(SingleUserDetailView, self).get_context_data(**kwargs)
        username = kwargs['object']
        single_user = User.objects.get(username=username)
        context['user'] = self.request.user
        context['single_user'] = single_user
        print(context)
        return context


@login_required(login_url='/accounts/login')
def add_comment(request):
    if request.POST['comment'] == '':
        return JsonResponse('error', safe=False)
    else:
        cmnt = request.POST['comment']
        post_id = request.POST['postid']
        post = Post.objects.get(pk=post_id)
        new_cmnt = Comment.objects.create(user=request.user, post=post, comment=cmnt)
        return JsonResponse('added', safe=False)


@login_required(login_url='/accounts/login')
def add_like(request):
    post_id = request.POST['postid']
    post = Post.objects.get(pk=post_id)
    new_like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        return JsonResponse('Liked', safe=False)
    else:
        return JsonResponse('Liked', safe=False)


class ProfileView(LoginRequiredMixin, View):
    template_name = "student/profile.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        me = Student.objects.get(user=request.user)
        p_form1 = ProfileUpdateForm1(instance=request.user)
        p_form2 = ProfileUpdateForm2(instance=me)
        my_union = me.union

        context = {'p_form1': p_form1, 'p_form2': p_form2, 'me': me}
        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        me = Student.objects.get(user=request.user)
        p_form2 = ProfileUpdateForm2(request.POST, instance=me)

        if p_form2.is_valid():
            p2 = p_form2.save(commit=False)
            p2.user = request.user
            p2.save()
            return redirect('student:profile')

        context = {"post_form": CreatePostForm()}
        return render(request, self.template_name, context)


@login_required(login_url='/accounts/login')
def edit_fullname(request):
    f_name = request.POST['first_name']
    l_name = request.POST['last_name']
    user_id = request.POST['user_id']
    me = User.objects.get(id=user_id)
    me.first_name = f_name
    me.last_name = l_name
    me.save()
    return JsonResponse('true', safe=False)


@login_required(login_url='/accounts/login')
def edit_profile_data(request):
    data = request.POST['editing_value']
    differ = request.POST['differ']
    user_id = request.POST['user_id']
    me = Student.objects.get(pk=user_id)
    us_me = User.objects.get(pk=user_id)

    if differ == 'bio':
        me.bio = data
        me.save()
        return JsonResponse('true', safe=False)
    elif differ == 'birthday':
        me.birth_date = data
        me.save()
        return JsonResponse('true', safe=False)
    elif differ == 'phone_number':
        us_me.phone_number = data
        us_me.save()
        return JsonResponse('true', safe=False)
    elif differ == 'location':
        me.location = data
        me.save()
        return JsonResponse('true', safe=False)
    elif differ == 'hobbies':
        me.hobbies = data
        me.save()
        return JsonResponse('true', safe=False)
    elif differ == 'interests':
        if me.interests == '':
            me.interests = [data]
        else:
            me.interests.append(data)
        me.save()
        return JsonResponse('true', safe=False)


class Timeline(LoginRequiredMixin, View):
    template_name = "student/timeline.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        me = request.user
        try:
            my_posts = Post.objects.filter(user=me)
        except:
            pass
        context = {'me': me, 'my_posts': my_posts}
        return render(request, self.template_name, context)


class Friends(LoginRequiredMixin, View):
    template_name = "student/friends.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        me = request.user

        friends = me.friends.all()

        context = {'me': me, 'friends': friends}
        return render(request, self.template_name, context)


class Unions(LoginRequiredMixin, View):
    template_name = "student/unions.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        me = request.user
        unions = User.objects.filter(is_union=True)
        try:
            my_union = me.student_set.union
        except:
            my_union = "not verified by a union"
        context = {'me': me, 'unions': unions, 'my_union': my_union}
        return render(request, self.template_name, context)


@login_required(login_url='/accounts/login')
def select_my_union(request):
    pk = request.POST['union']
    union = User.objects.get(pk=pk)
    if FriendRequest.objects.filter(from_user=request.user).exists():
        return JsonResponse('false', safe=False)
    else:
        f_request = FriendRequest.objects.create(
            from_user=request.user,
            to_user=union
        )
        return JsonResponse('true', safe=False)


@login_required(login_url='/accounts/login')
def upload_pp(request):
    pp = request.POST['profile_pic']
    user = request.user
    format, imgstr = pp.split(';base64,')
    ext = format.split('/')[-1]
    img = ContentFile(base64.b64decode(imgstr), name=user.username + '.' + ext)
    user.student.profile_img = img
    user.student.save()
    return redirect('student:profile')


@login_required(login_url='/accounts/login')
def upload_bg(request: WSGIRequest) -> HttpResponse:
    img = request.FILES.get('background_img')
    user = request.user
    user.student.background_img = img
    user.student.save()
    return redirect('student:profile')


@login_required(login_url='/accounts/login')
def chat_room(request, pk):
    user1 = request.user
    friends = user1.friends.all()
    if User.objects.filter(pk=pk).exists():
        user2 = User.objects.get(pk=pk)
        if Room.objects.filter(user2=user1, user1=user2).exists():
            room = Room.objects.get(user2=user1, user1=user2)
        else:
            room, created = Room.objects.get_or_create(user1=user1, user2=user2)
        messages_order = Message.objects.filter(room=room).order_by('-id')[:200]
        messages = reversed(messages_order)
        context = {'room': room, 'user1': user1, 'user2': user2, 'friends': friends, 'messages': messages}
        return render(request, 'student/chat.html', context)
    else:
        return redirect('student:friends')

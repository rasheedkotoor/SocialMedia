import requests
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
import base64

from accounts.models import Student, Union, User, MemberRequest, FriendRequest, PageAdmin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView
from student.forms import CreatePostForm
from student.models import Post
from student.views import UserHomeView


# Create your views here.


class UnionDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'union/union_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UnionDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        username = kwargs['object']
        union = User.objects.get(username=username)
        context['members'] = Student.objects.filter(union=union.pk)
        context['post'] = Post.objects.filter(user=union.pk).order_by('-created').first()
        context['union'] = union
        context['user'] = user
        if PageAdmin.objects.filter(page=union, admin=user).exists():
            context['admin'] = True
        return context


class MyUnionDetailView(LoginRequiredMixin, View):
    template_name = 'union/my_union.html'

    def get(self, request: WSGIRequest) -> HttpResponse:
        union = request.user.student.union
        members = Student.objects.filter(union=union.pk)
        union_post = Post.objects.filter(user=union.pk)
        if PageAdmin.objects.filter(page=union.user, admin=request.user).exists():
            admin = True
        else:
            admin = False

        context = {"union": union, "members": members, "union_post": union_post, 'admin': admin}
        return render(request, self.template_name, context)


class UnionAdminView(LoginRequiredMixin, View):
    template_name = 'union/union_admin_panel.html'

    def get(self, request: WSGIRequest) -> HttpResponse:
        post_form = CreatePostForm()
        union = request.user.student.union
        members = Student.objects.filter(union=union)
        member_requests = FriendRequest.objects.filter(to_user=union.user)
        if PageAdmin.objects.filter(page=union.user, admin=request.user).exists():
            admin = True
        else:
            admin = False

        context = {"union": union, "post_form": post_form, "members": members, 'member_requests': member_requests,
                   'admin': admin}
        return render(request, self.template_name, context)

    def post(self, request: WSGIRequest) -> HttpResponse:
        post_form = CreatePostForm(request.POST, request.FILES)
        union = request.user.student.union.user

        if post_form.is_valid():
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
            obj.user = union
            obj.filetype = filetype
            obj.save()
            return redirect('union:my_union')

        context = {"post_form": CreatePostForm()}
        return render(request, self.template_name, context)


@login_required(login_url='/accounts/login')
def union_join_req(request):
    union_id = request.POST['union_id']
    user_id = request.POST['user_id']
    value = request.POST['value']
    user = get_object_or_404(User, id=user_id)
    union = get_object_or_404(Union, user=union_id)

    if value == 'Accept':
        j_request = FriendRequest.objects.filter(
            from_user=user_id,
            to_user=union_id).first()
        user.is_verified = True
        user.student.union = union
        user.save()
        user.student.save()
        j_request.delete()
        return JsonResponse('Remove', safe=False)
    elif value == 'Reject':
        j_request = FriendRequest.objects.filter(
            from_user=user_id,
            to_user=union_id).first()
        j_request.delete()
        return JsonResponse('false', safe=False)
    elif value == 'Remove':
        user.is_verified = False
        user.save()
        user.student.union = None
        user.student.save()
        return JsonResponse('false', safe=False)


@login_required(login_url='/accounts/login')
def upload_union_pp(request):
    pp = request.POST['profile_pic']
    user = request.user
    union = user.student.union
    format, imgstr = pp.split(';base64,')
    ext = format.split('/')[-1]
    img = ContentFile(base64.b64decode(imgstr), name=union.user.username + '.' + ext)
    union.logo = img
    union.save()
    next = request.POST.get('next', '/unions/')
    return HttpResponseRedirect(next)


@login_required(login_url='/accounts/login')
def upload_union_bg(request: WSGIRequest) -> HttpResponse:
    img = request.FILES.get('background_img')
    user = request.user
    union = user.student.union
    union.background_img = img
    union.save()
    next = request.POST.get('next', '/unions/')
    return HttpResponseRedirect(next)


@login_required(login_url='/accounts/login')
def edit_profile_data(request):
    data = request.POST['editing_value']
    differ = request.POST['differ']
    union_id = request.POST['union_id']
    me = Union.objects.get(pk=union_id)
    us_me = User.objects.get(pk=union_id)

    if differ == 'username':
        us_me.username = data
        us_me.save()
        return JsonResponse('true', safe=False)
    elif differ == 'collage':
        me.college_name = data
        me.save()
        return JsonResponse('true', safe=False)
    elif differ == 'location':
        me.location = data
        me.save()
        return JsonResponse('true', safe=False)

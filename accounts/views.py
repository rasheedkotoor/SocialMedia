import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import auth
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView
from twilio.rest import Client

from StudentsCircle.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from .forms import StudentSignUpForm
from .models import User, FriendRequest, Student


# Create your views here.


class StudentRegister(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'accounts/student_register.html'

    def form_valid(self, form):
        user = form.save()
        # student, created = Student.objects.get_or_create(user=user)
        login(self.request, user)
        return redirect('/')


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/adminn/'
        return '/'


@login_required(login_url='/accounts/login')
def send_friend_request(request):
    to_id = request.POST['to_id']
    value = request.POST['value']
    sec_user = get_object_or_404(User, id=to_id)

    if value == 'Add Friend':
        f_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=sec_user)
        return JsonResponse('Cancel', safe=False)
    elif value == 'Cancel':
        f_request = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=sec_user).first()
        f_request.delete()
        return JsonResponse('Add Friend', safe=False)
    elif value == 'Accept':
        f_request = FriendRequest.objects.filter(
            from_user=sec_user,
            to_user=request.user).first()
        user1 = f_request.to_user
        user1.friends.add(sec_user)
        sec_user.friends.add(user1)
        f_request.delete()
        return JsonResponse('Message', safe=False)
    elif value == 'Delete':
        f_request = FriendRequest.objects.filter(
            from_user=sec_user,
            to_user=request.user).first()
        f_request.delete()
        return JsonResponse('Add Friend', safe=False)
    elif value == 'Unfriend':
        request.user.friends.remove(sec_user)
        sec_user.friends.remove(request.user)
        return JsonResponse('Add Friend', safe=False)

    elif value == 'Message':
        return redirect('student:message', sec_user)


def otp_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        phone_number = request.POST['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            request.session['phone_number'] = phone_number

            if user is not None:
                random_num = random.randint(1000, 9999)
                otp = random_num
                request.session['otp'] = otp
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f"your OTP is {otp}",
                    from_=TWILIO_PHONE_NUMBER,
                    to=f"+919497117447"
                )
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('upw', safe=False)
        else:
            return JsonResponse('nouser', safe=False)
    else:
        return render(request, 'accounts/otp_login.html')


def enter_otp(request):

    if request.method == 'POST':
        otp1 = request.POST['otp']
        phone_number = request.session['phone_number']
        otp = request.session['otp']
        user = User.objects.get(phone_number=phone_number)

        if int(otp1) == otp:
            auth.login(request, user)
            return JsonResponse('true', safe=False)
    else:
        return render(request, 'accounts/enter_otp.html')


# def post(self,request):
#     try:
#         id = request.user.id
#         # Get database
#         user = User.objects.get(id=id)
#         # Uploaded picture
#         thumb_file = request.FILES['uploadFile']
#         user.picture = thumb_file
#         user.save()
#         to_json_response = {
#                     'state':0
#                     }
#     except Exception as e:
#         print(e)
#         to_json_response={
#                 'state':1
#             }
#     return HttpResponse(json.dumps(to_json_response), content_type='application/json')

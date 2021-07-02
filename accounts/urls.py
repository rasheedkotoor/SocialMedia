from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import StudentRegister, UserLoginView, send_friend_request, otp_login, enter_otp

app_name = 'accounts'

urlpatterns = [
    # path('', TemplateView.as_view(template_name="accounts/home.html"), name='accounts'),
    path('student_register/', StudentRegister.as_view(), name='student_register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('login/', include('allauth.urls')),

    path('add_friend/', send_friend_request, name='add_friend'),
    path('otp_login/', otp_login, name='otp_login'),
    path('enter_otp/', enter_otp, name='enter_otp'),

]

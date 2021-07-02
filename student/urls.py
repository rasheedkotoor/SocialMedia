from django.urls import path
from django.views.generic import TemplateView
from .views import UserHomeView, add_comment, add_like, Timeline, \
    ProfileView, Friends, Unions, edit_fullname, edit_profile_data, \
    select_my_union, upload_pp, chat_room, upload_bg, SingleUserDetailView, SinglePostDetailView, SinglePostUpdateView, \
    SinglePostDeleteView

app_name = 'student'


urlpatterns = [
    path('', UserHomeView.as_view(), name='home'),

    path('add_cmnt/', add_comment, name='add_cmnt'),
    path('add_like/', add_like, name='add_like'),
    path('edit_fullname/', edit_fullname, name='edit_fullname'),
    path('edit_profile_data/', edit_profile_data, name='edit_profile_data'),
    path('select_my_union/', select_my_union, name='select_my_union'),
    path('upload_pp/', upload_pp, name='upload_pp'),
    path('upload_bg/', upload_bg, name='upload_bg'),
    path('chat_room/<int:pk>', chat_room, name='chat_room'),

    path('posts/<int:pk>', UserHomeView.as_view(), name='detail'),
    path('details/<int:pk>', SingleUserDetailView.as_view(), name='details'),
    path('post_details/<int:pk>', SinglePostDetailView.as_view(), name='post_details'),
    path('post_update/<int:pk>', SinglePostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>', SinglePostDeleteView.as_view(), name='post_delete'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('timeline/', Timeline.as_view(), name='timeline'),
    path('friends/', Friends.as_view(), name='friends'),
    path('unions/', Unions.as_view(), name='unions'),



]

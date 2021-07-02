from django.urls import path
from django.views.generic import TemplateView

from .views import AdminHomeView, UnionRegister, UnionsListView, UnionDetailView, add_page_admin, StudentsListView, \
    StudentDetailView

app_name = 'adminn'

urlpatterns = [
    path('', AdminHomeView.as_view(), name='home'),
    path('union_register/', UnionRegister.as_view(), name='union_register'),
    path('union_list/', UnionsListView.as_view(), name='union_list'),
    path('student_list/', StudentsListView.as_view(), name='student_list'),
    path('union_details/<int:pk>', UnionDetailView.as_view(), name='union_details'),
    path('student_details/<int:pk>', StudentDetailView.as_view(), name='student_details'),

    path('add_page_admin/', add_page_admin, name='add_page_admin'),

]


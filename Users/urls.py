from django.urls import path

from . import views

urlpatterns = [
    path("accounts/", views.ListCreateUserView.as_view()),
    path("login/", views.LoginUsersView.as_view()),
    path("accounts/newest/<int:amount_users>/", views.ListNewestUserView.as_view()),
    path("accounts/<pk>/", views.UpdateUserView.as_view()),
    path("accounts/<pk>/management/", views.UpdateManagementView.as_view())
    ]
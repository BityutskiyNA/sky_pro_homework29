from django.urls import path

from user.views import UserUpdateView, UserView, UserDeleteView, UserDetailView, UserCreateView

urlpatterns = [
    path('', UserView.as_view()),
    path("create/", UserCreateView.as_view()),
    path("<int:pk>/", UserDetailView.as_view()),
    path("<int:pk>/update/", UserUpdateView.as_view()),
    path("<int:pk>/delete/", UserDeleteView.as_view()),
]

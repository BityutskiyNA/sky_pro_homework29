from django.urls import path

from category.views import CatView, CatDetailView, CatUpdateView, CatdDeleteView, CatCreateView

urlpatterns = [
    path('', CatView.as_view()),
    path("create/", CatCreateView.as_view()),
    path("<int:pk>/", CatDetailView.as_view()),
    path("<int:pk>/update/", CatUpdateView.as_view()),
    path("<int:pk>/delete/", CatdDeleteView.as_view()),
]

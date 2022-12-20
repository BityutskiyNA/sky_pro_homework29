import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView

from ads.models import Ad
from ads.serializers import AdListSerializer
from category.models import Category
from sky_pro_homework29 import settings
from user.models import User


def ads(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        ad_name = request.GET.get('text', None)
        if ad_name:
            self.queryset = self.queryset.filter(
                name__contains=ad_name
            )

        ad_cat = request.GET.get('cat', None)
        if ad_cat:
            self.queryset = self.queryset.filter(
                category__id__contains=ad_cat
            )

        ad_location = request.GET.get('location', None)
        if ad_location:
            self.queryset = self.queryset.filter(
                author__location__name__contains=ad_location
            )

        ad_price_from = request.GET.get('price_from', None)
        ad_price_to = request.GET.get('price_to', None)
        if ad_price_from and ad_price_to:
            self.queryset = self.queryset.filter(
                price__gte=int(ad_price_from)
            )
            self.queryset = self.queryset.filter(
                price__lte=int(ad_price_to)
            )

        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'price', 'description', 'is_published', 'author', 'category']

    def post(self, request, *args, **kwargs):
        response = []
        ad_data = json.loads(request.body)
        user_data = User.objects.get(id=ad_data['author_id'])
        cat_data = Category.objects.get(id=ad_data['category_id'])
        ad = Ad.objects.create(
            name=ad_data['name'],
            author=user_data,
            price=ad_data['price'],
            description=ad_data['description'],
            category=cat_data,
            is_published=ad_data['is_published']
        )

        response.append(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "image": str(ad.image),
                "category": ad.category_id,
                "is_published": ad.is_published,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'is_published', 'image', 'author', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        response = []
        ad_data = json.loads(request.body)
        user_data = User.objects.get(id=ad_data['author_id'])
        cat_data = Category.objects.get(id=ad_data['category_id'])
        self.object.name = ad_data['name']
        self.object.author = user_data
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.category = cat_data

        self.object.save()

        response.append(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author": self.object.author_id,
                "price": self.object.price,
                "description": self.object.description,
                "image": str(self.object.image),
                "category": self.object.category_id,
                "is_published": self.object.is_published,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        response = []
        ad = self.get_object()
        response.append(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "image": str(ad.image),
                "category": ad.category_id,
                "is_published": ad.is_published,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()
        user_data = User.objects.get(id=self.object.author_id)
        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author_id": self.object.author_id,
                "author": user_data.first_name,
                "price": self.object.price,
                "description": self.object.description,
                "image": str(self.object.image),
                "category": self.object.category_id,
                "is_published": self.object.is_published,
            }
        )

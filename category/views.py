import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from category.models import Category


class CatView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')
        response = []
        for cat in self.object_list:
            response.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        cat = Category.objects.create(
            name=cat_data['name']
        )

        response = [{
            "id": cat.id,
            "name": cat.name,
        }]
        return JsonResponse(response, safe=False)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        response = []
        response.append(
            {
                "id": cat.id,
                "name": cat.name,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        response = []
        ad_data = json.loads(request.body)
        self.object.name = ad_data['name']

        self.object.save()

        response.append(
            {
                "id": self.object.id,
                "name": self.object.name,
            }
        )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatdDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)

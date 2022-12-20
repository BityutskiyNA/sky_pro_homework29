from django.contrib import admin

from ads.models import Ad
from category.models import Category
from user.models import Location, User

admin.site.register(Ad)
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Category)


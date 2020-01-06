from django.contrib import admin
from .models import Preferred_shops, Shop, Disliked_shops
# Register your models here.
admin.site.register(Shop)
admin.site.register(Preferred_shops)
admin.site.register(Disliked_shops)
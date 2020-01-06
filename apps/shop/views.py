import datetime
import re

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Shop, Preferred_shops, Disliked_shops


# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('authentification')
    else:
        if request.method == 'GET':
            deleteDislikedShops(request)
            context = {
                'page_name': "index",
            }
            return render(request, "index.html", context)


def deleteDislikedShops(request):
    disliked = Disliked_shops.objects.all()
    for d in disliked:
        diff = datetime.datetime.now() - d.dislike_time.replace(tzinfo=None)
        hours = diff.days * 24 + (diff.seconds / 3600)
        if hours > 2:
            d.delete()


@csrf_exempt
def save_events_json(request):
    if request.is_ajax() and request.method == 'POST' and request.body.decode() is not None:
        data = re.split(r'[=&]*', request.body.decode())
        Latitude = data[1]
        Longitude = data[3]
        current_user = request.user.id
        shops = Shop.objects.raw('''
        SELECT * , POWER( s.long - (%s), 2 ) + POWER( s.lat - (%s), 2 ) AS distance FROM shop_shop s 
        LEFT JOIN shop_disliked_shops d ON s.id = d.Shop_id LEFT JOIN shop_preferred_shops p ON s.id = p.Shop_id 
        WHERE  d.CustomUser_id != %s  OR p.CustomUser_id != %s OR (d.id IS NULL  AND p.id IS NULL)
        ORDER BY distance ;''', [Longitude, Latitude, current_user, current_user])
        data = serializers.serialize('json', shops)
        return HttpResponse(data, content_type='application/json')


def addPreferredShop(request, id):
    if not request.user.is_authenticated:
        return redirect('authentification')
    else:
        current_user = request.user
        Preferred_shops(Shop_id=id, CustomUser=current_user).save()

        return redirect('preferredShop')


def addDislikedShop(request, id):
    if not request.user.is_authenticated:
        return redirect('authentification')
    else:
        current_user = request.user
        now = datetime.datetime.now()
        Disliked_shops(Shop_id=id, CustomUser=current_user, dislike_time=now).save()

        return redirect('index')


def deletePreferredShop(request, id):
    if not request.user.is_authenticated:
        return redirect('authentification')
    else:
        Preferred_shops.objects.filter(Shop_id=id).delete()
        return redirect('index')


def preferredShop(request):
    if not request.user.is_authenticated:
        return redirect('authentification')
    else:
        if request.method == 'GET':
            current_user = request.user
            pr = Preferred_shops.objects.filter(CustomUser=current_user).prefetch_related()
            context = {
                'preferred_shops': pr,
                'page_name': "preferred_shop",
            }
            return render(request, "preferredShops.html", context)

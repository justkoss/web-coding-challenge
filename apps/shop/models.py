from django.db import models

from apps.profil.models import CustomUser


# Create your models here.
class Shop(models.Model):
    long = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False)
    name = models.CharField(max_length=45, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False, default="")
    model_pic = models.ImageField(upload_to='media/', default='images/no-img.png')
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, default="")

    def __str__(self):
        return self.name


class Preferred_shops(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, default="")
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True, default="")


class Disliked_shops(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, default="")
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True, default="")
    dislike_time = models.DateTimeField(blank=True, null=True, default="")

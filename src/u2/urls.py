
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home.as_view(), name="sellerhome"),
    path('newproduct', newproduct.as_view(), name="newproduct"),
    path('updateproduct/<int:id>', updatepro.as_view(), name="updateproduct"),
    path('deleteproduct/<int:id>', delete_product, name="deleteproduct"),

]

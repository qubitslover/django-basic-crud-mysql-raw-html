from django.shortcuts import render,redirect,reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login, logout, authenticate
from django.views import View
from .models import *
from django.http import HttpResponseRedirect


class Home(View):

    def get(self,request):

        seller_pro = Products.objects.filter(seller=request.user)
        context = {
            'products': seller_pro,
        }
        return render(request,'sops/home.html', context)



class newproduct(View):

    def get(self,request):

        return render(request,'sops/newpro.html')

    def post(self, request):

        name = request.POST['name']
        price = request.POST['price']
        category = request.POST['category']
        info = request.POST['description']
        status = request.POST['status']
        Products.objects.create(name=name, price=price, category=category, descritpion=info, status=False, seller=request.user)
        return redirect('/seller/newproduct')

class updatepro(View):

    def get(self,request, **kwargs):

        print(kwargs)
        get_product = Products.objects.get(id=kwargs['id'])

        return render(request, 'sops/editpro.html', {'product':get_product})

    def post(self, request, *args, **kwargs):
        print(kwargs)

        product_id = kwargs['id']
        name = request.POST['name']
        price = request.POST['price']
        category = request.POST['category']
        info = request.POST['description']
        status = request.POST['status']
        # id = request.POST['id']

        Products.objects.filter(id=product_id).update(name=name, price=price, category=category, descritpion=info,
                                                      status=status)

        return redirect('updateproduct', id=product_id)

@login_required(login_url='/seller/login')
def delete_product(request,id):

    product_to_delete = Products.objects.get(id=id)
    product_to_delete.delete()
    return redirect('/seller/')

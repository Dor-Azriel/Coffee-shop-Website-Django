from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import item,Menu,item_menu,order,order_item,table,seat
from django.forms import DateInput
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


def menu_dis(request,*args):
    print(Menu.objects.all())
    response =render(request,"menus_dis.html",{"list":Menu.objects.all()})
    if 'cart' not in request.COOKIES:
        response.set_cookie('cart','')
    return response

def show_menu(request,id,arg=None):
    if request.method == 'POST' :
        print(request.POST)
        if request.POST['Order'] == 'inc':
            items = item.objects.filter(menu_key=id).order_by('price')
        if request.POST['Order'] == 'dec':
            items = item.objects.filter(menu_key=id).order_by('price').reverse()
        if request.POST['Order'] == 'pop':
            items = item.objects.filter(menu_key=id).order_by('popularity')
        if request.POST['Order'] == 'rec':
            items = item.objects.filter(menu_key=id,special=True)
        if request.POST['Order'] == 'bus':
            items = item.objects.filter(menu_key=id,kind='business')
    else:
        items = item.objects.filter(menu_key=id)

    for it in items:
            it.vip=str(it.vip_price)
            print(it.vip)
    if request.user.groups.filter(name='client_vip').exists():
        vip =True
    else:
        vip = False
    response =render(request,"full_menu.html",{'menu':Menu.objects.get(id=id),
                                               'items': items,'is_vip':vip})
    #print(Menu.objects.filter(id=id))

    return response

def home_view(request,*args,**kargs):
    response = render(request, "start.html")
    response.set_cookie('price','0')
    response.set_cookie('cart','')
    return response


def add_to_cart(request,id=None):

    if request.method == 'POST':
        response = redirect('show_menu',id=id)
        items= request.COOKIES['cart']
        #print(request.POST)
        items+=request.POST.get('num')
        items += ","
        response.set_cookie('cart',items)
        #init price cookie
        if 'price' not in request.COOKIES and item.objects.filter(id=int(request.POST.get('num'))).exists():
            if item.objects.get(id=int(request.POST.get('num'))).special_price:
                response.set_cookie('price', str(
                    item.objects.get(id=int(request.POST.get('num'))).special_price))
            if request.user.groups.all().exists():
                if item.objects.get(id=int(request.POST.get('num'))).vip_price and request.user.groups.all()[0]=='client_vip':
                    response.set_cookie('price', str(
                        item.objects.get(id=int(request.POST.get('num'))).vip_price))
            else:
                response.set_cookie('price', str(
                                             item.objects.get(id=int(request.POST.get('num'))).price))
        #adding new item price to order price

        elif item.objects.filter(id=int(request.POST.get('num'))).exists() :
            if request.user.groups.all().filter(name="client_vip").exists():
                print("ccc")
                if item.objects.get(id=int(request.POST.get('num'))).vip_price and request.user.groups.all()[0].name=='client_vip':
                    response.set_cookie('price', str(float(request.COOKIES['price']) +
                                                     item.objects.get(id=int(request.POST.get('num'))).vip_price))
            elif item.objects.get(id=int(request.POST.get('num'))).special_price:
                response.set_cookie('price',str(float(request.COOKIES['price'])+
                        item.objects.get(id=int(request.POST.get('num'))).special_price))
            else:
                response.set_cookie('price',str(float(request.COOKIES['price'])+
                        item.objects.get(id=int(request.POST.get('num'))).price))
        print(request.user.groups.all())
        print(request.user.groups.all().filter(name="client_vip").exists())
        return response


def show_cart(request):
    new_cok = None
    cookies=-1
    price=0
    if request.method == 'POST':
        if request.POST.get('num'):
            items = request.COOKIES['cart'].split(',')
            new_cok=""
            if request.POST.get('num') in items :
                items.remove(request.POST.get('num'))
                print(items)
                for it in items:
                    if it !='':
                        new_cok += str(it) + ","
                print(item.objects.all().filter(id=int(request.POST.get('num'))).exists())
                if item.objects.all().filter(id=int(request.POST.get('num'))).exists():
                    cookies =float(request.COOKIES['price'])
                    if request.user.groups.all().filter(name="client_vip").exists():
                        print("!!!!!!!!!!!")
                        print(item.objects.get(id=int(request.POST.get('num'))).vip_price != None)
                        print(request.user.groups.all()[0]=='client_vip')
                        if item.objects.get(id=int(request.POST.get('num'))).vip_price != None and request.user.groups.all()[0].name=='client_vip':
                            price=item.objects.get(id=int(request.POST.get('num'))).vip_price
                    elif item.objects.get(id=int(request.POST.get('num'))).special_price:
                        price = item.objects.get(id=int(request.POST.get('num'))).special_price
                    else:
                        price=item.objects.get(id=int(request.POST.get('num'))).price
                cookies= cookies-price

    elif 'cart' in request.COOKIES:
        items = request.COOKIES['cart'].split(',')
    print(items)
    objlist = list()
    if 'cart' in request.COOKIES:
        for i in items:
            if i != '':
                objlist.append(item.objects.get(id=i))

    if request.user.groups.all().filter(name="barista").exists():
        html="barista_cart.html"
    else:
        html="cart.html"
    if new_cok != None:
        response=render(request,html,{'items':objlist})
        response.set_cookie('cart',new_cok)
    else:
        response=render(request,html,{'items':objlist})
    if cookies!=-1:
        response.set_cookie('price',str(cookies))
    return response



 ############# barista #############
def barista_home(request):
    if request.method=='POST':
        if request.POST['conf']:
            if order.objects.filter(id=request.POST.get('num')).exists():
                order.objects.filter(id=request.POST.get('num')).update(ready=True)
    response = render(request,"barista_home.html",{'orders':order.objects.all().filter(ready=False)})
    if 'order' not in request.COOKIES:
        response.set_cookie('order','')

    return response

def order_details(request,id):
    if request.method == 'POST':
       if request.POST['remove']:
            if order_item.objects.filter(item=request.POST.get('remove'),order=id).exists():
                order_item.objects.filter(item=request.POST.get('remove'),order=id).delete()

    items_ids = order_item.objects.all().filter(order=id).values_list('item')
    items=list()
    for i in items_ids:
        if i :
            items.append(item.objects.get(id=i[0]))

    return render(request,"order_details.html",{'items':items , 'id':id})

def update_order(request,id):
    items_ids = order_item.objects.all().filter(order=id).values_list('item')
    items = list()
    for i in items_ids:
        if i:
            items.append(item.objects.get(id=i[0]))

    return render(request, "order_details.html", {'items': items})

def brista_tabels(request):
    tables = table.objects.filter(active=False)
    return render(request,"tables.html",{'tables':tables})

def client_tables(request):
    tables = table.objects.filter(active=False,reserve=False)
    return render(request, "tables.html", {'tables': tables})


def log(request):
    groups = request.user.groups.all()
    if not groups:
        return redirect("menus")
    elif groups[0].name == 'barista':
        return redirect('barista')
    elif groups[0].name == 'client':
        return redirect("menus")
    elif groups[0].name=='client_vip':
        response =redirect("menus")
        response.set_cookie("vip","1")
        return response
    return redirect('home_view')



def logout_view(request):
    logout(request)
    response=render(request, "start.html" )
    response.set_cookie("cart","")
    response.set_cookie("price","0")
    if 'vip' in request.COOKIES:
        response.delete_cookie("vip")
    return response


def coffee(request):
    print(request.user.groups.all())
    return render(request,"coffee_dis.html",{'menu': {'name':"Coffee types"},
                                               'items': item.objects.all().filter(kind='coffee')})

def brista_order(request):
    return render(request,"barista_order.html",{'items': item.objects.all().filter(available=True)})


def create_order(request,tab):
    items = request.COOKIES['cart'].split(',')
    obj_items=list()
    for itm in items:
        if itm !='':
            if item.objects.filter(id=int(itm)).exists():
                obj_items.append(item.objects.get(id=int(itm)))
    summary=0
    for itm in obj_items:
        summary+=itm.price
    if tab != 0:
        ord=order(summary=summary,table=table.objects.get(id=tab))
    else:
        ord = order(summary=summary)
    ord.save()
    ord_itm=list()
    for obj in obj_items:
        ord_itm.append(order_item(item=itm,order=ord))
    for o in ord_itm:
        o.save()
    ressponse =redirect("payment_method")
    ressponse.set_cookie("order",ord.id)
    return ressponse


def choose_table(request):

    tables = table.objects.filter(active=False)
    for tab in tables :
        tab.add = seat.objects.filter(table_key=tab.pk).count()
    return render(request, "tables.html", {'tables': tables})

def save_table(request):
    if request.method == 'POST':
        if request.POST['choose']:
            if table.objects.filter(id=request.POST.get('num')).exists():
                table.objects.filter(id=request.POST.get('num')).update(reserve=True)
                tab=table.objects.filter(id=request.POST.get('num'))
                return redirect("create_order",tab[0].id)
    return redirect("choose_table")


def thanks_page(request):
    order.objects.filter(id=request.COOKIES['order']).update(payed=True)
    ord= order.objects.get(id=request.COOKIES['order'])
    if ord.table:
        table.objects.filter(id=ord.table.id).update(active=True)
    print(order.objects.get(id=request.COOKIES['order']))
    response =render(request,"thanks.html")
    response.set_cookie('cart','')
    response.set_cookie('price','0')
    return response

def payment_method(request):
    if request.method == 'POST':
        if request.POST['cash']:
            return redirect("payment_cash")
        if request.POST['credit']:
            return redirect("pay")
    if request.user.groups.all().filter(name="barista").exists():
        html = "payment_method_barista.html"
    else:
        html ="payment_method.html"
    return render(request,html)

def payment_cash(request):
    ord = order.objects.get(id=request.COOKIES['order'])
    if request.user.groups.all().filter(name="barista").exists():
        response= render(request,"barista_thanks.html")
    else:
        response=render(request,"payment_cash.html",{'number': ord.id , 'sum': ord.summary})
    response.set_cookie('cart','')
    response.set_cookie('price','0')
    return response

def add_to_cart_barista(request):

    if request.method == 'POST':
        response = redirect('barista_order')
        items= request.COOKIES['cart']
        #print(request.POST)
        items+=request.POST.get('num')
        items += ","
        response.set_cookie('cart',items)
        #init price cookie
        if 'price' not in request.COOKIES and item.objects.filter(id=int(request.POST.get('num'))).exists():
            response.set_cookie('price', str(
                                             item.objects.get(id=int(request.POST.get('num'))).price))
        #adding new item price to order price
        elif item.objects.filter(id=int(request.POST.get('num'))).exists() :
            response.set_cookie('price',str(float(request.COOKIES['price'])+
                            item.objects.get(id=int(request.POST.get('num'))).price))
        return response

def wait_for_pay(request):
    if request.method == 'POST':

        if request.POST.get('num'):
            return redirect("payment_method")
    return render(request,"wait_for_pay.html",{'orders':order.objects.filter(payed=False).order_by("time")})

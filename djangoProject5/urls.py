"""djangoProject5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Menu.views import home_view,menu_dis,show_menu,add_to_cart,show_cart,barista_home
from Menu.views import order_details,brista_tabels,log,logout_view,coffee,brista_order,client_tables,save_table
from Menu.forms import add_item,update_item,delete_item,add_menu,update_menu,delete_menu,add_item_menu,add_payment
from Menu.views import create_order,choose_table,thanks_page,payment_method,payment_cash,add_to_cart_barista,wait_for_pay
from items_menu.views import register_request
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home_view'),
    path('item/<int:pk>/new/',add_item.as_view()),
    path('item/<int:pk>/update/',update_item.as_view()),
    path('item/<int:pk>/delete/',delete_item.as_view()),
    path('menu/<int:pk>/new/',add_menu.as_view()),
    path('menu/<int:pk>/update/',update_menu.as_view()),
    path('menu/<int:pk>/delete/', delete_menu.as_view()),
    path('addtomenu/add/',add_item_menu.as_view()),
    #path('user/add/', add_user.as_view())
    path("register", register_request, name="register"),
    path("menus/",menu_dis,name="menus"),
    path("menus/<int:id>/", show_menu,name="show_menu"),
    path("addcart/<int:id>",add_to_cart,name="add_to_cart"),
    path("cart/",show_cart,name="cart"),
    path("barista/",barista_home, name="barista"),
    path("barista/<int:id>/",order_details,name="order_details"),
    path("barista/tables/",choose_table,name="tables"),
    path('login/', LoginView.as_view(template_name='admin/login.html',), name='login'),
    path('accounts/profile/', log, name='logd_view'),
    path('logout/',logout_view,name="logout"),
    path('coffee/',coffee, name="coffee"),
    path('barista/order/',brista_order,name="barista_order"),
    path("order/<int:tab>",create_order,name="create_order"),
    path('client/tables/',choose_table,name="client_tables"),
    path('payment/',add_payment.as_view(),name="pay"),
    path('thanks/',thanks_page,name="thanks_page"),
    path('saved/',save_table,name="save_table"),
    path('payment/method',payment_method,name="payment_method"),
    path('payment/cash', payment_cash, name="payment_cash"),
    path('barista/add',add_to_cart_barista,name="add_to_cart_barista"),
    path('barista/waiting/',wait_for_pay,name="wait_pay")

]

from django.urls import path
from . import views
from .middlewares.auth import  auth_middleware

from .views import index,Login,logout,Cart,CheckOut,OrderView


urlpatterns= [
    
    path('', index,name='index'),
    path('signup', views.signup),
     path('login', Login.as_view(), name='login'),
    # path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
     path('logout', logout , name='logout'),
    path('cart',(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders',(OrderView.as_view()), name='orders'),
    path('search', views.search, name='search'),
   # path('empty_cart/', views.empty_cart_view, name='empty_cart'),
    path('order/<int:order_id>/bill/', views.generate_bill_pdf, name='generate_bill_pdf'),
    path('order_con', views.order_con, name='order_con'),

 
  
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
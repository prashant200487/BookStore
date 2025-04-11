from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.cart_list, name='cart_list'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('signup/', views.signup, name='signup'),
    path('debug-cart/', views.debug_cart, name='debug_cart'),
    path('cart/update/<int:book_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/delete/<int:book_id>/', views.delete_from_cart, name='delete_from_cart'),
]
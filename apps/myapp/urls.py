from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('main', views.index),
	path('register', views.register),
	path('dashboard', views.dashboard),
	path('wish_items/<id>', views.wish_items),
	path('delete/<id>', views.delete),
	path('remove/<id>', views.remove),
	path('addtowishlist/<id>', views.wishlist),
	path('create', views.additem),
	path('processitem', views.processitem),
	path('login', views.login),
	path('logout', views.logout)
]
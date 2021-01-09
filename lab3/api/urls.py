from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_all_cats, name = 'all-cats'),
    path('cat-by-id/<str:pk>/', views.get_cat_by_id, name = 'cat-by-id'),
    path('cat-by-name/<str:cat_name>/', views.get_cat_by_name, name = 'cat-by-name'),
    path('create-cat/', views.create_cat, name = 'create-cat'),
    path('patch-cat/<str:pk>/', views.patch_cat, name = 'patch-cat'),
    path('put-cat/<str:pk>/', views.put_cat, name = 'put-cat'),
]

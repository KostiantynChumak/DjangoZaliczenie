from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.detail, name="detail"),
    path('addrestaurants/', views.add_restaurants, name="add_restaurants"),
    path('editrestaurants/<int:id>/', views.edit_restaurants, name="edit_restaurants"),
    path('deleterestaurants/<int:id>/', views.delete_restaurants, name="delete_restaurant"),
    path('addreview/<int:id>/', views.add_review, name="add_review"),
    path('editreview/<int:restaurant_id>/<int:review_id>/', views.edit_review, name="edit_review"),
    path('deletereview/<int:restaurant_id>/<int:review_id>/', views.delete_review, name="delete_review"),


]
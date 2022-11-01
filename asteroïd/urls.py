from django.urls import path

from . import views

urlpatterns = [
    path('',views.dates, name="dates"),
    path('results', views.results, name='results'),
]
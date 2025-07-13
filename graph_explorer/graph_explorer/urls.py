from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter_view, name='filter'),
    path('select-visualizer/', views.select_visualizer),
    path('select-workspace/', views.select_workspace),
]

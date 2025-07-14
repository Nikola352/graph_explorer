from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter_view, name='filter'),
    path('select-visualizer/', views.select_visualizer),
    path('select-workspace/', views.select_workspace),
    path('workspace-form/', views.workspace_form),
    path('save-workspace/', views.save_workspace, name='save-workspace'),
    path('delete-workspace/<str:workspace_id>/', views.delete_workspace),
]

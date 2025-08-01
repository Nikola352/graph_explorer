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
    path('search/', views.search_view, name='search'),
    path('remove-filter/', views.remove_filter, name='remove-filter'),
    path('remove-search/', views.remove_search, name='remove-search'),
    path('data-source-config', views.data_source_config),
    path('refresh-data-source/', views.refresh_data_source),
    path('cli/execute/', views.cli_command_view, name='cli_command'),
]

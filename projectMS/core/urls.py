from django.contrib import admin
from django.urls import path
from . import views

app_name = 'core_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/<str:filter>', views.home, name='dashboard'),
    path('related-projects/<str:category_key>/<str:filter>', views.related_projects, name='related_projects'),
    path('submit-project-files/<str:project_id>', views.submit_project_files, name='submit_project_files'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create-project/<str:group_id>', views.create_project, name='create_project'),
    path('create-group', views.create_group, name='create_group'),
    path('delete-group/<str:group_id>', views.delete_group, name='delete_group'),
    path('set-deadlines/<str:project_id>', views.set_deadlines, name='set_deadlines'),
    path('group-projects/<str:group_id>', views.single_group, name='single_group'),
    path('complete-project-step/<str:pk>', views.complete_project_step, name='complete_project_step'),
    path('mark-as-completed/<str:pk>', views.mark_as_completed, name='mark_as_completed'),
    path('notifications/<str:user_id>', views.get_notifications, name='get_notifications'),
    path('filtered/<str:filter>/<str:year>', views.filter_by_specific_year, name="filter_by_specific_year")
]

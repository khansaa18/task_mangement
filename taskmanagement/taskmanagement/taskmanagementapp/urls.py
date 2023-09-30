from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('home', index, name='home'),
    path('user', register_user, name='user'),
    path('deleteUser/<str:id>/', delete_user, name='deleteUser'),
    path('addtask', add_task, name='addtask'),
    path('mytasks', my_task, name='mytasks'),
    path('deleteTask/<str:taskid>/', delete_task, name='deleteTask'),
    path('markCompleted/<str:taskid>/', mark_complete, name='markCompleted'),
    path('startTask/<str:taskid>/', start_task, name='startTask'),
    path('usertasks', user_task, name='usertasks')
]

from django.urls import path
from .views import employee_hierarchy, employee_list, employee_create, employee_update, employee_delete  # Import the views module

urlpatterns = [
    path('hierarchy/', employee_hierarchy, name='employee_hierarchy'),  # Correct function name
    path('list/', employee_list, name='employee_list'),  # Correct function name
    path('create/', employee_create, name='employee_create'),
    path('update/<int:pk>/', employee_update, name='employee_update'),
    path('delete/<int:pk>/', employee_delete, name='employee_delete'),
]


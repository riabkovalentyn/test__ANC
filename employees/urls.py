from django.urls import path
from .views import employee_hierarchy, employee_list  # Import the views module

urlpatterns = [
    path('hierarchy/', employee_hierarchy, name='employee_hierarchy'),  # Correct function name
    path('list/', employee_list, name='employee_list'),  # Correct function name
]

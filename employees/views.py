from django.shortcuts import render
from django.db.models import Q
from .models import Employee


def employee_hierarchy(request):
    top_lvl_employees = Employee.objects.filter(manager__isnull=True)
    return render(request, 'employees/hierarchy.html', {'employees': top_lvl_employees})


def employee_list(request):
    employees = Employee.objects.all()
    sort_by = request.GET.get('sort_by', 'full_name')
    employees = employees.order_by(sort_by)
    query = request.GET.get('query', '')
    if query:
        employees = employees.filter(
            Q(full_name__icontains=query) |
            Q(position__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'employees/list.html', {'employees': employees, 'query': query, 'sort_by': sort_by})

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import Employee
from .forms import EmployeeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def employee_hierarchy(request):
    top_lvl_employees = Employee.objects.filter(manager__isnull=True)
    return render(request, 'employees/employee_hierarchy.html', {'employees': top_lvl_employees})


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
    return render(request, 'employees/employee_list.html', {'employees': employees, 'query': query, 'sort_by': sort_by})


def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


def build_employee_tree(employees, parent_id=None):
    tree_html = '<ul>'
    for employee in employees:
        if employee.manager_id == parent_id:
            tree_html += f'<li data-id="{employee.id}">{employee.full_name} - {employee.position}'
            tree_html += build_employee_tree(employees, employee.id)
            tree_html += '</li>'
    tree_html += '</ul>'
    return tree_html


def employee_hierarchy(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_hierarchy.html', {'employees': employees})


def change_manager(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        new_manager_id = request.POST.get('new_manager_id')
        try:
            employee = Employee.objects.get(pk=employee_id)
            new_manager = Employee.objects.get(pk=new_manager_id)
            employee.manager = new_manager
            employee.save()
            return JsonResponse({'success': True})
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee or manager does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
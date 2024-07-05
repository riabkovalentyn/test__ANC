import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from employees.models import Employee

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **kwargs):
        num_employees = 50000
        levels = 7

        self.stdout.write('Deleting old data...')
        Employee.objects.all().delete()

        self.stdout.write('Creating new data...')

        # Create top-level manager
        top_manager = Employee.objects.create(
            full_name="Top Manager",
            position="CEO",
            hire_date=datetime.now() - timedelta(days=365*5),
            email="topmanager@company.com"
        )

        employees = [top_manager]
        for level in range(1, levels):
            for _ in range(2 ** level):
                manager = random.choice(employees)
                employee = Employee(
                    full_name=f"Employee {len(employees) + 1}",
                    position=f"Position {level}",
                    hire_date=datetime.now() - timedelta(days=random.randint(0, 365*level)),
                    email=f"employee{len(employees) + 1}@company.com",
                    manager=manager
                )
                employees.append(employee)
                employee.save()

        self.stdout.write('Database populated with test data.')
from django.core.management.base import BaseCommand
import pandas as pd
from sku.models import Location, Department, Category, SubCategory, SKUDataMapping


class Command(BaseCommand):
    """
    run command to load the: data:= python manage.py importdata sku\meta_data.csv
    """
    help = 'Import data from CSV file and insert into Django models'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        filepath = options['filepath']
        try:
            data = pd.read_csv(filepath)
            for index, row in data.iterrows():
                location, created = Location.objects.get_or_create(name=row['Location'])
                department, created = Department.objects.get_or_create(name=row['Department'], location=location)
                category, created = Category.objects.get_or_create(name=row['Category'], department=department)
                subcategory, created = SubCategory.objects.get_or_create(name=row['SubCategory'], category=category)
                #SKUDataMapping.objects.create(description=row['NAME'], location=location, department=department, category=category, subcategory=subcategory)
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))

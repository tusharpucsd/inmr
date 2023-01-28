from django.core.management.base import BaseCommand
import pandas as pd
from sku.models import Location, Department, Category, SubCategory, SKUDataMapping


class Command(BaseCommand):
    """
    run command to load the: data:= python manage.py loadskudata sku\sku_data.txt
    """
    help = 'Import data from text file and insert into Django models'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        filepath = options['filepath']
        try:
            data = pd.read_csv(filepath)
            for index, row in data.iterrows():
                try:
                    location, created = Location.objects.get_or_create(name=row['LOCATION'])
                    department, created = Department.objects.get_or_create(name=row['DEPARTMENT'], location=location)
                    category, created = Category.objects.get_or_create(name=row['CATEGORY'], department=department)
                    subcategory, created = SubCategory.objects.get_or_create(name=row['SUBCATEGORY'], category=category)
                    sku_name = "SKUDESC{}".format(index+1)
                    SKUDataMapping.objects.create(description=sku_name, location=location, department=department, category=category, subcategory=subcategory)
                except Exception as ex:
                    self.stdout.write(self.style.ERROR(ex))
            self.stdout.write(self.style.SUCCESS('SKU Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))

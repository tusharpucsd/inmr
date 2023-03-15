from rest_framework import serializers
from .models import Location, Department, Category, SubCategory, SKUDataMapping


class LocationSerializer(serializers.ModelSerializer):
    departments = serializers.SerializerMethodField("get_all_departments")

    class Meta:
        model = Location
        fields = ('name', 'departments')
        # fields = '__all__'

    def get_all_departments(self, obj):
        return obj.department_set.all().values_list('name')

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField('get_department_name')

    class Meta:
        model = Category
        fields = ('id', 'name', 'department', 'department_name')
    
        def get_department_name(self, obj):
        return obj.department.name


    def validate_name(self, value):
        """Field level validation"""
        if not value.isalpha():
            raise serializers.ValidationError("Only characters are allowed.")
        elif len(value) > 20:
            raise serializers.ValidationError("Max length should be 20 characters.")
        return value

    def validate(self, data):
        """Object level validation"""
        department = data.get('department')
        if department.name in ["Bakery"]:
            raise serializers.ValidationError(
                "No more categories allowed under this department. Please select other department")

        return data


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'



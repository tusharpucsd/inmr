from django.db import models


class Location(models.Model):
    """
    Model for Location Management
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    """
    Model for Department Management
    """
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model for Category Management
    """
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    Model for SubCategory Management
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SKUDataMapping(models.Model):
    """
    Model for SKU DATA mapping Management
    """
    sku = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)



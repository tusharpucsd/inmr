from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Location, Department, Category, SubCategory, SKUDataMapping
from .serializers import LocationSerializer, DepartmentSerializer, CategorySerializer, SubCategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Location model
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDetailView(APIView):
    """
    View for Location detail. Returns serialized data based on the id's provided in the url.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_serializer_class(self):
        """
        Returns the serializer class based on the id's provided in the url.
        """
        location = self.kwargs.get('location_id')
        department = self.kwargs.get('department_id')
        category = self.kwargs.get('category_id')
        subcategory = self.kwargs.get('subcategory_id')

        if subcategory or all([location, department, category]):
            serializer = SubCategorySerializer
        elif location and department:
            serializer = CategorySerializer
        elif location:
            serializer = DepartmentSerializer
        else:
            serializer = LocationSerializer
        return serializer

    def get_queryset(self):
        """
        Returns the queryset based on the id's provided in the url.
        """
        location = self.kwargs.get('location_id')
        department = self.kwargs.get('department_id')
        category = self.kwargs.get('category_id')
        subcategory = self.kwargs.get('subcategory_id')

        if subcategory:
            queryset = SubCategory.objects.filter(id=subcategory, category_id=category,
                                                  category_id__department_id=department,
                                                  category_id__department_id__location_id=location)
        elif all([location, department, category]):
            queryset = SubCategory.objects.filter(category_id=category, category_id__department_id=department,
                                                  category_id__department_id__location_id=location)
        elif all([location, department]):
            queryset = Category.objects.filter(department_id=department, department_id__location_id=location)
        elif location:
            queryset = Department.objects.filter(location_id=location)
        else:
            queryset = Location.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Handles GET request and returns serialized data.
        """
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentDetailsAPIView(APIView):
    """
    Endpoint for managing department details.
    POST request: /departments/
    GET request: /departments/
    GET request with pk: /departments/<pk>/
    PUT request: /departments/<pk>/
    DELETE request: /departments/<pk>/
    """
    def post(self, request):
        """
        Handles a POST request to create a new department.
        """
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        """
        Retrieves a department object by its primary key (pk) and raises a 404 error if the object does not exist.
        """
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def get(self, request, pk=None):
        """
        Handles a GET request to retrieve a department or a list of departments.
        """
        if pk:
            department = self.get_object(pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)
        else:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        """
        Handles a PUT request to update a department.
        """
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles a DELETE request to delete a department.
        """
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Category model
    Endpoints:
    - `/category/` (GET, POST)
    - `/category/{pk}/` (GET, PUT, DELETE)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new category instance
        """
        data = request.data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a category instance
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Updates a category instance
        """
        partial = kwargs.pop('partial', False)
        try:
            object = self.get_object()
        except Category.DoesNotExist:
            raise HTTP_404_NOT_FOUND
        serializer = self.get_serializer(object, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a category instance
        """
        obj = self.get_object()
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryView(APIView):
    """
    API endpoint for SubCategory management.
    """
    def get_object(self, pk):
        return get_object_or_404(SubCategory, pk=pk)

    def get(self, request, pk=None):
        """
        Retrieve a SubCategory instance.
        """
        if pk:
            subcategory = self.get_object(pk)
            serializer = SubCategorySerializer(subcategory)
            return Response(serializer.data)
        else:
            subcategory = SubCategory.objects.all()
            serializer = SubCategorySerializer(subcategory, many=True)
            return Response(serializer.data)

    def post(self, request):
        """
        Create a SubCategory instance.
        """
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update a SubCategory instance.
        """
        subcategory = self.get_object(pk)
        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a SubCategory instance.
        """
        subcategory = self.get_object(pk)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_skus_by_meta_data(request):
    """
    Retrieve a list of SKUs based on the provided meta data.
    The meta data includes location, department, category, and subcategory.
    parameters:
          location(string): The location of the SKU.
          department(string): The department of the SKU.
          category(string): The category of the SKU.
          subcategory(string): The subcategory of the SKU.
    """
    location = request.query_params.get('location')
    department = request.query_params.get('department')
    category = request.query_params.get('category')
    subcategory = request.query_params.get('subcategory')
    skus = SKUDataMapping.objects.filter(
        location__name=location, department__name=department, category__name=category, subcategory__name=subcategory
    )
    data = [[sk.sku, sk.location.name, sk.department.name, sk.category.name, sk.subcategory.name] for sk in skus]
    return Response(data)

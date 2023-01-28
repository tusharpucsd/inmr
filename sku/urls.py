from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, LocationDetailView, DepartmentDetailsAPIView, CategoryViewSet, \
    get_skus_by_meta_data, SubCategoryView

router = DefaultRouter()
router.register('location', LocationViewSet)
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),

    # URL pattern for location and department details
    path("location/<int:location_id>/department/", LocationDetailView.as_view(), name='location-department'),

    # URL pattern for location, department and category details
    path("location/<int:location_id>/department/<int:department_id>/category/", LocationDetailView.as_view(), name='location-department-category'),

    # URL pattern for location, department, category and subcategory details
    path("location/<int:location_id>/department/<int:department_id>/category/<int:category_id>/subcategory/", LocationDetailView.as_view(), name="category-subcategory"),

    # URL pattern for location, department, category, subcategory details and subcategory id
    path("location/<int:location_id>/department/<int:department_id>/category/<int:category_id>/subcategory/<int:subcategory_id>/", LocationDetailView.as_view(), name='subcategory'),

    # URL pattern for department list & details
    path('departments/', DepartmentDetailsAPIView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailsAPIView.as_view(), name='department-detail'),

    # URL pattern for getting SKUs by meta data
    path('get_skus_by_meta_data/', get_skus_by_meta_data, name='get_skus_by_meta_data'),

    # URL pattern for SubCategory & SubCategory with primary key
    path('subcategory/', SubCategoryView.as_view()),
    path('subcategory/<int:pk>/', SubCategoryView.as_view()),
]






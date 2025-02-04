"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# We register our Recipe ViewSet with the router. It will automatically generate the URL patterns for the ViewSet.
# I.e., it will autogenerate urls depending on the functionality that's enabled on the viewset,
# and since we are using the ModelViewSet, it will autogenerate the urls for the list, create, update, delete, etc.
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]

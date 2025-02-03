"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


# The app_name is used to identify the app in the URL template tag.
# # When we use reverse() in the tests, we can use the app_name to identify the URL.
app_name = 'user'

urlpatterns = [
  path('create/', views.CreateUserView.as_view(), name='create'),
  path('token/', views.CreateTokenView.as_view(), name='token'),
]

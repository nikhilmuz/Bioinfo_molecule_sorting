from django.conf.urls import url
from .views import *
urlpatterns = [
  url(r'^run/$', Run.as_view(), name='Run Script'),
  url(r'^upload/$', UI.as_view(), name='UI'),
]
from django.urls import path
from . import views
urlpatterns = [
    path('', views.upload_csv),
    path('data', views.printdata, name='data'),
    path('trendspecial', views.trendspecial, name='trendspeacial'),
    path('trenddual', views.trenddual, name='trenddual')

]

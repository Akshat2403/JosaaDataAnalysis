from django.urls import path
from . import views
urlpatterns = [
    path('',views.upload_csv),
    path('base',views.base,name='base'),
    path('data',views.printdata,name = 'data'),
    path('dig-q1',views.dig_q1,name = 'dig_q1'),
    path('dev-q3',views.dev_q3,name = 'dev_q3'),
    path('dig-q2',views.dig_q2,name = 'dig_q2'),
    path('trendspecial', views.trendspecial, name='trendspeacial'),
    path('trenddual', views.trenddual, name='trenddual')
]

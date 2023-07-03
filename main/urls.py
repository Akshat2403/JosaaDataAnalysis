from django.urls import path
from . import views
urlpatterns = [
    path('',views.upload_csv),
    path('base',views.base,name='base'),
    path('data',views.printdata,name = 'data'),
    path('dig-q1',views.dig_q1,name = 'dig_q1'),
    path('mohit-q1',views.Moh_q1,name = 'Moh_q1'),
    path('mohit-q1exp',views.Moh_q1exp,name = 'Moh_q1exp'),
    path('mohit-q1exp2',views.Moh_q1exp2,name = 'Moh_q1exp2'),
    path('mohit-q2',views.branch_popularity,name = 'Moh_q2'),
    path('dig-q2',views.dig_q2,name = 'dig_q2'),
    path('trendspecial', views.trendspecial, name='trendspeacial'),
    path('trenddual', views.trenddual, name='trenddual')
]


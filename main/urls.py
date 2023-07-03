from django.urls import path
from . import views
urlpatterns = [
    path('',views.upload_csv),
    path('data',views.printdata,name = 'data'),
    path('dig-q1',views.dig_q1,name = 'dig_q1'),
    path('sid-q1',views.sid_q1,name = 'sid_q1'),
    path('sid-q2',views.sid_q2,name = 'sid_q2'),
    path('sid-q3',views.sid_q3,name = 'sid_q3'),
]
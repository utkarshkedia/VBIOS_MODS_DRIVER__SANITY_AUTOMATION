from django.urls import path
from .views import GPUspecs,test,home,Test_Systems,scheduled

urlpatterns = [
    path('',home),
    path('test',test),
    path('specs/',GPUspecs.as_view()),
    path('systems/',Test_Systems.as_view()),
    path('scheduled/',scheduled),
   # path('test/<int:id>/',test),
    ]

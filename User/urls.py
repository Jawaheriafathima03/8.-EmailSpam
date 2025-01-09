from django.urls import path 
from .import views 

urlpatterns=[ 
    path('',views.index,name='index'),
    path('register',views.register,name='reg'),
    path('login',views.login,name='login'),
    path('spam',views.spam,name='spam'),
    path('predict',views.predict,name='predict'),
    path('logout',views.logout,name='logout')
]
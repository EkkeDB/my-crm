
from django.urls import path
from .views import live_search


from . import views

urlpatterns = [
    path('', views.home, name=""),

    path('index', views.index, name="index"),

    path('charts', views.charts, name="charts"),

    path('login', views.login, name="login"),

    path('my-login', views.my_login, name="my-login"),

    path('register', views.register, name="register"),

    path('register2', views.register2, name="register2"),

    path('password', views.password, name="password"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('401', views.unauth, name="unauth"),

    path('404', views.notfound, name="notfound"),
    
    path('tables', views.tables, name="tables"),

    path('crypto', views.crypto, name="crypto"),

    path('mycrypto', views.mycrypto, name="mycrypto"),

    path('contracts', views.contracts, name="contracts"),

    path('live_search/', live_search, name='live_search'),
    
]

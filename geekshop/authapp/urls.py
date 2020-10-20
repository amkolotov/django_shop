from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    # path('login/', authapp.login, name='login'),
    path('login', authapp.UserLoginView.as_view(), name='login'),

    path('logout/', authapp.logout, name='logout'),
    path('edit/', authapp.edit, name='edit'),
    path('register/', authapp.register, name='register'),
]
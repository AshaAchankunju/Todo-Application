"""
URL configuration for todoapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tdapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("todos/all/",views.TodoListView.as_view(),name="todo-all"),
    path("todos/add/",views.TodoCreateView.as_view(),name="todo-add"),
    path("todos/<int:pk>/",views.TodoDetailView.as_view(),name="todo-detail"),
    path("todos/<int:pk>/remove/",views.TodoDeleteView.as_view(),name="todo-remove"),
    path("todos/<int:pk>/change/",views.TodoUpdateView.as_view(),name="todo-change"),
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("signin/",views.SignInView.as_view(),name="signin"),
    path("signout/",views.SignOutView.as_view(),name="signout")
]


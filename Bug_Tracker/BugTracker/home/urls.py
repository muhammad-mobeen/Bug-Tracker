"""BugTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from home import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('', views.dashboard, name='home'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("teams/", views.teams, name="teams"),
    path("add-ticket/", views.add_ticket, name="add-ticket"),
    path("update-status/<int:id>/<int:is_completed>/", views.update_status, name="update-status"),
    path("edit-ticket/<int:id>/", views.edit_ticket, name="edit-ticket"),
    path("update-ticket/<int:id>/", views.update_ticket, name="update-ticket"),
    path("delete-ticket/<int:id>/", views.delete_ticket, name="delete-ticket"),
    # path('index/', views.dashboard, name='home'),
    # path("show/", views.show, name="show"),
    # path("sort-tickets/", views.sorter, name="sort-tickets"),
]

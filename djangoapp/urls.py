from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns =[
    #path('', views.HomePageView, name="kotisivu")
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
]

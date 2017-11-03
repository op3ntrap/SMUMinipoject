from django.conf.urls import url , include
from . import views
from django.http import HttpResponse

# Testing Template
# def er(request):
#     return HttpResponse(":fasdofs")

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/$', views.logout),
    # url(r'test/$', er)
]
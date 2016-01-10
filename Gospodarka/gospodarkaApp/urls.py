from django.conf.urls import * 
from Gospodarka.gospodarkaApp.views import *

urlpatterns = patterns('', 
#url(r'^(?P<emp_id>\d+)/(?P<dept_name>\w+)/(?P<dept_id>\d+)/$' , newdept), 
url(r'^$', index),
url(r'^afterLogin', afterLogin),
url(r'^register', register, name='register'),
url(r'^login', user_login, name='login'),
)
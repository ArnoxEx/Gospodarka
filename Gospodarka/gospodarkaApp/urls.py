from django.conf.urls import *
from Gospodarka.gospodarkaApp.views import *

urlpatterns = patterns('',
#url(r'^(?P<emp_id>\d+)/(?P<dept_name>\w+)/(?P<dept_id>\d+)/$' , newdept),
url(r'^$',                                  index),
url(r'^register',                           register,       name='register'),
url(r'^login',                              user_login,     name='login'),
url(r'^logout',                             user_logout,    name='logout'),
url(r'^edit_profile',                       edit_profile,   name='edit_profile'),
url(r'^objects',                            objects,        name='objects'),
url(r'^add_object',                         add_object,     name='add_object'),
url(r'^edit_object/(?P<object_id>\w+)/$',   edit_object,    name='edit_object'),
url(r'^user_objects',                       user_objects,   name='user_objects'),
url(r'^object/(?P<object_id>\w+)/$',        object,         name='object'),
url(r'^events',                             eventsTable,    name='add_object'),
url(r'^orders',                             orders,         name='orders'),
)

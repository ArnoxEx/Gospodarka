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
url(r'^remove_object/(?P<object_id>\w+)/$', remove_object,  name='remove_object'),
url(r'^user_objects',                       user_objects,   name='user_objects'),
url(r'^object/(?P<object_id>\w+)/$',        object,         name='object'),
url(r'^events',                             eventsTable,    name='eventsTable'),
url(r'^event/(?P<event_id>\w+)/$',          event,          name='event'),
url(r'^add_event/(?P<object_id>\w+)/$',     add_event,      name='add_event'),
url(r'^edit_event/(?P<event_id>\w+)/$',     edit_event,     name='edit_event'),
url(r'^remove_event/(?P<event_id>\w+)/$',   remove_event,   name='remove_event'),
url(r'^orders',                             orders,         name='orders'),
url(r'^add_order/(?P<event_id>\w+)/$',      add_order,      name='add_order'),
)

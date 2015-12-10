from django.conf.urls import include, url, patterns
from django.contrib import admin
from settings import ADMIN_BASE

from . import views

base_pattern = '^{}'.format(ADMIN_BASE)

urlpatterns = [
    ### ADMIN ###
    url(base_pattern,
        include(patterns('',
                         url(r'^$', views.home, name='home'),
                         url(r'^django_admin/', include(admin.site.urls)),
                         url(r'^spam/', include('admin.spam.urls', namespace='spam')),
                         url(r'^auth/', include('admin.common_auth.urls', namespace='auth')),
                         url(r'^prereg/', include('admin.pre_reg.urls', namespace='pre_reg')),
                         url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                            views.password_reset_confirm_custom, name='password_reset_confirm'),
                         url(r'^reset/done/$', views.password_reset_done,
                            name='password_reset_complete'),
                         )
                )
        )
]

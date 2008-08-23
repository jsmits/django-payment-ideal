from django.conf.urls.defaults import *

urlpatterns = patterns('ideal.views',
    url(r'^status/', 'status', name="ideal_return_url"),
    url(r'^test_form/', 'test_form'), # comment out for production
)

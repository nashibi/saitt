from django.urls import path

from website.views import home_view, post_related_ajax, ajax_cat_post

app_name = 'website'

urlpatterns = [
    path('', home_view, name='home'),
    path('related_data/', post_related_ajax.as_view(), name='related_data'),
    path('ajax_cat_post/', ajax_cat_post.as_view(), name='ajax_cat_post')
]

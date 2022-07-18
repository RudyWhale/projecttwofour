from django.urls import path, include

from . import views
from . import ajax_views

urlpatterns = [
    path('', views.main, name='main'),

    # ajax paths
    path('ajax/authenticate', ajax_views.authenticate, name='authenticate'),
    path('ajax/get_guest_content', ajax_views.get_guest_content, name='get_guest_content'),
    path('ajax/update_guest_status', ajax_views.update_guest_status, name='update_guest_status'),
]

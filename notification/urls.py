from django.urls import path
from .views import (
    notification_view,



)

app_name = 'notification'
urlpatterns = [
    path('<int:pk>/', notification_view, name = 'notification-view'),

]
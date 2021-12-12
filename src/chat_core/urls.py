
from django.urls import path,include
from django.views.generic.base import RedirectView



urlpatterns = [
    path('chat/',include('chat.urls',namespace = 'chat')),
    path('', RedirectView.as_view(url='/chat/', permanent=True))
]

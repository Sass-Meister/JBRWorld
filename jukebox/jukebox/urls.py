"""jukebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from JukeBox_Republic.viewfiles.homepage import Index
from JukeBox_Republic.viewfiles.party import Party
from JukeBox_Republic.viewfiles.createparty import CreateParty
from JukeBox_Republic.viewfiles.callback import Callback
from JukeBox_Republic.viewfiles.currentlyplaying import currentlyplaying
from JukeBox_Republic.viewfiles.addsong import addSong

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', Callback.as_view()),
    path('party/create', CreateParty.as_view()),
    path('party/', Party.as_view()),
    path('host/', Party.as_view()),
    path('host/refresh/', currentlyplaying.as_view()),
    path('party/refresh/', currentlyplaying.as_view()),
    path('', Index.as_view()),
    path('addsong/', addSong.as_view())
]

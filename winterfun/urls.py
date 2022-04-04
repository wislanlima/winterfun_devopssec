"""winterfun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from frontend.views import index
from winterfun.views import wislan, auth

#TODO AQUI ONDE PARO O CTRZ
urlpatterns = [
    path("", index, name="testeindex"),
    path("auth/", auth, name="auth"),
    path("from/", wislan, name='testaaaaa'),


    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    # path('index/', include('frontend.urls')),
    path("profile/", include("profiles.urls")),
    path("post/", include("posts.urls")),
    path("frontend/", include("frontend.urls")),
    path("booking/", include("booking.urls")),
    path("event/", include("events.urls")),

    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    # path('profile/', users_view.ProfileView.as_view(), name='profile-user'),
    #    path('<username>/', UserProfile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

admin.site.site_header = "Winter Fun Sports -  Admin"
admin.site.site_title = "Winter Fun Sports Admin Portal"
admin.site.index_title = "Welcome to the Winter Fun Sports Portal"


from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include("accounts.urls")),
    path("api/",include("chat.urls")),
    path("friends/",include("friends.urls"))
]
urlpatterns+=[ path("schema/",Schema.as_view()),
              ]
if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),

    ] + urlpatterns
from django.conf.urls import url

from URLInspectorApp.views import IndexView

app_name = "URLInspectorApp"

urlpatterns = [
    url(r"^(?:index)?$", IndexView.as_view(), name="index"),
]

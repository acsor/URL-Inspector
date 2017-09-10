from django.conf.urls import url

import views


app_name = "URLInspectorApp"

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^inspection/(?P<pk>\d+)", views.InspectionView.as_view(), name="inspection"),
]

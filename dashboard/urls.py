from django.urls import path
from .views import dashboard, upload, download_doc, resources, about, services, contact

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("upload/", upload, name="upload"),
    path("resources/", resources, name="resources"),
    path("doc/<int:pk>/download/", download_doc, name="download_doc"),
    path("about/", about, name="about"),
    path("services/", services, name="services"),
    path("contact/", contact, name="contact"),
]

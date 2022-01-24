""" The URL mappings. """

from django.urls import re_path, path
from django.contrib import admin
from datasets.views import Mint, Url
from doi_site.views import DoiList, Domains, HomeView, Notes, Login, Logout
from mds.views import DoiView, MetadataView, MediaView


# pylint: disable=invalid-name
urlpatterns = [
    re_path(r"^$", HomeView.as_view(), name="home"),
    re_path(r"^index$", HomeView.as_view(), name="index"),
    re_path(r"^admin/", admin.site.urls),

    # web
    re_path(r"^doilist$", DoiList.as_view(), name="doi_list"),
    re_path(r"^domains$", Domains.as_view(), name="domains"),
    re_path(r"^mint$", Mint.as_view(), name="mint"),
    path('mint/<path:doi>', Url.as_view(), name="minturl"),
    re_path(r"^notes$", Notes.as_view(), name="notes"),

    # MDS
    re_path(r"^doi$", DoiView.as_view(), name="doi_view"),
    re_path(r"^doi/", DoiView.as_view(), name="doi_view"),
    re_path(r"^metadata$", MetadataView.as_view(), name="metadata_view"),
    re_path(r"^metadata/", MetadataView.as_view(), name="metadata_view"),
    re_path(r"^media/", MediaView.as_view(), name="media_view"),

    re_path(r"^accounts/login/$", Login.as_view(), name="login"),
    re_path(r"^logout/$", Logout.as_view(), name="logout"),

    re_path(r"", HomeView.as_view()),
]

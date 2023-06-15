from rest_framework.urls import path 
from JobBoard.api.views import JobOfferListView, JobOfferDetailView

urlpatterns = [
    path("jobs/", JobOfferListView.as_view(), name="job-list"),
    path("jobs/<int:pk>", JobOfferDetailView.as_view(), name="job-detail")
]

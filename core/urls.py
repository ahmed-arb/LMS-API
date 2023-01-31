"""
Urls for Core app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import BookLoanViewSet, BookRequestViewSet, BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"loans", BookLoanViewSet, basename="BookLoan")
router.register(r"book_requests", BookRequestViewSet, basename="BookRequest")

urlpatterns = [
    path("", include(router.urls)),
]

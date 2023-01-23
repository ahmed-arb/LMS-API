from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import BookLoanViewSet, BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"loans", BookLoanViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

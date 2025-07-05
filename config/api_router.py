from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from digimedix_be.core.apis.views import SpecialtyViewSet
from digimedix_be.users.apis.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("specialties", SpecialtyViewSet)


app_name = "api"
urlpatterns = router.urls

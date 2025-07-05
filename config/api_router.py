from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from digimedix_be.core.apis.views import SpecialtyViewSet
from digimedix_be.provider_groups.apis.views import ProviderGroupViewSet
from digimedix_be.users.apis.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("specialties", SpecialtyViewSet)
router.register("provider-groups", ProviderGroupViewSet)


app_name = "api"
urlpatterns = router.urls

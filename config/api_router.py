from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from azura_be.core.apis.views import SpecialtyViewSet
from azura_be.locations.apis.views import LocationViewSet
from azura_be.provider_groups.apis.views import DepartmentViewSet, ProviderGroupViewSet
from azura_be.users.apis.views import UserViewSet, BusinessAccountSignUpViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("auth", BusinessAccountSignUpViewSet)
router.register("specialties", SpecialtyViewSet)
router.register("provider-groups", ProviderGroupViewSet)
router.register("departments", DepartmentViewSet)
router.register("locations", LocationViewSet)


app_name = "api"
urlpatterns = router.urls

from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from azura_be.core.apis.views import SpecialtyViewSet, ICDCodeViewSet, ConditionViewSet, CPTCodeViewSet, HCPCSCodeViewSet, RxCodeViewSet, LoincCodeViewSet
from azura_be.locations.apis.views import LocationViewSet
from azura_be.provider_groups.apis.views import DepartmentViewSet, ProviderGroupViewSet
from azura_be.users.apis.views import UserViewSet, BusinessAccountSignUpViewSet
from azura_be.business_accounts.apis.views import AccountConfigurationViseSet
from azura_be.patients.apis.views import PatientViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("patients", PatientViewSet)
router.register("auth", BusinessAccountSignUpViewSet)
router.register("specialties", SpecialtyViewSet)
router.register("provider-groups", ProviderGroupViewSet)
router.register("departments", DepartmentViewSet)
router.register("locations", LocationViewSet)
router.register("icd-codes", ICDCodeViewSet)
router.register("conditions", ConditionViewSet)
router.register("cpt-codes", CPTCodeViewSet)
router.register("hcpcs-codes", HCPCSCodeViewSet)
router.register("rx-codes", RxCodeViewSet)
router.register("loinc-codes", LoincCodeViewSet)
router.register("account", AccountConfigurationViseSet, basename="account-configurations")


app_name = "api"
urlpatterns = router.urls

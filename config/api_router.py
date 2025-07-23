from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from azura_be.core.apis.views import SpecialtyViewSet, ICDCodeViewSet, ConditionViewSet, CPTCodeViewSet, HCPCSCodeViewSet, RxCodeViewSet, LoincCodeViewSet
from azura_be.locations.apis.views import LocationViewSet
from azura_be.provider_groups.apis.views import DepartmentViewSet, ProviderGroupViewSet
from azura_be.users.apis.views import UserViewSet, BusinessAccountSignUpViewSet
from azura_be.business_accounts.apis.views import AccountConfigurationViseSet
from azura_be.patients.apis.views import PatientViewSet
from azura_be.educations.apis.views import EducationViewSet
from azura_be.plans.apis.views import FormViewSet, PlanViewSet
from azura_be.core.apis.views import FrequencyViewSet, CategoryViewSet, TagViewSet, FlagViewSet
from azura_be.tasks.apis.views import TaskViewSet
from azura_be.appointments.apis.views import AppointmentViewSet
from azura_be.communications.apis.views import ThreadViewSet, CommunicationMessageViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("appointments", AppointmentViewSet)
router.register("threads", ThreadViewSet)
router.register("communications", CommunicationMessageViewSet)
router.register("tasks", TaskViewSet)
router.register("forms", FormViewSet)
router.register("plans", PlanViewSet)
router.register("frequencies", FrequencyViewSet)
router.register("categories", CategoryViewSet)
router.register("tags", TagViewSet)
router.register("flags", FlagViewSet)
router.register("patients", PatientViewSet)
router.register("educations", EducationViewSet)
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

from djstripe.models import Price
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from azura_be.billings.setup_plans import create_card_intent
from azura_be.billings.setup_plans import create_stripe_card_for_account
from azura_be.billings.setup_plans import subscribe_plan_for_account
from azura_be.business_accounts.apis.serializers import AccountConfigurationSerializer
from azura_be.business_accounts.apis.serializers import CardIntentSerializer
from azura_be.business_accounts.apis.serializers import CommunicationTemplateSerializer
from azura_be.business_accounts.apis.serializers import EmailConfigurationSerializer
from azura_be.business_accounts.apis.serializers import PlanSubscriptionSerializer
from azura_be.business_accounts.apis.serializers import PricePlanSerializer
from azura_be.business_accounts.apis.serializers import SMSConfigurationSerializer
from azura_be.business_accounts.apis.serializers import VitalAlertConfigurationSerializer
from azura_be.business_accounts.models import AccountConfiguration
from azura_be.business_accounts.models import BusinessAccount
from azura_be.business_accounts.models import CommunicationTemplate
from azura_be.business_accounts.models import EmailConfiguration
from azura_be.business_accounts.models import SMSConfiguration
from azura_be.business_accounts.models import VitalAlertConfiguration


class AccountConfigurationViseSet(viewsets.GenericViewSet):
    queryset = BusinessAccount.objects.all()
    serializer_class = CommunicationTemplateSerializer

    def get_serializer_class(self):
        if self.action == "email_configuration":
            return EmailConfigurationSerializer
        if self.action == "sms_configuration":
            return SMSConfigurationSerializer
        if self.action == "communication-templates":
            return CommunicationTemplateSerializer(many=True)
        if self.action == "card_intent":
            return CardIntentSerializer
        if self.action == "configurations":
            return AccountConfigurationSerializer
        if self.action == "create_vital_alert_configuration":
            return VitalAlertConfigurationSerializer
        if self.action == "vital_alert_configurations":
            return VitalAlertConfigurationSerializer(many=True)
        if self.action == "add_card":
            return PlanSubscriptionSerializer
        return super().get_serializer_class()

    @extend_schema(responses=PricePlanSerializer(many=True))
    @action(detail=False, methods=["GET"], url_path="plans", pagination_class=None)
    def get_plans(self, *args, **kwargs):
        return Response(PricePlanSerializer(Price.objects.all().distinct("unit_amount")).data)

    @action(detail=True, methods=["GET"], url_path="card-intent")
    def card_intent(self, request, *args, **kwargs):
        business_account = self.get_object()
        if request.user.id != business_account.created_by:
            return Response(
                {"detail": "You do not have permission to perform this action"},
                status=403,
            )

        setup_intent = create_card_intent(
            business_account.stripe_customer,
            business_account,
        )
        return Response({"client_secret": setup_intent.client_secret})

    @action(detail=True, methods=["POST"], url_path="add-card")
    def add_card(self, request, *args, **kwargs):
        business_account = self.get_object()
        serializer = PlanSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        price = serializer.validated_data.get("price")
        card_id = serializer.validated_data.get("card_id")
        create_stripe_card_for_account(business_account, card_id)
        subscribe_plan_for_account(
            business_account.stripe_customer,
            price,
            business_account,
        )
        return Response({"detail": "Plan subscribed successfully"})

    @action(detail=False, methods=["GET", "POST"], url_path="email-configuration")
    def email_configuration(self, request, *args, **kwargs):
        email_config = EmailConfiguration.objects.filter(
            business_account=request.business_account,
        ).first()

        if request.method == "POST":
            serializer = EmailConfigurationSerializer(
                data=request.data,
                instance=email_config,
                partial=email_config is not None,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(business_account=request.business_account)
            return Response(serializer.data)
        return Response(EmailConfigurationSerializer(email_config).data)

    @action(detail=False, methods=["GET", "POST"], url_path="sms-configuration")
    def sms_configuration(self, request, *args, **kwargs):
        sms_config = SMSConfiguration.objects.filter(
            business_account=request.business_account,
        ).first()

        if request.method == "POST":
            serializer = SMSConfigurationSerializer(
                data=request.data,
                instance=sms_config,
                partial=sms_config is not None,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(business_account=request.business_account)
            return Response(serializer.data)
        return Response(SMSConfigurationSerializer(sms_config).data)

    @action(
        detail=False,
        methods=["GET", "POST"],
        url_path="create-communication-template",
    )
    def create_communication_temaplate(self, request, *args, **kwargs):
        serializer = CommunicationTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(business_account=request.business_account)
        return Response(serializer.data)

    @action(detail=False, methods=["GET", "POST"], url_path="communication-templates")
    def communication_temaplates(self, request, *args, **kwargs):
        templates = CommunicationTemplate.objects.filter(
            business_account=request.business_account,
        )
        page = self.paginate_queryset(templates)
        serializer = CommunicationTemplateSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=["GET", "POST"],
        url_path="configurations",
    )
    def configurations(self, request, *args, **kwargs):
        obj = AccountConfiguration.objects.get_or_create(
            business_account=request.business_account,
        )

        if request.method == "GET":
            return Response(AccountConfigurationSerializer(obj).data)

        serializer = AccountConfigurationSerializer(data=request.data, instance=obj)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["POST"],
        url_path="create-vital-alert-configuration",
    )
    def create_vital_alert_configuration(self, request, *args, **kwargs):
        serializer = VitalAlertConfigurationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vital_alert = VitalAlertConfiguration.objects.filter(
            business_account=request.business_account,
            vital_type=serializer.validated_data.get("vital_type"),
        ).first()
        serializer.instance = vital_alert
        serializer.save(business_account=request.business_account)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="vital-alert-configurations",
        pagination_class=None,
    )
    def vital_alert_configurations(self, request, *args, **kwargs):
        vital_alerts = VitalAlertConfiguration.objects.filter(
            business_account=request.business_account,
        )
        serializer = VitalAlertConfigurationSerializer(vital_alerts, many=True)
        return Response(serializer.data)

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_tenants.models import TenantMixin
from django.core.validators import RegexValidator
from djstripe.models import Customer, Price, Card

from azura_be.base.constants import CommunicationTemplateTypeChoices, CommunicationTemplateUserTypeChoices, DisciplineChoices, EmailConfigurationProtocolChoices, SMSConfigurationProviderChoices
from azura_be.base.models import BaseModel
from azura_be.billings.setup_plans import create_stripe_customer_for_account


domain_validator = RegexValidator(
    regex=r'^((localhost|\d{1,3}(\.\d{1,3}){3}|([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}))(:\d{1,5})?$',
    message="Enter a valid domain, e.g., example.com"
)


class EnabledDomain(BaseModel):
    domain = models.CharField(validators=[domain_validator], unique=True)

    def __str__(self):
        return self.domain


class BusinessAccount(TenantMixin, BaseModel):
    name = models.CharField(max_length=255, unique=True)
    discipline_service = models.CharField(max_length=60, choices=DisciplineChoices)
    address = models.JSONField()
    contact = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$",
                message="Contact format must be one of (XXX) XXX-XXXX or XXX-XXX-XXXX",
                code="invalid_phone",
            )
        ],
    )
    email = models.EmailField(unique=True)
    website = models.URLField(unique=True)
    grace_code = models.CharField(max_length=255)
    web_address = models.CharField(null=True, unique=True, validators=[domain_validator])
    initial_completed = models.BooleanField(default=False)

    # Stripe Resources
    stripe_customer = models.OneToOneField(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='account'
    )
    stripe_price = models.ForeignKey(
        Price, on_delete=models.SET_NULL, null=True, blank=True, related_name='accounts'
    )
    stripe_cards = models.ManyToManyField(Card, related_name='cards')
    default_stripe_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True, related_name='default_account_cards')

    auto_create_schema = False

    def save(self, *args, **kwargs):
        if not self.schema_name:
            self.set_schema_name()
        if self.web_address:
            self.web_address = self.web_address.lower()
            self.validate_web_address()
        if self.initial_completed:
            self.auto_create_schema = True
        if self.stripe_customer is None:
            self.create_stripe_user()
        return super().save(*args, **kwargs)

    def create_stripe_user(self):
        create_stripe_customer_for_account(self, self.email)

    def set_schema_name(self):
        self.schema_name = str(self.id).replace("-", "_")

    def validate_web_address(self):
        if EnabledDomain.objects.filter(domain=self.web_address).exists():
            raise ValidationError(message={"web_address": "Please choose a correct we address"})
        for enabled_domain in EnabledDomain.objects.all():
            if self.web_address.endswith(enabled_domain.domain):
                return True
        raise ValidationError(message={"web_address": "Please choose a correct we address"})


class EmailConfiguration(BaseModel):
    business_account = models.OneToOneField(BusinessAccount, on_delete=models.CASCADE, related_name="email_configuration")
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150, blank=True)
    from_email = models.CharField(max_length=150)
    protocol = models.CharField(max_length=5, choices=EmailConfigurationProtocolChoices)
    authentication = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.authentication:
            errors = {}
            if not self.username:
                errors.update({"username": "Username is required"})
            if not self.password:
                errors.update({"password": "Password is required"})
            if errors:
                raise ValidationError(message=errors)
        return super().save(*args, **kwargs)


class SMSConfiguration(BaseModel):
    business_account = models.OneToOneField(BusinessAccount, on_delete=models.CASCADE, related_name="sms_configuration")
    provider = models.CharField(max_length=15, choices=SMSConfigurationProviderChoices)
    from_number = models.CharField(max_length=15)
    cred_json = models.JSONField()


class CommunicationTemplate(BaseModel):
    business_account = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, related_name="communication_templates")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=CommunicationTemplateTypeChoices)
    user_type = models.CharField(max_length=15, choices=CommunicationTemplateUserTypeChoices)
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    active = models.BooleanField(True)

    def save(self, *args, **kwargs):
        if self.type == CommunicationTemplateTypeChoices.EMAIL.name and not self.subject:
            raise ValidationError(message={"subject": "Subject is required"})
        if self.type == CommunicationTemplateTypeChoices.SMS.name and self.subject:
            raise ValidationError(message={"subject": "Subject is not accepteble"})
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = (("name", "type", "business_account"),)

class CommunicationTemplateVersion(BaseModel):
    template = models.ForeignKey(CommunicationTemplate, on_delete=models.CASCADE, related_name="versions")
    new_subject = models.CharField(max_length=255, blank=True)
    new_content = models.TextField()
    old_subject = models.CharField(max_length=255, blank=True)
    old_content = models.TextField()

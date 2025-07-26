from django_otp.plugins.otp_email.models import EmailDevice


class MobileDevice(EmailDevice):
    email = None

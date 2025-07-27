from allauth.account.models import app_settings
from django.core.signing import BadSignature
from django.core.signing import SignatureExpired
from django.core.signing import TimestampSigner
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.response import Response

from azura_be.mobile_devices.models import MobileDevice
from azura_be.users.models import User


class TwoFactorAuthService:
    def __init__(self):
        self.signer = TimestampSigner(salt=app_settings.SALT)

    def _user_devices(self, user):
        devices = {}
        email = EmailDevice.objects.filter(user=user).first()
        mobile = MobileDevice.objects.filter(user=user).first()
        authenticator = TOTPDevice.objects.filter(user=user).first()
        if email:
            devices.update({"email": email.id})
        if mobile:
            devices.update({"mobile": mobile.id})
        if authenticator:
            devices.update({"authenticator": authenticator.id})
        return devices

    def _user_device_by_id(self, user, device_id, device_type):
        if device_type == "email":
            return EmailDevice.objects.filter(user=user, id=device_id).first()
        if device_type == "authenticator":
            return TOTPDevice.objects.filter(user=user, id=device_id).first()
        return MobileDevice.objects.filter(user=user, id=device_id).first()

    def _user_signed_key(self, user):
        return self.signer.sign(str(user.uid))

    def _user_from_signed_key(self, key):
        try:
            user_uid = self.signer.unsign(key, max_age=600)
            return User.objects.get(uid=user_uid)
        except (User.DoesNotExist, User.MultipleObjectsReturned, SignatureExpired, BadSignature) as e:
            return Response({"detail": "Error occurred in signed key", "error": str(e)}, status=400)

    def get_devices_response(self, user):
        devices = self._user_devices(user)
        if not devices:
            return None
        return Response(
            {
                "devices": devices,
                "key": self._user_signed_key(user),
            },
        )

    def send_otp(self, signed_key, device_id, device_type):
        response_user = self._user_from_signed_key(signed_key)
        if not isinstance(response_user, User):
            return response_user
        user_device = self._user_device_by_id(response_user, device_id, device_type)
        if user_device is None:
            return Response({"detail": "User device not found"}, status=400)
        user_device.generate_challenge()
        return Response({"detail": f"OTP send to {device_type}"})

    def validate_otp(self, signed_key, device_id, device_type, otp):
        response_user = self._user_from_signed_key(signed_key)
        if not isinstance(response_user, User):
            return response_user
        user_device = self._user_device_by_id(response_user, device_id, device_type)
        if user_device is None:
            return Response({"detail": "User device not found"}, status=400)
        response = user_device.verify_token(otp)
        if not response:
            return Response({"detail": "OTP not Verified"}, status=400)
        return Response({"detail": "OTP Verified"})

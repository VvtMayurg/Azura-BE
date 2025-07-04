from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest

    from digimedix_be.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = f"{request.headers.get('Origin') or request.get_host()}/auth/confirm-email?key={emailconfirmation.key}"
        if "http://" not in url or "https://" not in url:
            url = f"https://{url}" if request.is_secure() else f"http://{url}"
        return url

    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def render_mail(self, template_prefix, email, context, headers=None):
        if "password_reset_url" in context:
            password_reset_url = context.get("password_reset_url")
            uid = password_reset_url.split("/")[-3]
            token = password_reset_url.split("/")[-2]
            password_reset_url = url = (
                f"{self.request.headers.get('Origin') or self.request.get_host()}/auth/forgot-password?uid={uid}&token={token}"
            )
            if (
                "http://" not in password_reset_url
                or "https://" not in password_reset_url
            ):
                password_reset_url = (
                    f"https://{password_reset_url}"
                    if self.request.is_secure()
                    else f"http://{password_reset_url}"
                )
            context["password_reset_url"] = password_reset_url
        return super().render_mail(template_prefix, email, context, headers)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user = super().populate_user(request, sociallogin, data)
        if not user.name:
            if name := data.get("name"):
                user.name = name
            elif first_name := data.get("first_name"):
                user.name = first_name
                if last_name := data.get("last_name"):
                    user.name += f" {last_name}"
        return user

import stripe
from django.core.management import call_command
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_plan_method():

    # Create Product
    starter_product = stripe.Product.create(name="Lite Plan")
    pro_product = stripe.Product.create(name="Premium Plan")

    # Create Monthly Prices
    stripe.Price.create(
        nickname="Monthly Lite Plan",
        unit_amount=4900,
        currency="usd",
        recurring={"interval": "month"},
        product=starter_product.id,
    )

    stripe.Price.create(
        nickname="Yearly Lite Plan",
        unit_amount=4900 * 12,
        currency="usd",
        recurring={"interval": "year"},
        product=starter_product.id,
    )

    stripe.Price.create(
        nickname="Monthly Premium Plan",
        unit_amount=8900,
        currency="usd",
        recurring={"interval": "month"},
        product=pro_product.id,
    )

    stripe.Price.create(
        nickname="Yearly Premium Plan",
        unit_amount=8900 * 12,
        currency="usd",
        recurring={"interval": "year"},
        product=pro_product.id,
    )

    call_command("djstripe_sync_models", "Product", "Price")

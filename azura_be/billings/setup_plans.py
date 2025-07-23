import stripe
from django.conf import settings
from django.core.management import call_command
from djstripe.models import Card
from djstripe.models import Customer

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


def create_card_intent(customer, account):
    return stripe.SetupIntent.create(
        customer=customer.id,
        payment_method_types=["card"],
        metadata={"account_id": account.id},
    )


def create_stripe_customer_for_account(account, email):
    stripe_customer = stripe.Customer.create(
        email=email, metadata={"account_id": account.id}
    )
    djstripe_customer = Customer.sync_from_stripe_data(stripe_customer)

    account.stripe_customer = djstripe_customer


def create_stripe_card_for_account(account, card_id):
    stripe_card = stripe.issuing.Card.retrieve(card_id)
    djstripe_card = Card.sync_from_stripe_data(stripe_card)
    stripe.Customer.modify(
        account.stripe_customer.id,
        invoice_settings={"default_payment_method": card_id},
    )

    account.default_stripe_card = djstripe_card
    if djstripe_card in account.stripe_cards.all():
        account.stripe_cards.remove(djstripe_card)


def subscribe_plan_for_account(customer: Customer, price, account):
    customer.subscribe(items=[{"price": price}])
    account.stripe_price = price
    account.initial_completed = True
    account.save()

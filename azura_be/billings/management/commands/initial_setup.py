from django.core.management.base import BaseCommand

from azura_be.billings.setup_plans import create_plan_method

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        create_plan_method()

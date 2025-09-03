from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP


class Command(BaseCommand):
    help = "Block an IP address by adding it to the BlockedIP table."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="The IP address to block")

    def handle(self, *args, **options):
        ip_address = options["ip_address"]
        try:
            blocked_ip, created = BlockedIP.objects.get_or_create(ip_address=ip_address)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully blocked IP: {ip_address}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"IP {ip_address} is already blocked.")
                )
        except Exception as e:
            raise CommandError(f"Error blocking IP {ip_address}: {e}")

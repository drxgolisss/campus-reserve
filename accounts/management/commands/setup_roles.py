from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from accounts.roles import ROLE_PERMISSIONS


class Command(BaseCommand):
    help = "Create CampusReserve roles and assign their permissions."

    def handle(self, *args, **options):
        permissions_by_name = {
            f"{permission.content_type.app_label}.{permission.codename}": permission
            for permission in Permission.objects.select_related("content_type")
        }

        for role_name, permission_names in ROLE_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=role_name)
            group.permissions.set(
                permissions_by_name[name]
                for name in permission_names
            )
            action = "Created" if created else "Updated"
            if options["verbosity"] >= 1:
                self.stdout.write(f"{action} {role_name} role.")

        if options["verbosity"] >= 1:
            self.stdout.write(self.style.SUCCESS("CampusReserve roles are ready."))

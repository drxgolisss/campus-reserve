from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase

from accounts.roles import ADMINISTRATOR, MANAGER, ROLE_PERMISSIONS, STUDENT


class SetupRolesCommandTests(TestCase):
    def test_command_creates_roles_with_expected_permissions(self):
        call_command("setup_roles", verbosity=0)

        for role_name, expected_permissions in ROLE_PERMISSIONS.items():
            group = Group.objects.get(name=role_name)
            actual_permissions = {
                f"{permission.content_type.app_label}.{permission.codename}"
                for permission in group.permissions.select_related("content_type")
            }
            self.assertEqual(actual_permissions, expected_permissions)

    def test_command_can_be_run_more_than_once(self):
        call_command("setup_roles", verbosity=0)
        call_command("setup_roles", verbosity=0)

        self.assertEqual(Group.objects.count(), len(ROLE_PERMISSIONS))

    def test_role_permissions_apply_to_group_members(self):
        call_command("setup_roles", verbosity=0)
        user_model = get_user_model()
        student = user_model.objects.create_user(username="student-role")
        manager = user_model.objects.create_user(username="manager-role")
        administrator = user_model.objects.create_user(username="administrator-role")

        student.groups.add(Group.objects.get(name=STUDENT))
        manager.groups.add(Group.objects.get(name=MANAGER))
        administrator.groups.add(Group.objects.get(name=ADMINISTRATOR))

        self.assertTrue(student.has_perm("resources.view_studyroom"))
        self.assertTrue(student.has_perm("bookings.add_roombooking"))
        self.assertFalse(student.has_perm("resources.change_studyroom"))
        self.assertFalse(student.has_perm("bookings.change_roombooking"))
        self.assertTrue(manager.has_perm("resources.change_studyroom"))
        self.assertTrue(manager.has_perm("bookings.change_roombooking"))
        self.assertFalse(manager.has_perm("resources.delete_studyroom"))
        self.assertTrue(administrator.has_perm("resources.delete_studyroom"))
        self.assertTrue(administrator.has_perm("auth.change_user"))

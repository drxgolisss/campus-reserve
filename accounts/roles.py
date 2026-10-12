STUDENT = "Student"
MANAGER = "Manager"
ADMINISTRATOR = "Administrator"

ROLE_PERMISSIONS = {
    STUDENT: {
        "resources.view_studyroom",
        "resources.view_equipmentitem",
    },
    MANAGER: {
        "resources.add_studyroom",
        "resources.change_studyroom",
        "resources.view_studyroom",
        "resources.add_equipmentitem",
        "resources.change_equipmentitem",
        "resources.view_equipmentitem",
    },
    ADMINISTRATOR: {
        "resources.add_studyroom",
        "resources.change_studyroom",
        "resources.delete_studyroom",
        "resources.view_studyroom",
        "resources.add_equipmentitem",
        "resources.change_equipmentitem",
        "resources.delete_equipmentitem",
        "resources.view_equipmentitem",
        "auth.add_user",
        "auth.change_user",
        "auth.delete_user",
        "auth.view_user",
        "auth.add_group",
        "auth.change_group",
        "auth.delete_group",
        "auth.view_group",
    },
}

from app.user_management import views as v

ACTION_MAPPING = {
    "roles:delete": "user_management.delete_role",
    "user_management:suspend_user": "user_management.suspend_user",
    "user_management:delete_user": "user_management.delete_user"
}

MESSAGE_MAPPING = {
    "roles:delete": "Are you sure you want to delete the role?",
    "user_management:suspend_user": ("Are you sure you want to "
                                     "suspend this user?"),
    "user_management:delete_user": "Delete user?"
}
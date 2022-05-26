from flask_principal import Permission, RoleNeed

add_users = Permission(RoleNeed('admin.user_mgmt:add_users'))
view_profile = Permission(RoleNeed('admin.user_mgmt:view_user_profile'))
logout_user = Permission(RoleNeed('admin.user_mgmt:logout_user'))
change_user_pwd = Permission(RoleNeed('admin.user_mgmt:change_user_passwd'))
edit_profile = Permission(RoleNeed('admin.user_mgmt:edit_user_profile'))
list_users = Permission(RoleNeed('admin.user_mgmt:list_users'))
suspend_user = Permission(RoleNeed('admin.user_mgmt:suspend_user'))
activate_user = Permission(RoleNeed('admin.user_mgmt:activate_user'))
delete_user = Permission(RoleNeed('admin.user_mgmt:delete_user'))
impersonate_user = Permission(RoleNeed('admin.user_mgmt:impersonate_user'))

list_roles = Permission(RoleNeed('admin.user_mgmt:list_roles'))
add_roles = Permission(RoleNeed('admin.user_mgmt:add_roles'))
edit_roles = Permission(RoleNeed('admin.user_mgmt:edit_roles'))
delete_roles = Permission(RoleNeed('admin.user_mgmt:delete_roles'))
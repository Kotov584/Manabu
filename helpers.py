def get_permissions_for_user(user, method, mode = None):
    allowed_fields = []

    user_groups = user.groups.all()

    for group in user_groups: 
        group_permissions = group.permissions.all()

        for permission in group_permissions:  
            if mode == "create":
                if permission.codename.endswith('_create'):
                    allowed_fields.append(permission.codename.split('_create')[0])

            if mode == "read":
                if permission.codename.endswith('_read'):
                    allowed_fields.append(permission.codename.split('_read')[0])

            if mode == "update":
                if permission.codename.endswith('_update'):
                    allowed_fields.append(permission.codename.split('_update')[0])

            if mode == "delete":
                if permission.codename.endswith('_delete'):
                    allowed_fields.append(permission.codename.split('_delete')[0])

            if mode == "fields":
                if permission.codename.endswith('_field') and permission.codename.startswith(method): 
                    field_name = permission.codename.replace('_field', '')
                    field_name_parts = field_name.split("_") 
                    field_name_parts = field_name_parts[2:]
                    allowed_fields.append(field_name_parts)

    if not allowed_fields:
        return None

    return allowed_fields[0] 
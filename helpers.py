def get_permissions_for_user(user, method, model, mode = None):
    allowed_fields = []

    user_groups = user.groups.all()

    for group in user_groups: 
        group_permissions = group.permissions.all()

        for permission in group_permissions:  
            method_mapping = {
                "create": "create_{}".format(model),
                "read": "read_{}".format(model),
                "update": "update_{}".format(model),
                "delete": "delete_{}".format(model)
            }

            if method in method_mapping:
                if permission.codename == method_mapping[method]:
                    allowed_fields.append(permission.codename)

            if mode == "fields":
                if permission.codename.endswith('_field') and permission.codename.startswith(method): 
                    field_name = permission.codename.replace('_field', '')
                    field_name_parts = field_name.split("_") 
                    field_name_parts = field_name_parts[2:]
                    allowed_fields.append(field_name_parts)

    if not allowed_fields:
        return None

    return allowed_fields[0] 
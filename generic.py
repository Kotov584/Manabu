from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group, Permission

def get_permissions_for_user(user, method, model, mode = None):
    allowed_fields = []

    user_groups = user.groups.all()

    for group in user_groups: 
        group_permissions = group.permissions.all()

        for permission in group_permissions:  
            method_mapping = {
                "create": "add_{}".format(model),
                "read": "view_{}".format(model),
                "update": "change_{}".format(model),
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

class GenericRepository:
    def __init__(self, model_class): 
        self.model_class = model_class
        self.objects = model_class.objects

    def all(self):
        return self.objects.all()

    def get(self, **kwargs):
        return self.objects.get(**kwargs)

    def filter(self, **kwargs):
        return self.objects.filter(**kwargs)

    def create(self, **kwargs):
        return self.objects.create(**kwargs)

    def update(self, instance, **kwargs):
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        
        instance.save()

        return instance

    def delete(self, instance):
        instance.delete()

class GenericAPIView(APIView):
    model_class = None
    permisssion_classes = None

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.repository = GenericRepository(self.model_class) 

    def get(self, request, id=None, format=None):
        allowed_fields = get_permissions_for_user(request.user, 'read', self.model_name)  

        if not allowed_fields:
            return Response({"error": "Permission denied"}, status=status.HTTP_400_BAD_REQUEST)

        allowed_fields = get_permissions_for_user(request.user, 'view_', self.model_name, 'fields') 

        if id:
            instance = self.repository.get(id=id)

            if not instance:
                return Response({"error": "Instance not found"}, status=status.HTTP_404_NOT_FOUND)

            instance_dict = model_to_dict(instance) 
            filtered_instance = {field: instance_dict[field] for field in allowed_fields if field in instance_dict}
            
            return Response({"instance": filtered_instance})

        instances = self.repository.all()

        if not instances:                
            return Response({"error": "Instances not found"}, status=status.HTTP_404_NOT_FOUND)

        instance_dicts = [model_to_dict(inst) for inst in instances]
        filtered_instances = []
        for instance_dict in instance_dicts:
            filtered_instance = {field: instance_dict[field] for field in allowed_fields if field in instance_dict}
            filtered_instances.append(filtered_instance)

        return Response({"instances": filtered_instances})

    def post(self, request, format=None):
        try:
            data = request.data
            instance = self.repository.create(**data)
        
        except Exception as error: 
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        
        instance_dict = model_to_dict(instance)
        return Response({"instance": instance_dict})

    def put(self, request, id, format=None):
        try:
            instance = self.repository.get(id=id)
            
            if not instance:
                return Response({"error": "Instance not found"}, status=status.HTTP_404_NOT_FOUND) 
            
            allowed_fields = get_permissions_for_user(request.user, 'view_', 'fields')
            filtered_data = {field: request.data[field] for field in allowed_fields if field in request.data}
            instance = self.repository.update(instance, **filtered_data)
            instance_dict = model_to_dict(instance)
            filtered_instance = {field: instance_dict[field] for field in allowed_fields if field in instance_dict}

            return Response({"instance": filtered_instance})
        
        except ValidationError as error:
            return Response({"error": error.detail}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None): 
        instance = self.repository.get(id=id)
        
        if not instance:
            return Response({"error": "Instance not found"}, status=status.HTTP_404_NOT_FOUND)
        
        self.repository.delete(instance)
        
        return Response({"message": "Instance deleted"})

class GenericView(GenericAPIView):
    model_class = None
    model_name = None
    model_name_plural = None
    permission_classes = None

    def get(self, request, *args, **kwargs):  
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)